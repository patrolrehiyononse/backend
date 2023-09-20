# Generated by Django 4.2.2 on 2023-09-19 14:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='BaseModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_date', models.DateTimeField(auto_now=True)),
                ('modified_date', models.DateTimeField(auto_now=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Person',
            fields=[
                ('basemodel_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='app.basemodel')),
                ('full_name', models.CharField(blank=True, max_length=255, null=True)),
                ('email', models.EmailField(blank=True, max_length=255, null=True)),
            ],
            bases=('app.basemodel',),
        ),
        migrations.CreateModel(
            name='Rank',
            fields=[
                ('basemodel_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='app.basemodel')),
                ('rank_code', models.CharField(blank=True, max_length=255, null=True)),
                ('description', models.CharField(blank=True, max_length=255, null=True)),
            ],
            bases=('app.basemodel',),
        ),
        migrations.CreateModel(
            name='Station',
            fields=[
                ('basemodel_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='app.basemodel')),
                ('station_code', models.CharField(blank=True, max_length=255, null=True)),
                ('station_name', models.CharField(blank=True, max_length=255, null=True)),
                ('description', models.CharField(blank=True, max_length=255, null=True)),
            ],
            bases=('app.basemodel',),
        ),
        migrations.CreateModel(
            name='SubUnit',
            fields=[
                ('basemodel_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='app.basemodel')),
                ('sub_unit_code', models.CharField(blank=True, max_length=255, null=True)),
                ('sub_unit_description', models.CharField(blank=True, max_length=255, null=True)),
                ('abbreviation', models.CharField(blank=True, max_length=255, null=True)),
            ],
            bases=('app.basemodel',),
        ),
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('basemodel_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='app.basemodel')),
                ('lat', models.CharField(blank=True, max_length=255, null=True)),
                ('lng', models.CharField(blank=True, max_length=255, null=True)),
                ('datetime', models.DateTimeField(blank=True, max_length=255, null=True)),
                ('is_active', models.BooleanField(default=False)),
            ],
            bases=('app.basemodel',),
        ),
        migrations.CreateModel(
            name='Unit',
            fields=[
                ('basemodel_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='app.basemodel')),
                ('unit_code', models.CharField(blank=True, max_length=255, null=True)),
                ('abbreviation', models.CharField(blank=True, max_length=255, null=True)),
                ('description', models.CharField(blank=True, max_length=255, null=True)),
            ],
            bases=('app.basemodel',),
        ),
    ]
