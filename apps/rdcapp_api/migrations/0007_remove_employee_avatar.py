# Generated by Django 5.0.4 on 2024-05-03 10:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('rdcapp_api', '0006_alter_eduinstitution_managers_alter_employee_avatar_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='employee',
            name='avatar',
        ),
    ]