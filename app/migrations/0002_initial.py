# Generated by Django 4.2.2 on 2023-09-19 14:03

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('app', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='basemodel',
            name='created_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='%(class)s_creator', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='basemodel',
            name='modified_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='%(class)s_updater', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='transaction',
            name='persons',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='app.person'),
        ),
        migrations.AddField(
            model_name='subunit',
            name='units',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='app.unit'),
        ),
        migrations.AddField(
            model_name='station',
            name='sub_unit',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='app.subunit'),
        ),
        migrations.AddField(
            model_name='person',
            name='person_rank',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='app.rank'),
        ),
        migrations.AddField(
            model_name='person',
            name='person_station',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='app.station'),
        ),
        migrations.AddField(
            model_name='person',
            name='person_unit',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='app.unit'),
        ),
    ]
