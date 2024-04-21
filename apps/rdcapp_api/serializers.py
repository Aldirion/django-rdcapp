from rest_framework import serializers

from . import models


class MunicipalitySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Municipality
        fields: tuple[str, ...] = (
            # Model Fields
            'id',
            'title',
            'region'
        )


class RegionSerializer(serializers.ModelSerializer):
    comp_count_spo = serializers.IntegerField()
    comp_count_school = serializers.IntegerField()

    class Meta:
        model = models.Region
        fields: tuple[str, ...] = (
            # Model Fields
            'id',
            'title',
            'district',
            'codegibdd',
            'codegost',
            'population',
            'count_school',
            'count_spo',
            # Annotated Fields
            'comp_count_spo',
            'comp_count_school',
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
            'id',
            'firstname',
            'lastname',
            'patronymic',
            'email',
            'quote',
            'region_id',
        )


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Post
        fields = '__all__' # TODO: Do not use __all__


class UPDEmployeeSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.Employee
        fields = '__all__' # TODO: Do not use __all__


class EduInstTypeSerializer(serializers.ModelSerializer):
    type = serializers.CharField(source='get_type_display')

    class Meta:
        model = models.EduInstitution
        fields: tuple[str, ...] = (
            # Model Fields
            'type',
        )


class SchoolSerializer(serializers.ModelSerializer):
    type = serializers.CharField(source='get_type_display')

    class Meta:
        model = models.EduInstitution
        fields: tuple[str, ...] = (
            # Model Fields
            'id',
            'type',
            'title',
            'inn',
            'kpp',
            'contingent',
        )
