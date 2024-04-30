from django.contrib import admin
from import_export import resources
from import_export.admin import ImportExportActionModelAdmin

from .models import (
    District,
    EduInstitution,
    # EduInstitutionEmployee,
    EduSpace,
    Employee,
    EmployeePost,
    Municipality,
    Post,
    Rc,
    Region,
    Subdivision,
)

# from import_export import fields
# from import_export.widgets import ForeignKeyWidget


# District Admin Panel Import Export
class DistrictResource(resources.ModelResource):
    # region = fields.Field(column_name = 'region', attribute = region, widget=ForeignKeyWidget(Region, 'title'))
    class Meta:
        model = District


class DistrictAdmin(ImportExportActionModelAdmin):
    resource_class = DistrictResource
    list_display = [field.name for field in District._meta.fields if field.name != "id"]
    # inlines = [DistrictImageInline]


# Region Admin Panel Import Export
class RegionResource(resources.ModelResource):
    # district = fields.Field(column_name = 'district', attribute = 'district', widget=ForeignKeyWidget(District, 'id'))
    class Meta:
        model = Region


class RegionAdmin(ImportExportActionModelAdmin):
    resource_class = RegionResource
    list_display = ["title", "count_spo", "count_school"]
    list_filter = ["id"]
    # inlines = [DistrictImageInline]


# Resource Center Admin Panel Import Export
class RCResource(resources.ModelResource):
    class Meta:
        model = Rc


class RCAdmin(ImportExportActionModelAdmin):
    resource_class = RCResource
    list_display = ["region", "email", "address"]
    list_filter = ["id"]


# Municipality Admin Panel Import Expot
class MunicipalityResource(resources.ModelResource):
    # district = fields.Field(column_name = 'district', attribute = 'district', widget=ForeignKeyWidget(District, 'id'))
    class Meta:
        model = Municipality


class MunicipalityAdmin(ImportExportActionModelAdmin):
    resource_class = MunicipalityResource
    list_display = ("title", "region_title", "count_school", "count_spo")
    list_filter = [
        ("region", admin.RelatedFieldListFilter),
    ]

    def region_title(self, obj):
        return obj.region.title

    # inlines = [DistrictImageInline]


# SubDivision Admin Panel Import Export
class SuvdivisionResource(resources.ModelResource):
    # district = fields.Field(column_name = 'district', attribute = 'district', widget=ForeignKeyWidget(District, 'id'))
    class Meta:
        model = Subdivision


class SubdivisionAdmin(ImportExportActionModelAdmin):
    resource_class = SuvdivisionResource
    list_display = [
        field.name for field in Subdivision._meta.fields if field.name != "id"
    ]
    list_filter = [
        # ("region", admin.RelatedFieldListFilter),
        "id",
        ("parent", admin.RelatedFieldListFilter),
    ]
    # inlines = [DistrictImageInline]


# Post Admin Panel Import Export
class PostResource(resources.ModelResource):
    # district = fields.Field(column_name = 'district', attribute = 'district', widget=ForeignKeyWidget(District, 'id'))
    class Meta:
        model = Post


class PostAdmin(ImportExportActionModelAdmin):
    resource_class = PostResource
    # list_display = [field.name for field in Subdivision._meta.fields if field.name != "id"]
    # list_filter = [
    #     # ("region", admin.RelatedFieldListFilter),
    #     "id"
    #     ]
    # inlines = [DistrictImageInline]


# Employee Admin Panel
class EmployeeAdmin(admin.ModelAdmin):
    raw_id_fields = ["user"]
    list_display = ["id", "get_full_name", "user", "region_id"]
    list_filter = ["region"]
    ordered_fields = ["get_full_name"]

    # search_fields=["region", "get_full_name"]
    class Meta:
        model = Employee


# EduInstitution Admin Panel Import Export
class EduInstResource(resources.ModelResource):
    class Meta:
        model = EduInstitution


class EduInstAdmin(ImportExportActionModelAdmin):
    readonly_fields = ["municipality"]

    resource_class = EduInstResource
    list_display = (
        "id",
        "type",
        "sign",
        "municipality",
        "municipality_region_title",
        "is_adviser_post_introduced",
        "inn",
        "kpp",
        "title",
        "eduenv",
    )
    list_filter = ["sign", "is_adviser_post_introduced"]
    search_fields = [
        "title",
        "inn",
    ]

    def municipality_region_title(self, obj):
        return obj.municipality.region.title

    def get_dynamic_info(self):
        # if self.fields.__getstate__('type') == 1:
        pass

    def change_view(self, request, object_id, form_url="", extra_context=None):
        extra_context = extra_context or {}
        extra_context["osm_data"] = self.get_dynamic_info()
        return super(EduInstAdmin, self).change_view(
            request,
            object_id,
            form_url,
            extra_context=extra_context,
        )


# Register models admin panel.
admin.site.register(District, DistrictAdmin)
admin.site.register(Region, RegionAdmin)
admin.site.register(Municipality, MunicipalityAdmin)
admin.site.register(Employee, EmployeeAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(Subdivision, SubdivisionAdmin)
admin.site.register(EmployeePost)
admin.site.register(EduInstitution, EduInstAdmin)
admin.site.register(Rc, RCAdmin)
admin.site.register(EduSpace)
