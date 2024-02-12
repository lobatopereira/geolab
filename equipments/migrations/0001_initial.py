# Generated by Django 4.2.3 on 2023-09-03 16:12

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
            name='DetalluEkipamentu',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nu_serial', models.CharField(max_length=100, null=True)),
                ('kondisaun', models.CharField(choices=[('Diak', 'Diak'), ('Aat', 'Aat')], max_length=10, null=True, verbose_name='Kondisaun')),
                ('status', models.CharField(choices=[('Uza Hela', 'Uza Hela'), ('Disponivel', 'Disponivel')], max_length=30, null=True, verbose_name='Status Ekipamentu')),
                ('image', models.ImageField(blank=True, null=True, upload_to='DetalluEkipamentu')),
                ('date_created', models.DateTimeField(auto_now_add=True, null=True)),
                ('hashed', models.CharField(max_length=32, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Doadores',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('kodigu', models.CharField(max_length=255, null=True)),
                ('doador', models.CharField(max_length=255, null=True)),
                ('date_created', models.DateTimeField(auto_now_add=True, null=True)),
                ('hashed', models.CharField(max_length=32, null=True)),
                ('user_created', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Ekipamentu',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data_simu', models.DateField(blank=True, null=True)),
                ('naran', models.CharField(max_length=255, null=True)),
                ('marka', models.CharField(max_length=255, null=True)),
                ('date_created', models.DateTimeField(auto_now_add=True, null=True)),
                ('hashed', models.CharField(max_length=32, null=True)),
                ('doador', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='doadorekipamentu', to='equipments.doadores')),
            ],
        ),
        migrations.CreateModel(
            name='Utilizador',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('naran', models.CharField(max_length=255, null=True, verbose_name='Naran Responsavel')),
                ('pozisaun', models.CharField(max_length=255, null=True, verbose_name='Pozisaun')),
                ('seksu', models.CharField(choices=[('Mane', 'Mane'), ('Feto', 'Feto')], max_length=10, null=True, verbose_name='Seksu')),
                ('nu_kontaktu', models.CharField(max_length=50, null=True, verbose_name='Nu. Kontaktu')),
                ('image', models.ImageField(blank=True, null=True, upload_to='Utilizador')),
                ('date_created', models.DateTimeField(auto_now_add=True, null=True)),
                ('hashed', models.CharField(max_length=32, null=True)),
                ('user_created', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='UtilizaEkipamentu',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data_empresta', models.DateField(blank=True, null=True, verbose_name='Data Empresta')),
                ('data_entrega', models.DateField(blank=True, null=True, verbose_name='Data entrega')),
                ('is_return', models.BooleanField(default=False, null=True)),
                ('kondisaun', models.CharField(choices=[('Diak', 'Diak'), ('Aat', 'Aat')], max_length=10, null=True, verbose_name='Kondisaun Depois Uza')),
                ('date_created', models.DateTimeField(auto_now_add=True, null=True)),
                ('hashed', models.CharField(max_length=32, null=True)),
                ('ekipamentu', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='uzaekipamentu', to='equipments.ekipamentu')),
                ('item', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='uzaekipamentu', to='equipments.detalluekipamentu')),
                ('user_created', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('utilizador', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='utilizadorekipamentu', to='equipments.utilizador')),
            ],
        ),
        migrations.CreateModel(
            name='KuantidadeEkipamentu',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('kuantidade_inisiu', models.IntegerField(blank=True, null=True, verbose_name='Kuantidade Inisiu')),
                ('kuantidade_disponivel', models.IntegerField(blank=True, null=True, verbose_name='Kuantidade Disponivel')),
                ('kuantidade_empresta', models.IntegerField(blank=True, null=True, verbose_name='Kuantidade Uza Hela')),
                ('date_created', models.DateTimeField(auto_now_add=True, null=True)),
                ('hashed', models.CharField(max_length=32, null=True)),
                ('ekipamentu', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='kuantekipamentu', to='equipments.ekipamentu')),
                ('user_created', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Kategoria',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('kategoria', models.CharField(max_length=255, null=True)),
                ('date_created', models.DateTimeField(auto_now_add=True, null=True)),
                ('hashed', models.CharField(max_length=32, null=True)),
                ('user_created', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='ekipamentu',
            name='kategoria',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='katekipamentu', to='equipments.kategoria'),
        ),
        migrations.AddField(
            model_name='ekipamentu',
            name='user_created',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='detalluekipamentu',
            name='ekipamentu',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='detekipamentu', to='equipments.ekipamentu'),
        ),
        migrations.AddField(
            model_name='detalluekipamentu',
            name='user_created',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
