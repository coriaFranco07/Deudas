# Generated by Django 5.0.1 on 2024-01-15 13:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('estado', '0002_histestado'),
    ]

    operations = [
        migrations.AlterField(
            model_name='histestado',
            name='dsc_std',
            field=models.CharField(max_length=50),
        ),
    ]