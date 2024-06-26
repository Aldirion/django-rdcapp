# Generated by Django 5.0.1 on 2024-04-03 05:04

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rdcapp_api', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employee',
            name='login',
            field=models.CharField(default=models.CharField()),
        ),
        migrations.AlterField(
            model_name='employee',
            name='tablenumber',
            field=models.CharField(),
        ),
        migrations.AlterField(
            model_name='post',
            name='department',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='rdcapp_api.department'),
        ),
        migrations.AlterField(
            model_name='post',
            name='priority',
            field=models.IntegerField(default=0, null=True),
        ),
        migrations.CreateModel(
            name='PostDepartment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('department', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='rdcapp_api.department')),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='rdcapp_api.post')),
            ],
        ),
    ]
