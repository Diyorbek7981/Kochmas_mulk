# Generated by Django 5.0.1 on 2024-02-18 09:12

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('homeapp', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='commentmodel',
            name='Author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='commentmodel',
            name='Parent',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='replies', to='homeapp.commentmodel'),
        ),
        migrations.AddField(
            model_name='homemodel',
            name='owner',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='commentmodel',
            name='Post',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='homeapp.homemodel'),
        ),
        migrations.AddField(
            model_name='homemodel',
            name='home_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='homeapp.hometypemodel'),
        ),
        migrations.AddField(
            model_name='picturemodel',
            name='home',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='homeapp.homemodel'),
        ),
        migrations.AddField(
            model_name='searchmodel',
            name='home_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='homeapp.hometypemodel'),
        ),
        migrations.AddField(
            model_name='searchmodel',
            name='type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='homeapp.typemodel'),
        ),
        migrations.AddField(
            model_name='homemodel',
            name='type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='homeapp.typemodel'),
        ),
    ]
