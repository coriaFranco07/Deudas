# Generated by Django 5.0.1 on 2024-01-15 12:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('control_std', '0006_alter_histcontrolestado_options_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='histcontrolestado',
            name='std_origen',
            field=models.CharField(max_length=20, null=True),
        ),
    ]
