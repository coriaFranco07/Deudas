# Generated by Django 5.0.1 on 2024-01-13 12:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tipo_reclamo', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='tiporeclamo',
            name='tipo_anual',
            field=models.BooleanField(default=False),
        ),
    ]