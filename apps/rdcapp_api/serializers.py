from pyclbr import Class

# from numpy import source
from rest_framework import serializers
from .models import *


class MunicipalitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Municipality
        fields = ("id", "title", "region")


class RegionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Region
        fields = "__all__"


class RegionDetailSerializer(serializers.Serializer):
    region = RegionSerializer
    computed_count_school = serializers.IntegerField()
    computed_count_spo = serializers.IntegerField()
    indicator = serializers.IntegerField()


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
