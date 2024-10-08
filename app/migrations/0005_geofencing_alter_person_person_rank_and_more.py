# Generated by Django 4.2.2 on 2024-04-20 11:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0004_person_account_number'),
    ]

    operations = [
        migrations.CreateModel(
            name='Geofencing',
            fields=[
                ('basemodel_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='app.basemodel')),
                ('name', models.CharField(blank=True, max_length=255, null=True)),
                ('coordinates', models.CharField(blank=True, max_length=255, null=True)),
            ],
            bases=('app.basemodel',),
        ),
        migrations.AlterField(
            model_name='person',
            name='person_rank',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='app.rank'),
        ),
        migrations.AlterField(
            model_name='person',
            name='person_station',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='app.station'),
        ),
        migrations.AlterField(
            model_name='person',
            name='person_unit',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='app.unit'),
        ),
        migrations.AlterField(
            model_name='subunit',
            name='units',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='app.unit'),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='persons',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='app.person'),
        ),
    ]
