# Generated by Django 5.0.1 on 2024-04-04 07:43

import django.core.validators
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='District',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField()),
            ],
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField()),
                ('priority', models.IntegerField(default=0, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Employee',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField()),
                ('firstname', models.CharField()),
                ('lastname', models.CharField()),
                ('patronymic', models.CharField(blank=True, null=True)),
                ('dateofbirth', models.DateField(blank=True, null=True)),
                ('sex', models.IntegerField(choices=[(0, 'Мужской'), (1, 'Женский')])),
                ('snils', models.CharField(blank=True, validators=[django.core.validators.RegexValidator(regex='^\\d{3}-\\d{3}-\\d{3} \\d{2}$')])),
                ('email', models.EmailField(blank=True, max_length=254, null=True)),
                ('phone_number', models.CharField(blank=True, max_length=17, null=True, validators=[django.core.validators.RegexValidator(regex='^((8|\\+7)[\\- ]?)?(\\(?\\d{3}\\)?[\\- ]?)?[\\d\\- ]{7,10}$')])),
                ('telegram_username', models.CharField(blank=True, null=True, validators=[django.core.validators.RegexValidator(regex='?:@|(?:(?:(?:https?://)?t(?:elegram)?)\\.me\\/))(\\w{4,})$')])),
                ('quote', models.CharField(blank=True, null=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='EmployeePost',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tab_number', models.CharField()),
                ('rate', models.FloatField()),
                ('employment', models.IntegerField(choices=[(0, 'Основное место работы'), (1, 'Внутреннее совмещение'), (2, 'Внешнее совмещение')])),
                ('join_date', models.DateField(blank=True, null=True)),
                ('fired_date', models.DateField(blank=True, null=True)),
                ('employee', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='rdcapp_api.employee')),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='rdcapp_api.post')),
            ],
        ),
        migrations.CreateModel(
            name='Region',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField()),
                ('codegibdd', models.CharField()),
                ('codegost', models.CharField()),
                ('capital', models.CharField(blank=True, null=True)),
                ('population', models.IntegerField(blank=True, null=True)),
                ('count_school', models.IntegerField(blank=True, null=True)),
                ('count_spo', models.IntegerField(blank=True, null=True)),
                ('district', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='rdcapp_api.district')),
            ],
        ),
        migrations.CreateModel(
            name='Rc',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('address', models.CharField(blank=True, null=True)),
                ('base_organization', models.CharField(blank=True, null=True)),
                ('email', models.EmailField(blank=True, max_length=254, null=True)),
                ('region', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='rdcapp_api.region')),
            ],
        ),
        migrations.CreateModel(
            name='Municipality',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField()),
                ('count_school', models.IntegerField(blank=True, null=True)),
                ('count_spo', models.IntegerField(blank=True, null=True)),
                ('region', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='rdcapp_api.region')),
            ],
        ),
        migrations.AddField(
            model_name='employee',
            name='region',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='rdcapp_api.region'),
        ),
        migrations.CreateModel(
            name='EduInstitution',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.IntegerField(choices=[(0, 'Школа'), (1, 'СПО')])),
                ('sign', models.IntegerField(choices=[(0, 'Головное учреждение'), (1, 'Филиал'), (2, 'Представительство'), (3, 'Обособленное структурное подразделение')], default=0)),
                ('is_adviser_post_introduced', models.BooleanField()),
                ('inn', models.CharField(max_length=10, validators=[django.core.validators.MinLengthValidator(10)])),
                ('kpp', models.CharField(max_length=9, validators=[django.core.validators.MinLengthValidator(9)])),
                ('title', models.CharField()),
                ('address', models.CharField(blank=True, null=True)),
                ('contingent', models.IntegerField(blank=True, null=True)),
                ('municipality', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='rdcapp_api.municipality')),
                ('region', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='rdcapp_api.region')),
            ],
        ),
        migrations.CreateModel(
            name='Subdivision',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField()),
                ('parent', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='rdcapp_api.subdivision')),
            ],
        ),
        migrations.AddField(
            model_name='post',
            name='subdivision',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='rdcapp_api.subdivision'),
        ),
    ]
