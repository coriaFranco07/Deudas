# Generated by Django 5.0.1 on 2024-02-05 17:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reclamo', '0011_rename_year_cred_histreclamo_year_credito'),
    ]

    operations = [
        migrations.AlterField(
            model_name='histreclamo',
            name='nro_supl',
            field=models.PositiveBigIntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='histreclamo',
            name='year_credito',
            field=models.PositiveSmallIntegerField(blank=True, null=True),
        ),
    ]
