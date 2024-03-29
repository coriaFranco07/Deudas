# Generated by Django 5.0.1 on 2024-01-15 14:05

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movimiento', '0007_alter_movimiento_fch_mov_user'),
        ('reclamo', '0003_remove_reclamo_activo_rec'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='movimiento',
            options={'ordering': ['-fch_std_mov'], 'verbose_name': 'Movimiento', 'verbose_name_plural': 'Movimiento'},
        ),
        migrations.CreateModel(
            name='HistMovimiento',
            fields=[
                ('h_id_mov', models.AutoField(primary_key=True, serialize=False)),
                ('id_mov', models.PositiveBigIntegerField()),
                ('fch_mov', models.DateField()),
                ('id_std_mov', models.CharField(max_length=50)),
                ('gde_mov', models.CharField(blank=True, max_length=50, null=True)),
                ('obs_mov', models.CharField(blank=True, max_length=200, null=True)),
                ('fch_std_mov', models.DateField()),
                ('fch_mov_user', models.DateTimeField(auto_now_add=True)),
                ('user_mov', models.CharField(max_length=20)),
                ('slug', models.CharField(blank=True, max_length=200, null=True)),
                ('h_fch_proc', models.DateTimeField(auto_now_add=True)),
                ('h_tipo_proc', models.CharField(max_length=1, null=True)),
                ('h_user_proc', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to=settings.AUTH_USER_MODEL)),
                ('id_rec', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='reclamo.reclamo')),
            ],
            options={
                'verbose_name': 'H_Movimiento',
                'verbose_name_plural': 'H_Movimiento',
                'ordering': ['-h_fch_proc'],
            },
        ),
    ]
