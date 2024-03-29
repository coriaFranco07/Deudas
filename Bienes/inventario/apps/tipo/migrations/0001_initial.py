# Generated by Django 4.2.1 on 2023-06-23 11:36

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Tipo',
            fields=[
                ('id_tipo', models.AutoField(primary_key=True, serialize=False)),
                ('dsc_tipo', models.CharField(max_length=30, unique=True)),
                ('fch_tipo', models.DateTimeField(auto_now=True)),
                ('slug', models.SlugField(blank=True, max_length=200, null=True)),
                ('user_tipo', models.ForeignKey(default=None, on_delete=django.db.models.deletion.RESTRICT, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'tipo',
                'verbose_name_plural': 'tipo',
                'ordering': ['dsc_tipo'],
            },
        ),
    ]
