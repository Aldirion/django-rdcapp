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


from rdcapp_api.serializers import *

#Отображение регионов/региона
class RegionView(APIView):
    def get(self, request, *args, **kwargs):
        user = request.user.id
        params = request.query_params
        print(f"CODEGOST: {params.get("codegost", None)}")
        if (params.get("codegost", None) != None):
            codeGost = params.get("codegost", None)
            print(f"CODEGOST_p: {codeGost}")
            regions = Region.objects.filter(codegost=codeGost)
            serializer = RegionSerializer(regions, many=True)
        else: 
            regions = Region.objects
            serializer = RegionSerializer(regions, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class RegionEmployeeView(APIView):
    def get(self, request, regionid, *args, **kwargs):
        employees = tuple(Employee.objects.filter(region_id=regionid).annotate(
            post_title = F('employeepost__post__title'),
            # post_priority = F('employeepost__post__priority')
        ).order_by('employeepost__post__priority'))
        response = defaultdict(lambda: {"count":0, "data": list()})
        for employee in employees:
            item = response[employee.post_title]
            # item['priority'] = employee.post_priority
            item['count'] += 1
            item['data'].append(EmployeeSerializer(employee).data)
        # print (response)
        return Response(response, status=status.HTTP_200_OK)
    
class RegionMunicipalityView(APIView):
    def get(self,request, regionid, *args, **kwargs):
        municipalities = tuple (Municipality.objects.filter(region_id=regionid))
        serializer = MunicipalitySerializer(municipalities, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
