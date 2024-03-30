from django.shortcuts import render
from django.views.generic import ListView

from django.contrib.auth.models import Group, User
from rest_framework import permissions, viewsets, status
from rest_framework.views import APIView
from rest_framework.response import Response


from rdcapp_api.serializers import *

class EmployeeViewSet(viewsets.ModelViewSet):
    queryset=Employee.objects.all().order_by('joindate')
    serializer_class = EmployeeSerializer
    # permission_classes = [permissions.IsAuthenticated]
class MunicipalityViewSet(viewsets.ModelViewSet):
    queryset=Municipality.objects.all().order_by('title')
    serializer_class = MunicipalitySerializer
    # permission_classes = [permissions.IsAuthenticated]

class RegionViewSet(viewsets.ModelViewSet):
    queryset=Region.objects.all().order_by('title')
    serializer_class = RegionSerializer
    # permission_classes = [permissions.IsAuthenticated]

class RegionView(APIView):
    def get(self, request, *args, **kwargs):
        user=request.user.id
        params=request.query_params
        print(f"CODEGOST: {params.get("codegost", None)}")
        if (params.get("codegost", None) != None):
            codeGost = params.get("codegost", None)
            print(f"CODEGOST_p: {codeGost}")
            regions=Region.objects.all().filter(codegost=codeGost)
            serializer=RegionSerializer(regions, many=True)
        else: 
            regions=Region.objects.all()
            serializer=RegionSerializer(regions, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class EmployeeView(APIView):
    def get(self, request, *args, **kwargs):
        user=request.user.id
        params=request.query_params
        # print (params.items.length)
        if params.get("id", None) != None:
            employees=Employee.objects.all().filter(id=params.get("id"))
        elif params.get("regionid", None) != None:
            if params.get("postid", None) != None:
                employees=Employee.objects.all().filter(regionid=params.get("regionid"), postid=params.get("postid"))
            else:
                employees=Employee.objects.all().filter(regionid=params.get("regionid"))
        elif params.get("postid", None) != None and params.get("regionid", None) == None:
            employees=Employee.objects.all().filter(postid=params.get("postid"))
        else:
            employees=Employee.objects.all()
        serializer=EmployeeSerializer(employees, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
# Create your views here.
class RegionEmployeeView(APIView):
    def get(self, request, regionid, *args, **kwargs):
        #Получение всех сотрудников в регионе
        queryset=Employee.objects.all().filter(regionid=regionid)
        #Получение всех должностей
        postset=Post.objects.all()
        posts=set()
        response_dict={}
        #Получение числа сотрудников в регионе
        response_dict.update({"total_count":len(queryset)})
        #Получение id всех должностей в регионе
        for employee in queryset:
            if employee.postid not in posts:
                posts.add(employee.postid)
        #Формирование структуры словарь словарей с массивом словарей
        for post in posts:
            employee_by_post_list=[]
            for employee in queryset:
                if employee.postid==post:
                    employee_by_post_list.append(employee)
            response_dict.update({
                postset.get(id=post).title:{"count":len(employee_by_post_list), "data":EmployeeSerializer(employee_by_post_list, many=True).data}
                })
        #Отправка ответа
        return Response(response_dict, status=status.HTTP_200_OK)

    

