# Generated by Django 4.2.2 on 2024-08-27 12:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_remove_customuser_person'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='sub_unit',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
