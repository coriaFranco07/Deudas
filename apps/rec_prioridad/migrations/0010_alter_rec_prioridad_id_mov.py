# Generated by Django 5.0.1 on 2024-01-24 13:59

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movimiento', '0009_alter_movimiento_id_rec'),
        ('rec_prioridad', '0009_alter_rec_prioridad_id_mov'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rec_prioridad',
            name='id_mov',
            field=models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, related_name='prioridad_movs', to='movimiento.movimiento'),
        ),
    ]
