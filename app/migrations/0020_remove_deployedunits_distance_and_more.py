# Generated by Django 4.2.2 on 2024-07-15 01:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0019_remove_deployedunits_starting_point'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='deployedunits',
            name='distance',
        ),
        migrations.RemoveField(
            model_name='deployedunits',
            name='duration',
        ),
    ]
