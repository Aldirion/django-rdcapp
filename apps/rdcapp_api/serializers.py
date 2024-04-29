from numpy import source
from rest_framework import serializers

from apps.rdcapp_api.models import (Region, Municipality, Employee, Post, EmployeePost, EduInstitution,)
# from apps.rdcapp_api import models



class RegionSerializer(serializers.ModelSerializer):
    # Annotated Fields
    comp_count_spo = serializers.IntegerField()
    comp_count_school = serializers.IntegerField()
    comp_indicator_count_eduinst = serializers.SerializerMethodField()
    rrc_address = serializers.CharField()
    rrc_email = serializers.EmailField()

    class Meta:
        model = Region
        # model = models.Region
        fields: tuple[str, ...] = (
            # Model Fields
            "id",
            "title",
            "district",
            "codegibdd",
            "codegost",
            "population",
            "count_school",
            "count_spo",
            # Annotated Fields
            "comp_count_spo",
            "comp_count_school",
            "rrc_address",
            "rrc_email",
            # Method Fields
            "comp_indicator_count_eduinst",
        )

    def get_comp_indicator_count_eduinst(self, obj):
        # color=(255-255*val//100, 255*val//100, 0)
        return round(
            (obj.comp_count_spo + obj.comp_count_school)
            / (obj.count_spo + obj.count_school)
            * 100
        )


class Counter:
    def __init__(self, val):
        self.val = val


class CounterSerializer(serializers.Serializer):
    val = serializers.IntegerField()


class IntSerializer(serializers.Serializer):
    val = serializers.IntegerField()

class MunicipalitySerializer(serializers.ModelSerializer):
    comp_count_spo = serializers.IntegerField()
    comp_count_school = serializers.IntegerField()
    comp_indicator_count_eduinst = serializers.SerializerMethodField()

    class Meta:
        model = Municipality
        # model = models.Municipality
        fields: tuple[str, ...] = (
            # Model Fields
            "id",
            "title",
            "region",
            "oktmo5",
            "count_school",
            "count_spo",
            # Annotated Fields
            "comp_count_school",
            "comp_count_spo",
            # Method Fields
            "comp_indicator_count_eduinst",
        )

    def get_comp_indicator_count_eduinst(self, obj):
        if obj.count_school is not None and obj.count_spo is not None:
            return round(
                (obj.comp_count_spo + obj.comp_count_school)
                / (obj.count_spo + obj.count_school)
                * 100
            )
        else:
            return 100

class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        # model = models.Employee
        model = Employee
        fields: tuple[str, ...] = (
            # Model Fields
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
        # model = models.Post
        model = Post

        fields = "__all__"  # TODO: Do not use __all__


class UPDEmployeeSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        # model = models.Employee
        model = Employee
        fields = "__all__"  # TODO: Do not use __all__


class EduInstTypeSerializer(serializers.ModelSerializer):
    type = serializers.CharField(source="get_type_display")
    sign = serializers.CharField(source="get_sign_display")

    class Meta:
        # model = models.EduInstitution
        model = EduInstitution
        fields: tuple[str, ...] = (
            # Model Fields
            "type",
            "sign",
        )


class SchoolSerializer(serializers.ModelSerializer):
    # type = serializers.CharField(source="get_type_display")
    sign = serializers.CharField(source="get_sign_display")

    class Meta:
        # model = models.EduInstitution
        model = EduInstitution
        fields: tuple[str, ...] = (
            # Model Fields
            "id",
            "sign",
            # "type",
            "title",
            # "inn",
            # "kpp",
            "contingent",
            "address",
        )


#TODO Решить проблему циплического импорта

# class SchoolMuseumSerializer(serializers.Serializer):
#     pass


# class EduSpaceSerializer(serializers.ModelSerializer):
#     class Meta:
#         # model = models.EduSpace
#         model = EduSpace

#     def save(self):
#         edu_space_type = self.validated_data["edu_space_type"]
#         # serializer = models.EduSpaceType.get_serializer(edu_space_type)
#         serializer = EduSpaceType.get_serializer(edu_space_type)
#         # super()