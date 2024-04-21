from typing import TypedDict

from collections import defaultdict

from django.db.models import F, OuterRef
from django_stubs_ext import WithAnnotations

from rest_framework import generics, status, views
from rest_framework.response import Response

from .utils import SubqueryCount

from . import models
from .serializers import (
    RegionSerializer,
    SchoolSerializer,
    EmployeeSerializer,
    MunicipalitySerializer,
)


def get_default_color_identifier(val):
    # colors={
    #     "0":"F85151",
    #     "1":"F87351",
    #     "2":"F88651",
    #     "3":"F89C51",
    #     "4":"F8BB51",
    #     "5":"F8DC51",
    #     "6":"E5F851",
    #     "7":"CCF851",
    #     "8":"BEF851",
    #     "9":"51F85F",
    #     "10":"51F897",
    # }
    # if val<10:
    #     return colors["0"]
    # elif val
    colors=["F85151","F87351","F88651","F89C51","F8BB51","F8DC51","E5F851","CCF851","BEF851","51F85F","51F897"]

    color=(255-255*val//100, 255*val//100, 0)
    return colors[val//10]



# Отображение регионов/региона
class RegionView(generics.ListAPIView):
    pagination_class = None
    serializer_class = RegionSerializer

    def get_queryset(self):
        queryset = models.Region.objects.annotate(
            comp_count_spo=SubqueryCount(
                models.EduInstitution.objects.filter(
                    type=1,
                    sign=0,
                    municipality__region_id=OuterRef('id'),
                ).values_list('id')
            ),
            comp_count_school=SubqueryCount(
                models.EduInstitution.objects.filter(
                    type=0,
                    sign=0,
                    municipality__region_id=OuterRef('id'),
                ).values_list('id')
            )
        )

        codegost = self.request.query_params.get('codegost')

        if codegost:
            queryset = queryset.filter(
                codegost=codegost,
            )

        return queryset



class RegionEmployeeQuerySet(TypedDict):
    post_title: str


class RegionEmployeeView(views.APIView):
    def get(self, request, regionid, *args, **kwargs):
        employees: tuple[WithAnnotations[
            models.Employee,
            RegionEmployeeQuerySet,
        ], ...] = tuple(
            models.Employee.objects.filter(region_id=regionid).annotate(
                post_title=F('employeepost__post__title'),
            ).order_by(
                'employeepost__post__priority'
            )
        )

        response = defaultdict(
            lambda: {
                'count': 0,
                'data': list(),
            }
        )

        for employee in employees:
            item = response[employee.post_title]
            item['count'] += 1
            item['data'].append(EmployeeSerializer(employee).data)

        # print (response)
        return Response(response, status=status.HTTP_200_OK)


class RegionMunicipalityView(views.APIView):
    def get(self, request, regionid, *args, **kwargs):
        municipalities = tuple(
            models.Municipality.objects.filter(
                region_id=regionid
            )
        )

        return Response(
            MunicipalitySerializer(
                municipalities,
                many=True
            ).data,
            status=status.HTTP_200_OK
        )

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
            ], ...
        ] = tuple(
            models.EduInstitution.objects.filter(sign=0).annotate(
                regionid=F("municipality__region__id"),
                municipality_title=F("municipality__title"),
                region=F("municipality__region__title"),
            ).filter(
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


# TODO: Separate on two endpoints
class MunicipalityEduInstOriginView(views.APIView):
    def get(self, request, regionid, municipalityid, *args, **kwargs):
        municipality = models.Municipality.objects.filter(id=municipalityid)
        if municipality[0].region.id != regionid:
            return Response(
                "Указанный муниципалитет не входит в состав выбранного региона",
                status=status.HTTP_400_BAD_REQUEST,
            )
        eduinstitutions = tuple(
            models.EduInstitution.objects.filter(municipality_id=municipalityid)
            .filter(sign=0)
            .annotate(
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
