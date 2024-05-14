import json
from collections import defaultdict
from email.policy import default
from typing import TypedDict

from django.db.models import F, IntegerField, OuterRef, Count, Q, Sum
from django.db.models.fields.json import KT
from django.db.models.functions import Cast
from django.db.models.expressions import RawSQL
from django.shortcuts import get_object_or_404
from django_stubs_ext import WithAnnotations
from django_cte import With
from rest_framework import generics, permissions, status, views
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

from . import models
from .serializers import (
    EmployeeProfileSerializer,
    EmployeeSerializer,
    FedEmployeeSerializer,
    MunicipalitySerializer,
    RegionSerializer,
    SchoolDetailSerializer,
    SchoolSerializer,
)
from .utils import Subquery, SubqueryCount, SubquerySum


# Отображение профилей пользователей
@api_view(["GET", "PUT"])
@permission_classes([permissions.IsAuthenticated])
def profile(request):
    user = request.user
    userprofile = models.Employee.objects.annotate(
        post_title=F("employeepost__post__title"),
        post_subdivision=F("employeepost__post__subdivision__title"),
        tab_number=F("employeepost__tab_number"),
    ).get(user_id=user.id)
    user_posts = list(
        models.EmployeePost.objects.filter(employee=userprofile)
        .annotate(
            post_title=F("post__title"),
            subdivision_title=F("post__subdivision__title"),
        )
        .values("post_title", "subdivision_title", "tab_number")
    )
    user_eduinstitutions = list(
        models.EduInstitutionEmployee.objects.filter(employee=userprofile).annotate(
            edu_inst_title=F("edu_institution__title")
        )
    )
    userprofile.posts = user_posts
    userprofile.eduinstitutions = user_eduinstitutions
    if request.method == "GET":
        serializer = EmployeeProfileSerializer(userprofile, many=False)
    elif request.method == "PUT":
        serializer = EmployeeProfileSerializer(
            userprofile, data=request.data, partial=True
        )
        if serializer.is_valid():
            serializer.save()
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(["GET"])
@permission_classes([permissions.IsAuthenticated])
def get_some_profile(request, userid):
    userprofile = models.Employee.objects.annotate(
        post_title=F("employeepost__post__title"),
        post_subdivision=F("employeepost__post__subdivision__title"),
        tab_number=F("employeepost__tab_number"),
    ).get(user_id=userid)
    user_posts = list(
        models.EmployeePost.objects.filter(employee=userprofile)
        .annotate(
            post_title=F("post__title"),
            subdivision_title=F("post__subdivision__title"),
        )
        .values("post_title", "subdivision_title", "tab_number")
    )
    user_eduinstitutions = list(
        models.EduInstitutionEmployee.objects.filter(employee=userprofile).annotate(
            edu_inst_title=F("edu_institution__title")
        )
    )
    userprofile.posts = user_posts
    userprofile.eduinstitutions = user_eduinstitutions
    serializer = EmployeeProfileSerializer(userprofile, many=False)
    return Response(serializer.data, status=status.HTTP_200_OK)


# Отображение регионов/региона
class RegionView(views.APIView):
    pagination_class = None
    serializer_class = RegionSerializer

    def get_school_data(self):
        cte_queryset = (
            models.EduInstitution.objects.annotate(
                region_id=F("municipality__region_id")
            )
            .filter(
                type=0,
            )
            .values(
                "region_id",
                "type",
            )
        )
        cte = With(cte_queryset)

        queryset = models.Region.objects.exclude(
            id=91
        )  # TODO: Hardcode ID is a very bad idead, better come with a better marker
        codegost = self.request.query_params.get("codegost")

        if codegost:
            queryset = queryset.filter(
                codegost=codegost,
            )

        school_eduenv_dict = {
            "total_kdn": Cast(KT("eduenv__kdn"), output_field=IntegerField()),
            "total_museum": Cast(KT("eduenv__museum"), output_field=IntegerField()),
            "total_mediacentre": Cast(KT("eduenv__kdn"), output_field=IntegerField()),
            "total_theatre": Cast(KT("eduenv__theatre"), output_field=IntegerField()),
            "total_tour_club": Cast(
                KT("eduenv__tour_club"), output_field=IntegerField()
            ),
            "total_cinema_club": Cast(
                KT("eduenv__cinema_club"), output_field=IntegerField()
            ),
            "total_mpc": Cast(KT("eduenv__mpc"), output_field=IntegerField()),
            "total_yunarmy_participants": Cast(
                KT("eduenv__yunarmy_participants"), output_field=IntegerField()
            ),
            "total_classes_are_eagles": Cast(
                KT("eduenv__classes_are_eagles"), output_field=IntegerField()
            ),
            "total_ssc": Cast(KT("eduenv__ssc"), output_field=IntegerField()),
            "total_volunteers_squad": Cast(
                KT("eduenv__volunteers_squad"), output_field=IntegerField()
            ),
            "total_leaders_squad": Cast(
                KT("eduenv__leaders_squad"), output_field=IntegerField()
            ),
            "total_uid": Cast(KT("eduenv__uid"), output_field=IntegerField()),
            "total_y_rescuers_squad": Cast(
                KT("eduenv__y_rescuers_squad"), output_field=IntegerField()
            ),
        }

        for name, lookup in school_eduenv_dict.items():
            cte_queryset = cte_queryset.annotate(
                **{
                    f"school_{name}": Sum(lookup),
                }
            )

        cte_queryset = cte_queryset.annotate(
            school_total_cdi=Count(RawSQL("1", ()), filter=Q(eduenv__cdi=True)),
            school_total_ssgo=Count(RawSQL("1", ()), filter=Q(eduenv__ssgo=True)),
            school_total_leaders_league=Count(
                RawSQL("1", ()), filter=Q(eduenv__leaders_league=True)
            ),
        )

        cte = With(cte_queryset)
        queryset = queryset.annotate(
            school_total_cdi=RawSQL("cte.school_total_cdi", ()),
            school_total_ssgo=RawSQL("cte.school_total_ssgo", ()),
            school_total_leaders_league=RawSQL("cte.school_total_leaders_league", ()),
        )

        for name, lookup in school_eduenv_dict.items():
            queryset = queryset.annotate(
                **{
                    f"school_{name}": Sum(
                        getattr(cte.col, f"school_{name}"),
                    ),
                }
            )

        queryset = cte.join(queryset, id=cte.col.region_id).with_cte(cte)

        data = {}
        for item in queryset:
            item_data = {}
            for name in school_eduenv_dict.keys():
                item_data[name] = getattr(item, f"school_{name}") or 0

            item_data["total_cdi"] = item.school_total_cdi
            item_data["total_ssgo"] = item.school_total_ssgo
            item_data["total_leaders_league"] = item.school_total_leaders_league

            data[item.id] = item_data

        return data

    def get_spo_data(self):
        cte_queryset = (
            models.EduInstitution.objects.annotate(
                region_id=F("municipality__region_id")
            )
            .filter(
                type=1,
            )
            .values(
                "region_id",
                "type",
            )
        )
        cte = With(cte_queryset)

        queryset = models.Region.objects.exclude(
            id=91
        )  # TODO: Hardcode ID is a very bad idead, better come with a better marker
        codegost = self.request.query_params.get("codegost")

        if codegost:
            queryset = queryset.filter(
                codegost=codegost,
            )

        spo_eduenv_dict = {
            "total_kdn": Cast(KT("eduenv__kdn"), output_field=IntegerField()),
            "total_museum": Cast(KT("eduenv__museum"), output_field=IntegerField()),
            "total_mediacentre": Cast(KT("eduenv__kdn"), output_field=IntegerField()),
            "total_theatre": Cast(KT("eduenv__theatre"), output_field=IntegerField()),
            "total_tour_club": Cast(
                KT("eduenv__tour_club"), output_field=IntegerField()
            ),
            "total_cinema_club": Cast(
                KT("eduenv__cinema_club"), output_field=IntegerField()
            ),
            "total_mpc": Cast(KT("eduenv__mpc"), output_field=IntegerField()),
            "total_ssc": Cast(KT("eduenv__ssc"), output_field=IntegerField()),
            "total_volunteers_squad": Cast(
                KT("eduenv__volunteers_squad"), output_field=IntegerField()
            ),
            "total_leaders_squad": Cast(
                KT("eduenv__leaders_squad"), output_field=IntegerField()
            ),
            "total_ccr": Cast(KT("eduenv__ccr"), output_field=IntegerField()),
        }

        for name, lookup in spo_eduenv_dict.items():
            cte_queryset = cte_queryset.annotate(
                **{
                    f"spo_{name}": Sum(lookup),
                }
            )

        cte_queryset = cte_queryset.annotate(
            spo_total_cdi=Count(RawSQL("1", ()), filter=Q(eduenv__cdi=True)),
            spo_total_ssgo=Count(RawSQL("1", ()), filter=Q(eduenv__ssgo=True)),
            spo_total_leaders_league=Count(
                RawSQL("1", ()), filter=Q(eduenv__leaders_league=True)
            ),
        )

        cte = With(cte_queryset)
        queryset = queryset.annotate(
            spo_total_cdi=RawSQL("cte.spo_total_cdi", ()),
            spo_total_ssgo=RawSQL("cte.spo_total_ssgo", ()),
            spo_total_leaders_league=RawSQL("cte.spo_total_leaders_league", ()),
        )

        for name, lookup in spo_eduenv_dict.items():
            queryset = queryset.annotate(
                **{
                    f"spo_{name}": Sum(
                        getattr(cte.col, f"spo_{name}"),
                    ),
                }
            )

        queryset = cte.join(queryset, id=cte.col.region_id).with_cte(cte)

        data = {}
        for item in queryset:
            item_data = {}
            for name in spo_eduenv_dict.keys():
                item_data[name] = getattr(item, f"spo_{name}") or 0

            item_data["total_cdi"] = item.spo_total_cdi
            item_data["total_ssgo"] = item.spo_total_ssgo
            item_data["total_leaders_league"] = item.spo_total_leaders_league

            data[item.id] = item_data

        return data

    def get(self, request):
        cte = With(
            models.EduInstitution.objects.values("type")
            .annotate(type_count=Count("type"), region_id=F("municipality__region_id"))
            .filter(
                sign=0,
            )
            .values("type", "region_id", "type_count")
            .order_by(),
            materialized=True,
        )

        queryset = (
            models.Region.objects.exclude(id=91)
            .annotate(
                comp_count_spo=Subquery(
                    cte.queryset()
                    .filter(type=1, region_id=OuterRef("id"))
                    .values("type_count")
                ),
                comp_count_school=Subquery(
                    cte.queryset()
                    .filter(type=0, region_id=OuterRef("id"))
                    .values("type_count")
                ),
                rrc_address=Subquery(
                    models.Rc.objects.filter(region_id=OuterRef("id")).values(
                        "address"
                    ),
                ),
                rrc_email=Subquery(
                    models.Rc.objects.filter(region_id=OuterRef("id")).values("email"),
                ),
            )
            .with_cte(cte)
        )

        codegost = self.request.query_params.get("codegost")

        if codegost:
            queryset = queryset.filter(
                codegost=codegost,
            )

        response_data = []
        school_data = self.get_school_data()
        spo_data = self.get_spo_data()

        for item in queryset:
            data = RegionSerializer(item).data

            data["school"] = school_data.get(item.id)
            data["spo"] = spo_data.get(item.id)

            response_data.append(data)
        return Response(response_data, status=status.HTTP_200_OK)


class RegionEmployeeQuerySet(TypedDict):
    post_title: str


class RegionEmployeeView(views.APIView):
    def get(self, request, regionid, *args, **kwargs):
        employees: tuple[
            WithAnnotations[
                models.Employee,
                RegionEmployeeQuerySet,
            ],
            ...,
        ] = tuple(
            models.Employee.objects.filter(region_id=regionid)
            .annotate(
                post_title=F("employeepost__post__title"),
            )
            .order_by("employeepost__post__priority")
        )

        response = defaultdict(
            lambda: {
                "count": 0,
                "data": list(),
            }
        )

        for employee in employees:
            item = response[employee.post_title]
            item["count"] += 1
            item["data"].append(EmployeeSerializer(employee).data)

        # print (response)
        return Response(response, status=status.HTTP_200_OK)

class FederalEmployeeQuerySet(TypedDict):
    post_title: str
    post_subdivision: str

# @permission_classes([permissions.IsAuthenticated])
class FederalEmployeeView(views.APIView):
    def get(self, request, *args, **kwargs):
        # subdivisions = tuple(models.Subdivision.objects)
        employees = tuple(
                models.Employee.objects.filter(region_id=91) #TODO: HARDCODE id BAD refactor
                .annotate(
                    post_title=F("employeepost__post__title"),
                    post_subdivision=F("employeepost__post__subdivision__title"),
                    post_sd_id=F("employeepost__post__subdivision__id"),
                    post_sd_par=F("employeepost__post__subdivision__parent"),
                    post_sd_par_t=F("employeepost__post__subdivision__parent__title"),
                )
                .order_by("employeepost__post__priority")
            )
        deps = defaultdict(
            lambda: {
                "count":0,
                "data": list()
            }
        )
        response = defaultdict(
                lambda: {
                    "count": 0,
                    "data": list(),
                    "departments": dict()
                }
            )
        # for subdiv in subdivisions:
        #     item = deps[subdiv]

        for employee in employees:
            item = response[employee.post_subdivision]
            item["count"] += 1
            item["data"].append(FedEmployeeSerializer(employee).data)
        return Response(response, status=status.HTTP_200_OK)

# def MySum(Sum)
class RegionMunicipalityView(views.APIView):
    pagination_class = None
    serializer_class = MunicipalitySerializer

    def get(self, request, regionid, *args, **kwargs):
        fields = ["id", "type", "sign", "municipality", "eduenv"]
        eduinstitutions = models.EduInstitution.objects.filter(
            municipality_id=OuterRef("pk"),
        ).values_list(*fields)
        queryset = models.Municipality.objects.filter(region_id=regionid).annotate(
            comp_count_school=SubqueryCount(
                eduinstitutions.filter(
                    type=0,
                    sign=0,
                ).values_list("id")
            ),
            comp_count_spo=SubqueryCount(
                eduinstitutions.filter(
                    type=1,
                    sign=0,
                ).values_list("id")
            ),
        )
        school_eduenv_dict = {
            "total_kdn": Cast(KT("eduenv__kdn"), output_field=IntegerField()),
            "total_museum": Cast(KT("eduenv__museum"), output_field=IntegerField()),
            "total_mediacentre": Cast(KT("eduenv__kdn"), output_field=IntegerField()),
            "total_theatre": Cast(KT("eduenv__theatre"), output_field=IntegerField()),
            "total_tour_club": Cast(
                KT("eduenv__tour_club"), output_field=IntegerField()
            ),
            "total_cinema_club": Cast(
                KT("eduenv__cinema_club"), output_field=IntegerField()
            ),
            "total_mpc": Cast(KT("eduenv__mpc"), output_field=IntegerField()),
            "total_yunarmy_participants": Cast(
                KT("eduenv__yunarmy_participants"), output_field=IntegerField()
            ),
            "total_classes_are_eagles": Cast(
                KT("eduenv__classes_are_eagles"), output_field=IntegerField()
            ),
            "total_ssc": Cast(KT("eduenv__ssc"), output_field=IntegerField()),
            "total_volunteers_squad": Cast(
                KT("eduenv__volunteers_squad"), output_field=IntegerField()
            ),
            "total_leaders_squad": Cast(
                KT("eduenv__leaders_squad"), output_field=IntegerField()
            ),
            # 'total_leaders_league': Sum(Cast(KT("eduenv__leaders_league"), output_field=IntegerField())),
            "total_uid": Cast(KT("eduenv__uid"), output_field=IntegerField()),
            "total_y_rescuers_squad": Cast(
                KT("eduenv__y_rescuers_squad"), output_field=IntegerField()
            ),
        }
        spo_eduenv_dict = {
            "total_kdn": Cast(KT("eduenv__kdn"), output_field=IntegerField()),
            "total_museum": Cast(KT("eduenv__museum"), output_field=IntegerField()),
            "total_mediacentre": Cast(KT("eduenv__kdn"), output_field=IntegerField()),
            "total_theatre": Cast(KT("eduenv__theatre"), output_field=IntegerField()),
            "total_tour_club": Cast(
                KT("eduenv__tour_club"), output_field=IntegerField()
            ),
            "total_cinema_club": Cast(
                KT("eduenv__cinema_club"), output_field=IntegerField()
            ),
            "total_mpc": Cast(KT("eduenv__mpc"), output_field=IntegerField()),
            "total_ssc": Cast(KT("eduenv__ssc"), output_field=IntegerField()),
            "total_volunteers_squad": Cast(
                KT("eduenv__volunteers_squad"), output_field=IntegerField()
            ),
            "total_leaders_squad": Cast(
                KT("eduenv__leaders_squad"), output_field=IntegerField()
            ),
            "total_ccr": Cast(KT("eduenv__ccr"), output_field=IntegerField()),
        }
        for name, lookup in school_eduenv_dict.items():
            queryset = queryset.annotate(
                **{
                    f"school_{name}": SubquerySum(
                        eduinstitutions.filter(type=0)
                        .annotate(agg_value=lookup)
                        .values("agg_value"),
                        column="agg_value",
                    ),
                }
            )
        queryset = queryset.annotate(
            school_total_cdi=SubqueryCount(
                eduinstitutions.filter(type=0, eduenv__cdi=True)
            ),
            school_total_ssgo=SubqueryCount(
                eduinstitutions.filter(type=0, eduenv__ssgo=True)
            ),
            school_total_leaders_league=SubqueryCount(
                eduinstitutions.filter(type=0, eduenv__leaders_league=True)
            ),
        )
        for name, lookup in spo_eduenv_dict.items():
            queryset = queryset.annotate(
                **{
                    f"spo_{name}": SubquerySum(
                        eduinstitutions.filter(type=1)
                        .annotate(agg_value=lookup)
                        .values("agg_value"),
                        column="agg_value",
                    ),
                }
            )
        queryset = queryset.annotate(
            spo_total_cyi=SubqueryCount(
                eduinstitutions.filter(type=1, eduenv__cyi=True)
            ),
            spo_total_ssgo=SubqueryCount(
                eduinstitutions.filter(type=1, eduenv__ssgo=True)
            ),
            spo_total_leaders_league=SubqueryCount(
                eduinstitutions.filter(type=1, eduenv__leaders_league=True)
            ),
        )
        response_data = []
        for item in queryset:
            data = MunicipalitySerializer(item).data
            data["school"] = {}
            data["spo"] = {}
            for name in school_eduenv_dict.keys():
                data["school"][name] = getattr(item, f"school_{name}")
            data["school"]["total_cdi"] = getattr(item, "school_total_cdi")
            data["school"]["total_ssgo"] = getattr(item, "school_total_ssgo")
            data["school"]["total_leaders_league"] = getattr(
                item, "school_total_leaders_league"
            )
            for name in spo_eduenv_dict.keys():
                data["spo"][name] = getattr(item, f"spo_{name}")
            data["spo"]["total_cyi"] = getattr(item, "spo_total_cyi")
            data["spo"]["total_ssgo"] = getattr(item, "spo_total_ssgo")
            data["spo"]["total_leaders_league"] = getattr(
                item, "spo_total_leaders_league"
            )
            response_data.append(data)
        return Response(response_data, status=status.HTTP_200_OK)


# Отображение списка образовательных учреждений на уровне региона/муниципалитета
class RegionEduInstOriginQuerySet(TypedDict):
    regionid: int
    municipality_title: str
    region: str


class RegionEduInstOriginView(views.APIView):
    def get(self, request, regionid, *args, **kwargs):
        eduinstitutions: tuple[
            WithAnnotations[
                models.EduInstitution,
                RegionEduInstOriginQuerySet,
            ],
            ...,
        ] = tuple(
            models.EduInstitution.objects.filter(sign=0)
            .annotate(
                regionid=F("municipality__region__id"),
                municipality_title=F("municipality__title"),
                region=F("municipality__region__title"),
            )
            .filter(
                regionid=regionid,
            )
        )

        eduinstitutions_c = defaultdict(
            lambda: {
                "schools": dict({"count": 0, "schools": list()}),
                "spo": dict({"count": 0, "spo": list()}),
            }
        )

        for eduinst in eduinstitutions:
            item = eduinstitutions_c[eduinst.municipality_title]
            if eduinst.type == 0:
                item["schools"]["count"] += 1
                item["schools"]["schools"].append(SchoolSerializer(eduinst).data)
            else:
                item["spo"]["count"] += 1
                item["spo"]["spo"].append(SchoolSerializer(eduinst).data)

        response = dict(
            {
                "count_schools": sum(
                    value["schools"]["count"] for value in eduinstitutions_c.values()
                ),
                "count_spo": sum(
                    value["spo"]["count"] for value in eduinstitutions_c.values()
                ),
                "data": eduinstitutions_c,
            }
        )
        return Response(response, status=status.HTTP_200_OK)


class RegionSchoolsOriginView(views.APIView):
    def get(self, request, regionid, *args, **kwargs):
        eduinstitutions: tuple[
            WithAnnotations[
                models.EduInstitution,
                RegionEduInstOriginQuerySet,
            ],
            ...,
        ] = tuple(
            models.EduInstitution.objects.filter(sign=0, type=0)
            .annotate(
                regionid=F("municipality__region__id"),
                municipality_title=F("municipality__title"),
                region=F("municipality__region__title"),
            )
            .filter(
                regionid=regionid,
            )
        )

        eduinstitutions_c = defaultdict(
            lambda: {
                "count": 0,
                "schools": list(),
                # "schools": dict({"count": 0, "data": list()}),
            }
        )

        for eduinst in eduinstitutions:
            item = eduinstitutions_c[eduinst.municipality_title]
            item["count"] += 1
            item["schools"].append(SchoolSerializer(eduinst).data)

        response = dict(
            {
                "count_schools": sum(
                    value["count"] for value in eduinstitutions_c.values()
                ),
                "data": eduinstitutions_c,
            }
        )
        return Response(response, status=status.HTTP_200_OK)


class RegionSPOOriginView(views.APIView):
    def get(self, request, regionid, *args, **kwargs):
        eduinstitutions: tuple[
            WithAnnotations[
                models.EduInstitution,
                RegionEduInstOriginQuerySet,
            ],
            ...,
        ] = tuple(
            models.EduInstitution.objects.filter(sign=0, type=1)
            .annotate(
                regionid=F("municipality__region__id"),
                municipality_title=F("municipality__title"),
                region=F("municipality__region__title"),
            )
            .filter(
                regionid=regionid,
            )
        )

        eduinstitutions_c = defaultdict(
            lambda: {
                "count": 0,
                "spo": list(),
                # "schools": dict({"count": 0, "data": list()}),
            }
        )

        for eduinst in eduinstitutions:
            item = eduinstitutions_c[eduinst.municipality_title]
            item["count"] += 1
            item["spo"].append(SchoolSerializer(eduinst).data)

        response = dict(
            {
                "count_spo": sum(
                    value["count"] for value in eduinstitutions_c.values()
                ),
                "data": eduinstitutions_c,
            }
        )
        return Response(response, status=status.HTTP_200_OK)


class MunicipalityEduInstOriginView(views.APIView):
    def get(self, request, regionid, municipalityid, *args, **kwargs):
        # municipality = models.Municipality.objects.get(id=municipalityid)
        municipality = get_object_or_404(models.Municipality, pk=municipalityid)
        print(municipality)
        if municipality.region.id != regionid:
            return Response(
                "Указанный муниципалитет не входит в состав выбранного региона",
                status=status.HTTP_400_BAD_REQUEST,
            )
        eduinstitutions = tuple(
            models.EduInstitution.objects.filter(
                municipality_id=municipalityid,
                # sign=0
            ).annotate(
                regionid=F("municipality__region__id"),
            )
        )
        response = defaultdict(
            lambda: {
                "municipality": eduinstitutions[0].municipality.title,
                "count": 0,
                "schools": dict({"count": 0, "schools": list()}),
                "spo": dict({"count": 0, "spo": list()}),
            }
        )
        for eduinst in eduinstitutions:
            item = response[eduinst.municipality.id]
            item["count"] += 1

            if eduinst.type == 0:
                item["schools"]["count"] += 1
                item["schools"]["schools"].append(SchoolSerializer(eduinst).data)
            else:
                item["spo"]["count"] += 1
                item["spo"]["spo"].append(SchoolSerializer(eduinst).data)

        return Response(response, status=status.HTTP_200_OK)


class MunicipalitySchoolOriginView(views.APIView):
    def get(self, request, regionid, municipalityid, *args, **kwargs):
        # municipality = models.Municipality.objects.filter(id=municipalityid)
        municipality = get_object_or_404(models.Municipality, pk=municipalityid)
        if municipality.region.id != regionid:
            return Response(
                "Указанный муниципалитет не входит в состав выбранного региона",
                status=status.HTTP_400_BAD_REQUEST,
            )
        eduinstitutions = tuple(
            models.EduInstitution.objects.filter(
                municipality_id=municipalityid, sign=0, type=0
            ).annotate(
                regionid=F("municipality__region__id"),
            )
        )
        response = defaultdict(
            lambda: {
                "municipality": eduinstitutions[0].municipality.title,
                "count": 0,
                "schools": list(),
            }
        )
        for eduinst in eduinstitutions:
            item = response[eduinst.municipality.id]
            item["count"] += 1
            item["schools"].append(SchoolSerializer(eduinst).data)

        return Response(response, status=status.HTTP_200_OK)


class MunicipalitySPOOriginView(views.APIView):
    def get(self, request, regionid, municipalityid, *args, **kwargs):
        # municipality = models.Municipality.objects.filter(id=municipalityid)
        municipality = get_object_or_404(models.Municipality, pk=municipalityid)
        if municipality.region.id != regionid:
            return Response(
                "Указанный муниципалитет не входит в состав выбранного региона",
                status=status.HTTP_400_BAD_REQUEST,
            )
        eduinstitutions = tuple(
            models.EduInstitution.objects.filter(
                municipality_id=municipalityid, type=1
            ).annotate(
                regionid=F("municipality__region__id"),
            )
        )
        response = defaultdict(
            lambda: {
                "municipality": eduinstitutions[0].municipality.title,
                "count": 0,
                "spo": list(),
            }
        )
        for eduinst in eduinstitutions:
            item = response[eduinst.municipality.id]
            item["count"] += 1
            item["spo"].append(SchoolSerializer(eduinst).data)

        return Response(response, status=status.HTTP_200_OK)


class EduInstitutionDetailView(views.APIView):
    def get(
        self, request, regionid=None, municipalityid=None, id=None, *args, **kwargs
    ):
        eduinstitution = get_object_or_404(models.EduInstitution, pk=id)
        data = SchoolDetailSerializer(eduinstitution, many=False).data
        if regionid is not None:
            if municipalityid is not None:
                municipality = get_object_or_404(models.Municipality, pk=municipalityid)
                if municipality.region.id != regionid:
                    return Response(
                        "Указанный муниципалитет не входит в состав выбранного региона",
                        status=status.HTTP_400_BAD_REQUEST,
                    )
                else:
                    if eduinstitution.municipality.id != municipality.id:
                        return Response(
                            "Указанное образовательное учреждение не входит в состав выбранного муниципалитета",
                            status=status.HTTP_400_BAD_REQUEST,
                        )
                    else:
                        return Response(data, status=status.HTTP_200_OK)
            elif eduinstitution.municipality.region.id != regionid:
                return Response(
                    "Указанное образовательное учреждение не входит в состав выбранного региона",
                    status=status.HTTP_400_BAD_REQUEST,
                )
            else:
                return Response(data, status=status.HTTP_200_OK)
        else:
            return Response(data, status=status.HTTP_200_OK)
