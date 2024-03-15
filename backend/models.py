# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Department(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    title = models.CharField(db_column='Title', blank=True, null=True)  # Field name made lowercase.
    managmentid = models.IntegerField(db_column='ManagmentID', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Department'


class District(models.Model):
    districtid = models.AutoField(db_column='DistrictID', primary_key=True)  # Field name made lowercase.
    title = models.CharField(db_column='Title', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'District'


class Eduinstsign(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    title = models.TextField(db_column='Title', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'EduInstSign'


class Eduinsttype(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    title = models.TextField(db_column='Title', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'EduInstType'


class Eduinstitution(models.Model):
    id = models.UUIDField(db_column='ID', primary_key=True)  # Field name made lowercase.
    typeid = models.IntegerField(db_column='TypeID')  # Field name made lowercase.
    signid = models.IntegerField(db_column='SignID')  # Field name made lowercase.
    municipalityid = models.UUIDField(db_column='MunicipalityID')  # Field name made lowercase.
    regionid = models.IntegerField(db_column='RegionID')  # Field name made lowercase.
    isadviserpostintroduced = models.BooleanField(db_column='IsAdviserPostIntroduced')  # Field name made lowercase.
    inn = models.TextField(db_column='INN')  # Field name made lowercase.
    address = models.TextField(db_column='Address', blank=True, null=True)  # Field name made lowercase.
    contingent = models.IntegerField(db_column='Contingent', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'EduInstitution'


class Employee(models.Model):
    id = models.UUIDField(db_column='ID', primary_key=True)  # Field name made lowercase.
    created = models.DateTimeField(db_column='Created', blank=True, null=True)  # Field name made lowercase.
    joindate = models.DateField(db_column='JoinDate', blank=True, null=True)  # Field name made lowercase.
    isactive = models.BooleanField(db_column='IsActive')  # Field name made lowercase.
    fireddate = models.DateField(db_column='FiredDate', blank=True, null=True)  # Field name made lowercase.
    login = models.CharField(db_column='Login')  # Field name made lowercase.
    firstname = models.CharField(db_column='FirstName')  # Field name made lowercase.
    lastname = models.CharField(db_column='LastName')  # Field name made lowercase.
    patronymic = models.CharField(db_column='Patronymic', blank=True, null=True)  # Field name made lowercase.
    regionid = models.IntegerField(db_column='RegionID')  # Field name made lowercase.
    postid = models.IntegerField(db_column='PostID')  # Field name made lowercase.
    departmentid = models.IntegerField(db_column='DepartmentID', blank=True, null=True)  # Field name made lowercase.
    managmentid = models.IntegerField(db_column='ManagmentID')  # Field name made lowercase.
    tablenumber = models.CharField(db_column='TableNumber')  # Field name made lowercase.
    dateofbirth = models.DateField(db_column='DateOfBirth', blank=True, null=True)  # Field name made lowercase.
    email = models.CharField(db_column='Email', blank=True, null=True)  # Field name made lowercase.
    phone = models.CharField(db_column='Phone', blank=True, null=True)  # Field name made lowercase.
    telegramnik = models.CharField(db_column='TelegramNik', blank=True, null=True)  # Field name made lowercase.
    quote = models.TextField(db_column='Quote', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Employee'


class Management(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    title = models.CharField(db_column='Title', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Management'


class Municipality(models.Model):
    id = models.UUIDField(db_column='ID', primary_key=True)  # Field name made lowercase.
    title = models.TextField(db_column='Title')  # Field name made lowercase.
    regionid = models.IntegerField(db_column='RegionID')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Municipality'


class Post(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    post = models.CharField(db_column='Post', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Post'


class Rc(models.Model):
    id = models.UUIDField(db_column='ID', primary_key=True)  # Field name made lowercase.
    regionid = models.IntegerField(db_column='RegionID')  # Field name made lowercase.
    address = models.TextField(db_column='Address', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    baseorganization = models.TextField(db_column='BaseOrganization', blank=True, null=True)  # Field name made lowercase.
    email = models.TextField(db_column='Email', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'RC'


class Region(models.Model):
    regionid = models.AutoField(db_column='RegionID', primary_key=True)  # Field name made lowercase.
    title = models.CharField(db_column='Title', blank=True, null=True)  # Field name made lowercase.
    dsid = models.ForeignKey(District, models.DO_NOTHING, db_column='DSID', blank=True, null=True)  # Field name made lowercase.
    codegibdd = models.CharField(db_column='CodeGIBDD', blank=True, null=True)  # Field name made lowercase.
    codegost = models.CharField(db_column='CodeGOST', blank=True, null=True)  # Field name made lowercase.
    capital = models.TextField(db_column='Capital', blank=True, null=True)  # Field name made lowercase.
    population = models.IntegerField(db_column='Population', blank=True, null=True)  # Field name made lowercase.
    regionheadid = models.UUIDField(db_column='RegionHeadID', blank=True, null=True)  # Field name made lowercase.
    rcid = models.IntegerField(db_column='RCID', blank=True, null=True)  # Field name made lowercase.
    indicator = models.SmallIntegerField(db_column='Indicator', blank=True, null=True)  # Field name made lowercase.
    countschool = models.IntegerField(db_column='CountSchool', blank=True, null=True)  # Field name made lowercase.
    countspo = models.IntegerField(db_column='CountSPO', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Region'


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.BooleanField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.BooleanField()
    is_active = models.BooleanField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.SmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    id = models.BigAutoField(primary_key=True)
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'
