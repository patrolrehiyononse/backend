# Generated by Django 4.2.2 on 2024-06-03 07:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0015_alter_pathtrace_path_line'),
    ]

    operations = [
        migrations.RenameField(
            model_name='pathtrace',
            old_name='path_line',
            new_name='lat',
        ),
        migrations.AddField(
            model_name='pathtrace',
            name='lng',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
