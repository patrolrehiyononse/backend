# Generated by Django 4.2.2 on 2024-07-09 06:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0018_deployedunits'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='deployedunits',
            name='starting_point',
        ),
    ]
