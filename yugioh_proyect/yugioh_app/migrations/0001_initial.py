# Generated by Django 5.1.4 on 2025-01-04 23:58

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Carta',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=255)),
                ('tipo', models.CharField(max_length=255)),
                ('nivel', models.IntegerField()),
                ('ataque', models.IntegerField()),
                ('defensa', models.IntegerField()),
                ('descripcion', models.TextField()),
                ('imagen_url', models.URLField()),
            ],
        ),
        migrations.CreateModel(
            name='Deck',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=255)),
                ('fecha_creacion', models.DateTimeField(auto_now_add=True)),
                ('usuario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='CartaDeck',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cantidad', models.IntegerField()),
                ('carta', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='yugioh_app.carta')),
                ('deck', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='yugioh_app.deck')),
            ],
        ),
        migrations.CreateModel(
            name='Partida',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha_inicio', models.DateTimeField(auto_now_add=True)),
                ('fecha_fin', models.DateTimeField(blank=True, null=True)),
                ('ganador', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ganador', to=settings.AUTH_USER_MODEL)),
                ('jugador1', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='jugador1', to=settings.AUTH_USER_MODEL)),
                ('jugador2', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='jugador2', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
