# Generated by Django 5.0.1 on 2024-01-24 13:31

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movimiento', '0009_alter_movimiento_id_rec'),
        ('rec_prioridad', '0008_histrec_prioridad_norma_legal_prior_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rec_prioridad',
            name='id_mov',
            field=models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, related_name='prior_movs', to='movimiento.movimiento'),
        ),
    ]
