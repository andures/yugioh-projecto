# Generated by Django 5.1.4 on 2025-01-05 04:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('yugioh_app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='carta',
            name='ataque',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='carta',
            name='defensa',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='carta',
            name='descripcion',
            field=models.TextField(default=''),
        ),
        migrations.AlterField(
            model_name='carta',
            name='imagen_url',
            field=models.URLField(default=''),
        ),
        migrations.AlterField(
            model_name='carta',
            name='nivel',
            field=models.IntegerField(default=1),
        ),
    ]
