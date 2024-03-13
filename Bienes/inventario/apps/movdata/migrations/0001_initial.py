# Generated by Django 4.2.1 on 2023-06-23 11:36

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('oficina', '0001_initial'),
        ('bien', '0001_initial'),
        ('estado', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='MovData',
            fields=[
                ('id_mov', models.AutoField(primary_key=True, serialize=False)),
                ('gde_mov', models.CharField(blank=True, max_length=80, null=True)),
                ('observ_mov', models.TextField(blank=True, max_length=500, null=True)),
                ('fch_dsd', models.DateTimeField(auto_now_add=True)),
                ('fch_hst', models.DateTimeField(blank=True, null=True)),
                ('slug', models.SlugField(blank=True, max_length=200, null=True)),
                ('bien_mov', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.RESTRICT, related_name='movimientos', to='bien.bien')),
                ('destino', models.ForeignKey(default=None, on_delete=django.db.models.deletion.RESTRICT, related_name='destino', to='oficina.oficina')),
                ('estado', models.ForeignKey(default='Alta', on_delete=django.db.models.deletion.RESTRICT, related_name='estado', to='estado.estado')),
                ('origen', models.ForeignKey(default=None, on_delete=django.db.models.deletion.RESTRICT, related_name='oficina', to='oficina.oficina')),
                ('user_mov', models.ForeignKey(default=None, on_delete=django.db.models.deletion.RESTRICT, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'MovData',
                'verbose_name_plural': 'MovDatas',
                'ordering': ['bien_mov'],
            },
        ),
    ]