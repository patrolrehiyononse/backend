# Generated by Django 4.2.2 on 2024-05-13 10:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0007_person_person_sub_unit'),
    ]

    operations = [
        migrations.AlterField(
            model_name='person',
            name='person_rank',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='app.rank'),
        ),
        migrations.AlterField(
            model_name='person',
            name='person_station',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='app.station'),
        ),
        migrations.AlterField(
            model_name='person',
            name='person_sub_unit',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='app.subunit'),
        ),
        migrations.AlterField(
            model_name='person',
            name='person_unit',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='app.unit'),
        ),
        migrations.AlterField(
            model_name='subunit',
            name='units',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='app.unit'),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='persons',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='app.person'),
        ),
    ]
