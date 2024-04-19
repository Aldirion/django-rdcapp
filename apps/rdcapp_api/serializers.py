from pyclbr import Class

# from numpy import source
from rest_framework import serializers
from django.db.models import Func, F, Value
from .models import *


class MunicipalitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Municipality
        fields = ("id", "title", "region")


class RegionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Region
        fields = "__all__"


class Counter:
    def __init__(self, val):
        self.val = val


class CounterSerializer(serializers.Serializer):
    val = serializers.IntegerField()


class IntSerializer(serializers.Serializer):
    val = serializers.IntegerField()


class RegionDetailSerializer(serializers.ModelSerializer):
    computed = serializers.SerializerMethodField()

    class Meta:
        model = Region
        fields = "__all__"

    def get_computed(self, obj):
        colors = [
            "F85151",
            "F87351",
            "F88651",
            "F89C51",
            "F8BB51",
            "F8DC51",
            "E5F851",
            "CCF851",
            "BEF851",
            "51F85F",
            "51F897",
        ]
        eduinstitutions = tuple(
            EduInstitution.objects.filter(sign=0)
            .annotate(
                regionid=F("municipality__region__id"),
                count_school=F("municipality__region__count_school"),
                count_spo=F("municipality__region__count_spo"),
            )
            .filter(regionid=obj.id)
        )
        # print(eduinstitutions[0].count_school)
        data = dict({"comp_count_spo": 0, "comp_count_school": 0, "color": 0})
        for eduinst in eduinstitutions:
            if eduinst.type == 0:
                data["comp_count_school"] += 1
            else:
                data["comp_count_spo"] += 1
        val = sum(data.values())
        data["color"] = colors[
            int((val / (int(obj.count_school) + int(obj.count_spo))) * 100 // 10)
        ]
        return data


class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = (
            "id",
            "firstname",
            "lastname",
            "patronymic",
            "email",
            "quote",
            "region_id",
        )


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = "__all__"


class UPDEmployeeSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Employee
        fields = "__all__"


class EduInstTypeSerializer(serializers.ModelSerializer):
    type = serializers.CharField(source="get_type_display")

    class Meta:
        model = EduInstitution
        fields = ("type",)


class SchoolSerializer(serializers.ModelSerializer):
    type = serializers.CharField(source="get_type_display")

    class Meta:
        model = EduInstitution
        fields = (
            "id",
            "type",
            "title",
            "inn",
            "kpp",
            "contingent",
        )
