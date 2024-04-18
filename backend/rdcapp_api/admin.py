from django.contrib import admin
from .models import *

from import_export.admin import ImportExportActionModelAdmin
from import_export import resources
from import_export import fields
from import_export.widgets import ForeignKeyWidget


class DistrictResource(resources.ModelResource):
    # region = fields.Field(column_name = 'region', attribute = region, widget=ForeignKeyWidget(Region, 'title'))
    class Meta:
        model = District


class DistrictAdmin(ImportExportActionModelAdmin):
    resource_class = DistrictResource
    list_display = [field.name for field in District._meta.fields if field.name != "id"]
    # inlines = [DistrictImageInline]


class RegionResource(resources.ModelResource):
    # district = fields.Field(column_name = 'district', attribute = 'district', widget=ForeignKeyWidget(District, 'id'))
    class Meta:
        model = Region


class RegionAdmin(ImportExportActionModelAdmin):
    resource_class = RegionResource
    list_display = [field.name for field in District._meta.fields if field.name != "id"]
    list_filter = ["id"]
    # inlines = [DistrictImageInline]


class MunicipalityResource(resources.ModelResource):
    # district = fields.Field(column_name = 'district', attribute = 'district', widget=ForeignKeyWidget(District, 'id'))
    class Meta:
        model = Municipality


class MunicipalityAdmin(ImportExportActionModelAdmin):
    resource_class = MunicipalityResource
    list_display = [field.name for field in District._meta.fields if field.name != "id"]
    list_filter = [
        ("region", admin.RelatedFieldListFilter),
    ]
    # inlines = [DistrictImageInline]


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


class EmployeeAdmin(admin.ModelAdmin):
    raw_id_fields = ["user"]

    class Meta:
        model = Employee


# Register your models here.

admin.site.register(District, DistrictAdmin)
admin.site.register(Region, RegionAdmin)
admin.site.register(Municipality, MunicipalityAdmin)
admin.site.register(Employee, EmployeeAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(Subdivision, SubdivisionAdmin)
admin.site.register(EmployeePost)
# admin.site.register(User, UserAdmin)
