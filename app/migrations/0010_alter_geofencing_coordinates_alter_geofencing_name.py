# Generated by Django 4.2.2 on 2024-05-15 10:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0009_alter_geofencing_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='geofencing',
            name='coordinates',
            field=models.CharField(blank=True, max_length=600, null=True),
        ),
        migrations.AlterField(
            model_name='geofencing',
            name='name',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
