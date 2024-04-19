from django.db import models
from django.utils import timezone
from django.core.validators import RegexValidator, MinLengthValidator
from django.contrib.auth.models import User


# Модели региональной информации
class District(models.Model):
    title = models.CharField()

    def __str__(self):
        return self.title


class Region(models.Model):
    title = models.CharField()
    district = models.ForeignKey(District, on_delete=models.CASCADE)
    codegibdd = models.CharField()
    codegost = models.CharField()
    capital = models.CharField(blank=True, null=True)
    population = models.IntegerField(blank=True, null=True)
    count_school = models.IntegerField(blank=True, null=True)
    count_spo = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return f"{self.title}, {self.get_total_eduinst()}"
    def get_total_eduinst(self):
        total = self.count_school + self.count_spo
        return total


class Municipality(models.Model):
    title = models.CharField()
    region = models.ForeignKey(Region, on_delete=models.CASCADE)
    count_school = models.IntegerField(blank=True, null=True)
    count_spo = models.IntegerField(blank=True, null=True)
    oktmo5 = models.CharField(blank=True, null=True)

    def __str__(self):
        return f"{self.title}"


class Rc(models.Model):
    region = models.ForeignKey(Region, on_delete=models.CASCADE)
    address = models.CharField(blank=True, null=True)
    base_organization = models.CharField(blank=True, null=True)
    email = models.EmailField(blank=True, null=True)

    def __str__(self):
        return f"{self.region}| Адрес:{self.address}"


# Модели штатного расписания
# вс


class Subdivision(models.Model):
    title = models.CharField()
    parent = models.ForeignKey(
        "SubDivision", blank=True, null=True, on_delete=models.CASCADE
    )

    def __str__(self):
        return self.title


class Post(models.Model):
    title = models.CharField()
    priority = models.IntegerField(default=0, null=True)
    subdivision = models.ForeignKey(Subdivision, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.title} | {self.subdivision}"


# Модель сотрудника
class Employee(models.Model):
    SEX_CHOICES = ((0, "Мужской"), (1, "Женский"))
    created = models.DateTimeField(editable=False, auto_now_add=True)
    modified = models.DateTimeField(null=True, auto_now=True)
    firstname = models.CharField()
    lastname = models.CharField()
    patronymic = models.CharField(blank=True, null=True)
    dateofbirth = models.DateField(blank=True, null=True)
    sex = models.IntegerField(choices=SEX_CHOICES)
    snils_regex = RegexValidator(regex=r"^\d{3}-\d{3}-\d{3} \d{2}$")
    snils = models.CharField(validators=[snils_regex], blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    phone_regex = RegexValidator(
        regex=r"^((8|\+7)[\- ]?)?(\(?\d{3}\)?[\- ]?)?[\d\- ]{7,10}$"
    )
    phone_number = models.CharField(
        validators=[phone_regex], max_length=17, blank=True, null=True
    )
    telegram_regex = RegexValidator(
        regex=r"?:@|(?:(?:(?:https?://)?t(?:elegram)?)\.me\/))(\w{4,})$"
    )
    telegram_username = models.CharField(
        validators=[telegram_regex], blank=True, null=True
    )
    quote = models.CharField(blank=True, null=True)
    region = models.ForeignKey(Region, on_delete=models.CASCADE, blank=True, null=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def get_full_name(self):
        full_name = f"{self.lastname} {self.firstname} {self.patronymic}"
        return full_name

    def __str__(self):
        return f"{self.get_full_name()}"


class EmployeePost(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    tab_number = models.CharField()
    rate = models.FloatField()
    TYPE_EMPLOYMENT_CHOICES = (
        (0, "Основное место работы"),
        (1, "Внутреннее совмещение"),
        (2, "Внешнее совмещение"),
    )
    employment = models.IntegerField(choices=TYPE_EMPLOYMENT_CHOICES)
    join_date = models.DateField(blank=True, null=True)
    fired_date = models.DateField(blank=True, null=True)

    def __str__(self):
        return f"{self.employee} : {self.tab_number}"


# Модели образовательной организации
class EduInstitution(models.Model):
    TYPE_CHOICES = (
        (0, "Школа"),
        (1, "СПО"),
    )
    SIGN_CHOICES = (
        (0, "Головное учреждение"),
        (1, "Филиал"),
        (2, "Представительство"),
        (3, "Обособленное структурное подразделение"),
    )
    type = models.IntegerField(choices=TYPE_CHOICES)
    sign = models.IntegerField(choices=SIGN_CHOICES, default=0)
    municipality = models.ForeignKey(Municipality, on_delete=models.CASCADE)
    # region = models.ForeignKey(Region, on_delete=models.CASCADE)
    is_adviser_post_introduced = models.BooleanField()
    inn = models.CharField(max_length=10, validators=[MinLengthValidator(10)])
    kpp = models.CharField(max_length=9, validators=[MinLengthValidator(9)])
    title = models.CharField()
    address = models.CharField(blank=True, null=True)
    contingent = models.IntegerField(blank=True, null=True)
    eduenv = models.JSONField(blank=True, null=True)

    def __str__(self):
        return f"{self.title}"


class EduInstitutionEmployee(models.Model):
    edu_institution = models.ForeignKey(EduInstitution, on_delete=models.CASCADE)
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
