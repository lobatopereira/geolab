# Generated by Django 4.2.3 on 2023-11-18 05:54

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('equipments', '0005_alter_utilizaekipamentu_kondisaun'),
    ]

    operations = [
        migrations.CreateModel(
            name='LabInventory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('naran', models.CharField(max_length=255, null=True)),
                ('dataTama', models.DateField(blank=True, null=True)),
                ('marka', models.CharField(max_length=255, null=True)),
                ('date_created', models.DateTimeField(auto_now_add=True, null=True)),
                ('hashed', models.CharField(max_length=32, null=True)),
                ('doador', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='doadorinventory', to='equipments.doadores')),
                ('kategoria', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='katinventory', to='equipments.kategoria')),
                ('user_created', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AlterField(
            model_name='utilizaekipamentu',
            name='item',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='uzaekipamentu', to='equipments.detalluekipamentu', verbose_name='Detallu Ekipamentu'),
        ),
        migrations.AlterField(
            model_name='utilizaekipamentu',
            name='total_loron_kontra',
            field=models.IntegerField(blank=True, null=True, verbose_name='Total Loron Kontra'),
        ),
        migrations.CreateModel(
            name='LabInventoryTransaction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data', models.DateField(null=True)),
                ('total_tama', models.IntegerField(blank=True, null=True, verbose_name='Total Tama')),
                ('total_sai', models.IntegerField(blank=True, null=True, verbose_name='Total Sai')),
                ('total', models.IntegerField(blank=True, null=True, verbose_name='Total')),
                ('is_confirm', models.BooleanField(default=False, null=True)),
                ('date_created', models.DateTimeField(auto_now_add=True, null=True)),
                ('hashed', models.CharField(max_length=32, null=True)),
                ('inventory', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='inventoryTransaction', to='equipments.labinventory')),
                ('user_created', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='LabInventoryStock',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('kodigu_stock', models.CharField(blank=True, max_length=100, null=True)),
                ('total_tama', models.IntegerField(blank=True, null=True, verbose_name='Total Tama')),
                ('total_stock', models.IntegerField(blank=True, null=True, verbose_name='Total Stock')),
                ('total_sai', models.IntegerField(blank=True, null=True, verbose_name='Total Sai')),
                ('date_created', models.DateTimeField(auto_now_add=True, null=True)),
                ('hashed', models.CharField(max_length=32, null=True)),
                ('inventory', models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='inventoryStock', to='equipments.labinventory')),
                ('user_created', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
