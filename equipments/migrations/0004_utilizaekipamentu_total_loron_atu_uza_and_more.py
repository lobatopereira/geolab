# Generated by Django 4.2.3 on 2023-10-20 18:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('equipments', '0003_utilizaekipamentu_data_atu_entrega'),
    ]

    operations = [
        migrations.AddField(
            model_name='utilizaekipamentu',
            name='total_loron_atu_uza',
            field=models.IntegerField(blank=True, null=True, verbose_name='Total Loron'),
        ),
        migrations.AddField(
            model_name='utilizaekipamentu',
            name='total_loron_kontra',
            field=models.IntegerField(blank=True, null=True, verbose_name='Total Loron'),
        ),
    ]
