# Generated by Django 5.0.1 on 2024-01-10 00:25

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movimiento', '0002_movimiento_fch_mov_user_alter_movimiento_fch_mov_and_more'),
        ('reclamo', '0003_remove_reclamo_activo_rec'),
    ]

    operations = [
        migrations.AlterField(
            model_name='movimiento',
            name='id_rec',
            field=models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, related_name='reclam', to='reclamo.reclamo'),
        ),
    ]
