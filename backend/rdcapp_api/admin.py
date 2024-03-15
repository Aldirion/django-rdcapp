from django.contrib import admin
from .models import *

# Register your models here.

admin.site.register(District)
admin.site.register(Region)
admin.site.register(Municipality)
admin.site.register(Employee)
admin.site.register(Post)
admin.site.register(Management)
admin.site.register(Department)
admin.site.register(AuthGroup)
admin.site.register(AuthGroupPermissions)
admin.site.register(AuthPermission)
admin.site.register(AuthUser)
admin.site.register(AuthUserGroups)
admin.site.register(AuthUserUserPermissions)
admin.site.register(DjangoAdminLog)
admin.site.register(DjangoContentType)
admin.site.register(DjangoMigrations)
admin.site.register(DjangoSession)
