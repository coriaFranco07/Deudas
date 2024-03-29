# Generated by Django 5.0.1 on 2024-01-24 20:00

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('administrador', '0006_delete_historialadmin'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='HistorialAdmin',
            fields=[
                ('h_id_user', models.AutoField(primary_key=True, serialize=False)),
                ('id_user', models.PositiveBigIntegerField()),
                ('email', models.EmailField(max_length=254)),
                ('password', models.CharField(max_length=255)),
                ('h_fch_creacion', models.DateTimeField(auto_now_add=True)),
                ('h_fch_modificacion', models.DateTimeField(auto_now=True)),
                ('h_user_proc', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'H_Usuario',
                'verbose_name_plural': 'H_Usuarios',
            },
        ),
    ]
