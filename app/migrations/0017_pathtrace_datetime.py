# Generated by Django 4.2.2 on 2024-06-03 07:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0016_rename_path_line_pathtrace_lat_pathtrace_lng'),
    ]

    operations = [
        migrations.AddField(
            model_name='pathtrace',
            name='datetime',
            field=models.DateTimeField(blank=True, max_length=255, null=True),
        ),
    ]
