# Generated by Django 4.0.5 on 2022-07-08 22:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Curriculo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('empresa', models.CharField(max_length=120)),
                ('data_inicio', models.DateTimeField()),
                ('data_saida', models.DateTimeField()),
                ('empresa_atual', models.BooleanField()),
                ('resumo', models.TextField()),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Perfil',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('nome', models.CharField(max_length=30)),
                ('sobrenome', models.CharField(max_length=30)),
                ('email', models.EmailField(max_length=254)),
                ('github', models.URLField()),
                ('avatar', models.ImageField(upload_to='')),
                ('celular', models.CharField(max_length=20)),
                ('perfil', models.TextField()),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
