# Generated by Django 4.2.2 on 2024-07-16 13:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0024_remove_deployedunits_persons_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='deployedunits',
            old_name='deployement_name',
            new_name='deployment_name',
        ),
    ]
