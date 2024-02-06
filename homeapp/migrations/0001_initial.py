# Generated by Django 5.0.1 on 2024-02-06 15:24

import django.contrib.auth.models
import django.contrib.auth.validators
import django.core.validators
import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='HomeTypeModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='LocationModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='TypeModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Users',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('phone', models.CharField(blank=True, max_length=20, null=True)),
                ('bio', models.TextField(blank=True, null=True)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='HomeModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150)),
                ('name_en', models.CharField(max_length=150, null=True)),
                ('name_uz', models.CharField(max_length=150, null=True)),
                ('name_ru', models.CharField(max_length=150, null=True)),
                ('count_rooms', models.IntegerField(default=0, validators=[django.core.validators.MaxValueValidator(10), django.core.validators.MinValueValidator(0)])),
                ('description', models.TextField()),
                ('description_en', models.TextField(null=True)),
                ('description_uz', models.TextField(null=True)),
                ('description_ru', models.TextField(null=True)),
                ('price', models.DecimalField(decimal_places=2, max_digits=8, validators=[django.core.validators.MinValueValidator(0)])),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('home_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='homeapp.hometypemodel')),
                ('home_type_en', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='homeapp.hometypemodel')),
                ('home_type_ru', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='homeapp.hometypemodel')),
                ('home_type_uz', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='homeapp.hometypemodel')),
                ('location', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='homeapp.locationmodel')),
                ('location_en', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='homeapp.locationmodel')),
                ('location_ru', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='homeapp.locationmodel')),
                ('location_uz', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='homeapp.locationmodel')),
                ('type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='homeapp.typemodel')),
                ('type_en', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='homeapp.typemodel')),
                ('type_ru', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='homeapp.typemodel')),
                ('type_uz', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='homeapp.typemodel')),
            ],
            options={
                'verbose_name': 'Ko`chmas mulk',
                'verbose_name_plural': 'Ko`chmas mulklar',
                'ordering': ['-created'],
            },
        ),
        migrations.CreateModel(
            name='PictureModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pic', models.ImageField(upload_to='home/')),
                ('home', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='homeapp.homemodel')),
            ],
        ),
        migrations.CreateModel(
            name='SearchModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('count_rooms', models.IntegerField(default=0, validators=[django.core.validators.MaxValueValidator(10), django.core.validators.MinValueValidator(0)])),
                ('price', models.DecimalField(blank=True, decimal_places=2, max_digits=8, null=True, validators=[django.core.validators.MinValueValidator(0)])),
                ('up_low', models.IntegerField(blank=True, default=0, null=True, validators=[django.core.validators.MaxValueValidator(1), django.core.validators.MinValueValidator(0)])),
                ('home_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='homeapp.hometypemodel')),
                ('location', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='homeapp.locationmodel')),
                ('type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='homeapp.typemodel')),
            ],
        ),
    ]
