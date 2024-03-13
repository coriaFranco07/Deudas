# Generated by Django 5.0.1 on 2024-01-15 19:01

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('estado', '0003_alter_histestado_dsc_std'),
        ('legajo', '0001_initial'),
        ('reclamo', '0003_remove_reclamo_activo_rec'),
        ('tipo_reclamo', '0004_alter_histtiporeclamo_options'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='HistReclamo',
            fields=[
                ('h_id_rec', models.AutoField(primary_key=True, serialize=False)),
                ('id_rec', models.PositiveBigIntegerField()),
                ('fch_dsd_rec', models.DateField()),
                ('fch_hst_rec', models.DateField()),
                ('dias_rec', models.PositiveIntegerField(default=0)),
                ('fch_rec', models.DateTimeField(auto_now=True)),
                ('user_rec', models.CharField(max_length=20)),
                ('slug', models.CharField(blank=True, max_length=200, null=True)),
                ('h_fch_proc', models.DateTimeField(auto_now_add=True)),
                ('h_tipo_proc', models.CharField(max_length=1, null=True)),
                ('h_user_proc', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to=settings.AUTH_USER_MODEL)),
                ('id_legajo', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='legajo.legajo')),
                ('id_tipo_rec', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='tipo_reclamo.tiporeclamo')),
                ('std_rec', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='estado.estado')),
            ],
            options={
                'verbose_name': 'Reclamo',
                'verbose_name_plural': 'Reclamos',
                'ordering': ['-h_fch_proc'],
            },
        ),
    ]