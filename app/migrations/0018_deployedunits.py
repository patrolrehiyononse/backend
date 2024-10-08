# Generated by Django 4.2.2 on 2024-07-08 04:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0017_pathtrace_datetime'),
    ]

    operations = [
        migrations.CreateModel(
            name='DeployedUnits',
            fields=[
                ('basemodel_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='app.basemodel')),
                ('starting_point', models.CharField(blank=True, max_length=500, null=True)),
                ('destination', models.CharField(blank=True, max_length=500, null=True)),
                ('distance', models.IntegerField(blank=True, null=True)),
                ('duration', models.DecimalField(blank=True, decimal_places=1, max_digits=10, null=True)),
                ('persons', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='app.person')),
            ],
            bases=('app.basemodel',),
        ),
    ]
