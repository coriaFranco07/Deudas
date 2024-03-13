# Generated by Django 5.0.1 on 2024-01-15 13:40

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tipo_reclamo', '0002_tiporeclamo_tipo_anual'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='HistTipoReclamo',
            fields=[
                ('h_id_tipo_rec', models.AutoField(primary_key=True, serialize=False)),
                ('id_tipo_rec', models.PositiveIntegerField()),
                ('dsc_tipo_rec', models.CharField(max_length=50)),
                ('tipo_anual', models.BooleanField(default=False)),
                ('fch_tipo_rec', models.DateTimeField(auto_now=True)),
                ('user_tipo_rec', models.CharField(max_length=20)),
                ('slug', models.CharField(blank=True, max_length=200, null=True)),
                ('h_fch_proc', models.DateTimeField(auto_now_add=True)),
                ('h_tipo_proc', models.CharField(max_length=1, null=True)),
                ('h_user_proc', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Tipo Reclamo',
                'verbose_name_plural': 'Tipos Reclamos',
                'ordering': ['-h_fch_proc'],
            },
        ),
    ]