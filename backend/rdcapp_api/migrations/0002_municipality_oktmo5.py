# Generated by Django 5.0.1 on 2024-04-05 12:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rdcapp_api', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='municipality',
            name='oktmo5',
            field=models.CharField(blank=True, null=True),
        ),
    ]
