# Generated by Django 5.0.1 on 2024-02-27 14:54

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('homeapp', '0002_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='homemodel',
            name='comforts',
            field=models.ManyToManyField(to='homeapp.comforstypemodel'),
        ),
        migrations.AlterField(
            model_name='picturemodel',
            name='home',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='pictures', to='homeapp.homemodel'),
        ),
    ]