# Generated by Django 5.0.1 on 2024-01-15 13:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('control_std', '0011_histcontrolestado_h_fch_proc_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='histcontrolestado',
            options={'ordering': ['-h_fch_proc'], 'verbose_name': 'H_Control Estado', 'verbose_name_plural': 'H_Controles Estados'},
        ),
    ]