# Generated by Django 4.2.2 on 2024-04-20 14:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0005_geofencing_alter_person_person_rank_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='geofencing',
            name='center',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
