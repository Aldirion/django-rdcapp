from django.shortcuts import render
from django.views.generic import ListView
from django.db.models import Func, F, Value
from collections import defaultdict

from django.contrib.auth.models import Group, User
from rest_framework import permissions, viewsets, status
from rest_framework.views import APIView
from rest_framework.response import Response

from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from django.db.models import Count


from .serializers import *


# Отображение регионов/региона
class RegionView(APIView):
    def get(self, request, *args, **kwargs):
        user = request.user.id
        params = request.query_params
        print(f"CODEGOST: {params.get('codegost', None)}")
        if params.get("codegost", None) != None:
            codeGost = params.get("codegost", None)
            print(f"CODEGOST_p: {codeGost}")
            regions = Region.objects.filter(codegost=codeGost)
            serializer = RegionSerializer(regions, many=True)
        else:
            regions = Region.objects
            serializer = RegionSerializer(regions, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class RegionDetailView(APIView):
    def get(self, request, *args, **kwargs):
        regions = tuple(Region.objects)

        # serializer = RegionSerializer(regions, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class RegionEmployeeView(APIView):
    def get(self, request, regionid, *args, **kwargs):
        employees = tuple(
            Employee.objects.filter(region_id=regionid)
            .annotate(
                post_title=F("employeepost__post__title"),
                # post_priority = F('employeepost__post__priority')
            )
            .order_by("employeepost__post__priority")
        )
        response = defaultdict(lambda: {"count": 0, "data": list()})
        for employee in employees:
            item = response[employee.post_title]
            # item['priority'] = employee.post_priority
            item["count"] += 1
            item["data"].append(EmployeeSerializer(employee).data)
        # print (response)
        return Response(response, status=status.HTTP_200_OK)


class RegionMunicipalityView(APIView):
    def get(self, request, regionid, *args, **kwargs):
        municipalities = tuple(Municipality.objects.filter(region_id=regionid))
        serializer = MunicipalitySerializer(municipalities, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class RegionEduInstOriginView(APIView):
    def get(self, request, regionid, *args, **kwargs):
        eduinstitutions = tuple(
            EduInstitution.objects.filter(sign=0)
            .annotate(
                regionid=F("municipality__region__id"),
                municipality_title=F("municipality__title"),
                # municipality_id = F('municipality__id'),
                region=F("municipality__region__title"),
                # type_ = F('type')
            )
            .filter(regionid=regionid)
        )
        # serialized_schools = SchoolSerializer(schools, many=True)
        eduinstitutions_c = defaultdict(
            lambda: {
                "schools": dict({"count": 0, "schools": list()}),
                "spo": dict({"count": 0, "spo": list()}),
            }
        )
        # eduinstitutions_c = defaultdict(lambda: {"count":0, "schools":dict({"count":0, "schools":list()}), "spo":dict({"count":0, "spo":list()})})
        for eduinst in eduinstitutions:
            item = eduinstitutions_c[eduinst.municipality_title]
            # item['data'].append(SchoolSerializer(eduinst).data)
            if eduinst.type == 0:
                item["schools"]["count"] += 1
                item["schools"]["schools"].append(SchoolSerializer(eduinst).data)
            else:
                item["spo"]["count"] += 1
                item["spo"]["spo"].append(SchoolSerializer(eduinst).data)
        # response = defaultdict(lambda: {"count":0, "data":list()})
        # for municipalities in eduinstitutions_c:
        #     item = response[]
        # print(eduinstitutions_c.values())
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


class MunicipalityEduInstOriginView(APIView):
    def get(self, request, regionid, municipalityid, *args, **kwargs):
        municipality = Municipality.objects.filter(id=municipalityid)
        if municipality[0].region.id != regionid:
            return Response(
                "Указанный муниципалитет не входит в состав выбранного региона",
                status=status.HTTP_400_BAD_REQUEST,
            )
        # if municipalityid not in municipalities.:
        #     return Response(status=status.HTTP_400_BAD_REQUEST)
        eduinstitutions = tuple(
            EduInstitution.objects.filter(municipality_id=municipalityid)
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
            # if regionid!=eduinst.regionid:
            #     return Response("Указанный муниципалитет не входит в состав выбранного региона", status=status.HTTP_400_BAD_REQUEST)
            item = response[eduinst.municipality.id]
            item["count"] += 1
            # item['data'].append(SchoolSerializer(eduinst).data)
            if eduinst.type == 0:
                item["schools"]["count"] += 1
                item["schools"]["schools"].append(SchoolSerializer(eduinst).data)
            else:
                item["spo"]["count"] += 1
                item["spo"]["spo"].append(SchoolSerializer(eduinst).data)

        return Response(response, status=status.HTTP_200_OK)
