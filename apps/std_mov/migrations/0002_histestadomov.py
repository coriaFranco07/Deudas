# Generated by Django 5.0.1 on 2024-01-15 13:49

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('std_mov', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='HistEstadoMov',
            fields=[
                ('h_id_std_mov', models.AutoField(primary_key=True, serialize=False)),
                ('id_std_mov', models.PositiveIntegerField()),
                ('dsc_std_mov', models.CharField(max_length=50)),
                ('fch_std_mov', models.DateTimeField(auto_now=True)),
                ('user_std_mov', models.CharField(max_length=20)),
                ('slug', models.CharField(blank=True, max_length=200, null=True)),
                ('h_fch_proc', models.DateTimeField(auto_now_add=True)),
                ('h_tipo_proc', models.CharField(max_length=1, null=True)),
                ('h_user_proc', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'H_Estado de Movimiento',
                'verbose_name_plural': 'H_Estados de Movimientos',
                'ordering': ['-h_fch_proc'],
            },
        ),
    ]