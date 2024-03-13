# Generated by Django 5.0.1 on 2024-01-10 00:37

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movimiento', '0003_alter_movimiento_id_rec'),
        ('reclamo', '0003_remove_reclamo_activo_rec'),
    ]

    operations = [
        migrations.AlterField(
            model_name='movimiento',
            name='id_rec',
            field=models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='reclamo.reclamo'),
        ),
    ]