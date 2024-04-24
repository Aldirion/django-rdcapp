from typing import TypedDict

from collections import defaultdict

from django.shortcuts import get_object_or_404, get_list_or_404

from django.db.models import F, OuterRef
from django_stubs_ext import WithAnnotations

from rest_framework import generics, status, views
from rest_framework.response import Response

# from ...models___ import Municipality

from .utils import SubqueryCount, Subquery

from . import models
from .serializers import (
    RegionSerializer,
    SchoolSerializer,
    EmployeeSerializer,
    MunicipalitySerializer,
)


# Отображение регионов/региона
class RegionView(generics.ListAPIView):
    pagination_class = None
    serializer_class = RegionSerializer

    def get_queryset(self):
        queryset = models.Region.objects.exclude(id=91).annotate(
            comp_count_spo=SubqueryCount(
                models.EduInstitution.objects.filter(
                    type=1,
                    sign=0,
                    municipality__region_id=OuterRef("id"),
                ).values_list("id")
            ),
            comp_count_school=SubqueryCount(
                models.EduInstitution.objects.filter(
                    type=0,
                    sign=0,
                    municipality__region_id=OuterRef("id"),
                ).values_list("id")
            ),
            rrc_address=Subquery(
                models.Rc.objects.filter(region_id=OuterRef("id")).values("address"),
            ),
            rrc_email=Subquery(
                models.Rc.objects.filter(region_id=OuterRef("id")).values("email"),
            ),
        )

        codegost = self.request.query_params.get("codegost")

        if codegost:
            queryset = queryset.filter(
                codegost=codegost,
            )

        return queryset


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


class RegionMunicipalityView(views.APIView):
    pagination_class = None
    serializer_class = MunicipalitySerializer

    def get(self, request, regionid, *args, **kwargs):
        # regionid=self.kwargs['region']
        queryset = models.Municipality.objects.filter(region_id=regionid).annotate(
            comp_count_school=SubqueryCount(
                models.EduInstitution.objects.filter(
                    type=0,
                    sign=0,
                    municipality_id=OuterRef("id"),
                ).values_list("id")
            ),
            comp_count_spo=SubqueryCount(
                models.EduInstitution.objects.filter(
                    type=1,
                    sign=0,
                    municipality_id=OuterRef("id"),
                ).values_list("id")
            ),
        )
        serializer = MunicipalitySerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class RegionEduInstOriginQuerySet(TypedDict):
    regionid: int
    municipality_title: str
    region: str


# TODO: Separate on two endpoints
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


# TODO: Separate on two endpoints
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
                municipality_id=municipalityid, sign=0
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
                municipality_id=municipalityid, sign=0, type=1
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
