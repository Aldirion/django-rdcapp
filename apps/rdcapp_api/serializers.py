from numpy import source
from rest_framework import serializers

from . import models


class MunicipalitySerializer(serializers.ModelSerializer):
    comp_count_spo = serializers.IntegerField()
    comp_count_school = serializers.IntegerField()
    comp_indicator_count_eduinst = serializers.SerializerMethodField()

    class Meta:
        model = models.Municipality
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
        if obj.count_school != None and obj.count_spo != None:
            return round(
                (obj.comp_count_spo + obj.comp_count_school)
                / (obj.count_spo + obj.count_school)
                * 100
            )
        else:
            return 100


class RegionSerializer(serializers.ModelSerializer):
    # Annotated Fields
    comp_count_spo = serializers.IntegerField()
    comp_count_school = serializers.IntegerField()
    comp_indicator_count_eduinst = serializers.SerializerMethodField()
    rrc_address = serializers.CharField()
    rrc_email = serializers.EmailField()

    class Meta:
        model = models.Region
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


class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Employee
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
        model = models.Post
        fields = "__all__"  # TODO: Do not use __all__


class UPDEmployeeSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.Employee
        fields = "__all__"  # TODO: Do not use __all__


class EduInstTypeSerializer(serializers.ModelSerializer):
    type = serializers.CharField(source="get_type_display")
    sign = serializers.CharField(source="get_sign_display")

    class Meta:
        model = models.EduInstitution
        fields: tuple[str, ...] = (
            # Model Fields
            "type",
            "sign",
        )


class SchoolSerializer(serializers.ModelSerializer):
    # type = serializers.CharField(source="get_type_display")
    sign = serializers.CharField(source="get_sign_display")

    class Meta:
        model = models.EduInstitution
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
