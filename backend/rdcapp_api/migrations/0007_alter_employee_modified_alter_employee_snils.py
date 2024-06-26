# Generated by Django 5.0.1 on 2024-04-13 11:41

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rdcapp_api', '0006_migrate_employee_data'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employee',
            name='modified',
            field=models.DateTimeField(auto_now=True, null=True),
        ),
        migrations.AlterField(
            model_name='employee',
            name='snils',
            field=models.CharField(blank=True, null=True, validators=[django.core.validators.RegexValidator(regex='^\\d{3}-\\d{3}-\\d{3} \\d{2}$')]),
        ),
    ]
