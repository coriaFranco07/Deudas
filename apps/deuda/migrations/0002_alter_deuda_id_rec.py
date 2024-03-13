# Generated by Django 5.0.1 on 2024-01-13 05:49

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('deuda', '0001_initial'),
        ('reclamo', '0003_remove_reclamo_activo_rec'),
    ]

    operations = [
        migrations.AlterField(
            model_name='deuda',
            name='id_rec',
            field=models.OneToOneField(on_delete=django.db.models.deletion.RESTRICT, related_name='deudas_reclamos', to='reclamo.reclamo'),
        ),
    ]
