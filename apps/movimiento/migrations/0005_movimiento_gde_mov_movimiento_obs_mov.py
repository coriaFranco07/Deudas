# Generated by Django 5.0.1 on 2024-01-10 10:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movimiento', '0004_alter_movimiento_id_rec'),
    ]

    operations = [
        migrations.AddField(
            model_name='movimiento',
            name='gde_mov',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='movimiento',
            name='obs_mov',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]
