# Generated by Django 4.2.2 on 2024-05-15 10:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0008_alter_person_person_rank_alter_person_person_station_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='geofencing',
            name='name',
            field=models.CharField(blank=True, max_length=600, null=True),
        ),
    ]
