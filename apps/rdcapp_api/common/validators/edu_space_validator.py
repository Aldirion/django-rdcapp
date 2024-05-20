from dataclasses import dataclass
import enum
from rest_framework import serializers


# TODO: Описать вложенные структуры показателей для каждой из активностей
# School education space serializers
class SchoolMuseumSerializer(serializers.Serializer):
    pass


class SchoolTheatreSerializer(serializers.Serializer):
    pass


class SchoolMediaCentreSerializer(serializers.Serializer):
    pass


class SchoolTouristicClubSerializer(serializers.Serializer):
    pass


class SchoolCinemaClubSerializer(serializers.Serializer):
    pass


class SchoolMilitaryClubSerializer(serializers.Serializer):
    pass


class SchoolSportClubSerializer(serializers.Serializer):
    pass


class SchoolVolunteersSquadSerializer(serializers.Serializer):
    pass


class SchoolLeadersSquadSerializer(serializers.Serializer):
    pass


class SchoolUIDSquadSerializer(serializers.Serializer):
    pass


class SchoolYoungRescuersSquadSerializer(serializers.Serializer):
    pass


# TODO: Описать вложенные структуры показателей для каждой из активностей
# SPO education space serializers


class EduInstitutionType(int, enum.Enum):
    SCHOOL = 0
    SPO = 1


@dataclass
class EduSpaceTypeItem:
    title: str
    key: str
    type_: EduInstitutionType
    serializer: serializers.Serializer

    # def __init__(self, title, key, type_, serializer):
    #     self.title = title
    #     self.key = key
    #     self.type_ = type_
    #     self.serializer = serializer


class EduSpaceType:
    items = (
        EduSpaceTypeItem(
            title="Музей",
            key="museum",
            type_=EduInstitutionType.SCHOOL,
            serializer=SchoolMuseumSerializer,
        ),
        EduSpaceTypeItem(
            title="Театр",
            key="theatre",
            type_=EduInstitutionType.SCHOOL,
            serializer=SchoolMuseumSerializer,
        ),
        EduSpaceTypeItem(
            title="Театр",
            key="theatre",
            type_=EduInstitutionType.SPO,
            serializer=SchoolMuseumSerializer,
        ),
    )

    @classmethod
    def choices(cls):
        return tuple(
            (
                f"{item.key}__{item.type_}",
                f"{item.title} (Школа)" if item.type_ == 0 else f"{item.title} (СПО)",
            )
            for item in cls.items
        )

    @classmethod
    def get_serializer(cls, edu_space_type):
        for item in cls.items:
            if f"{item.key}__{item.type_}" == f"{item.key}__{edu_space_type}":
                return item.serializer
        return None
