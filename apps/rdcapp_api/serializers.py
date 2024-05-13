# from numpy import source
from django.contrib.auth.models import User
from rest_framework import serializers

from apps.rdcapp_api.models import (
    # EmployeePost,
    EduInstitution,
    EduSpace,
    Employee,
    Municipality,
    Post,
    Region,
)

from .common.validators.edu_space_validator import EduSpaceType


# Region Serializers
class RegionSerializer(serializers.ModelSerializer):
    # Annotated Fields
    comp_count_spo = serializers.IntegerField()
    comp_count_school = serializers.IntegerField()
    comp_indicator_count_eduinst = serializers.SerializerMethodField()
    rrc_address = serializers.CharField()
    rrc_email = serializers.EmailField()

    class Meta:
        model = Region
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
            # # "comp_count_museum",
            "rrc_address",
            "rrc_email",
            # Method Fields
            "comp_indicator_count_eduinst",
        )

    def get_comp_indicator_count_eduinst(self, obj):
        # color=(255-255*val//100, 255*val//100, 0)
        if obj.count_school is not None and obj.count_spo is not None:
            if obj.comp_count_school is not None and obj.comp_count_spo is not None:
                return round(
                    (obj.comp_count_spo + obj.comp_count_school)
                    / (obj.count_spo + obj.count_school)
                    * 100
                )
            else:
                return 0
        else:
            return 100


class Counter:
    def __init__(self, val):
        self.val = val


class CounterSerializer(serializers.Serializer):
    val = serializers.IntegerField()


class IntSerializer(serializers.Serializer):
    val = serializers.IntegerField()


# Municipality Serializers
class MunicipalitySerializer(serializers.ModelSerializer):
    comp_count_spo = serializers.IntegerField()
    comp_count_school = serializers.IntegerField()
    comp_indicator_count_eduinst = serializers.SerializerMethodField()

    class Meta:
        model = Municipality
        fields: tuple[str, ...] = (
            # Model Fields
            "id",
            "title",
            "region",
            "oktmo5",
            "codegost",
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


# Employee Serializers
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "username")


class EmployeeRegionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Region
        fields = (
            "id",
            "title",
        )


class EmployeePostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ("title", "subdivision")


class EmployeeProfilePostSerializer(serializers.Serializer):
    post_title = serializers.CharField()
    subdivision_title = serializers.CharField()
    tab_number = serializers.CharField()


class EmployeeEduinstSerializer(serializers.Serializer):
    edu_inst_title = serializers.CharField()


class EmployeeProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(many=False, required=True)
    region = EmployeeRegionSerializer(many=False, required=True)
    posts = serializers.ListSerializer(child=EmployeeProfilePostSerializer())
    eduinstitutions = serializers.ListSerializer(child=EmployeeEduinstSerializer())

    class Meta:
        model = Employee
        fields = (
            "id",
            "firstname",
            "lastname",
            "patronymic",
            "email",
            "bio",
            "quote",
            "phone_number",
            "telegram_username",
            "avatar",
            "region",
            "posts",
            "eduinstitutions",
            "user",
        )
        read_only_fields = (
            "user",
            "firstname",
            "lastname",
            "patronymic",
            "region",
            "posts",
            "eduinstitutions",
        )


class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
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
            "avatar",
            "user"
        )


# EduInstitution Serializers
class EduInstTypeSerializer(serializers.ModelSerializer):
    type = serializers.CharField(source="get_type_display")
    sign = serializers.CharField(source="get_sign_display")

    class Meta:
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
        model = EduInstitution
        fields: tuple[str, ...] = (
            # Model Fields
            "id",
            "sign",
            "title",
            "contingent",
            "address",
        )


class SchoolDetailSerializer(serializers.ModelSerializer):
    type = serializers.CharField(source="get_type_display")
    sign = serializers.CharField(source="get_sign_display")

    class Meta:
        model = EduInstitution
        fields: tuple[str, ...] = (
            # Model Fields
            "id",
            "sign",
            "type",
            "title",
            "inn",
            "kpp",
            "contingent",
            "address",
            "eduenv",
        )


# TODO: Implement save method for Education space
class EduSpaceSerializer(serializers.ModelSerializer):
    class Meta:
        # model = models.EduSpace
        model = EduSpace

    def save(self):
        # edu_space_type = self.validated_data["edu_space_type"]
        # serializer = models.EduSpaceType.get_serializer(edu_space_type)
        # serializer = EduSpaceType.get_serializer(edu_space_type)
        # super()
        pass
