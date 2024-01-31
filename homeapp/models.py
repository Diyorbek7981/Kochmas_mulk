from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator


# Create your models here.
class Users(AbstractUser):
    phone = models.CharField(max_length=20, blank=True, null=True)
    bio = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.username


class TypeModel(models.Model):
    name = models.CharField(max_length=50)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class LocationModel(models.Model):
    name = models.CharField(max_length=50)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class HomeTypeModel(models.Model):
    name = models.CharField(max_length=50)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class HomeModel(models.Model):
    name = models.CharField(max_length=150)
    type = models.ForeignKey(TypeModel, on_delete=models.CASCADE)
    home_type = models.ForeignKey(HomeTypeModel, on_delete=models.CASCADE)
    description = models.TextField()
    price = models.DecimalField(max_digits=8, decimal_places=2)
    rate = models.IntegerField(default=0, validators=[MaxValueValidator(5), MinValueValidator(0)])
    location = models.ForeignKey(LocationModel, on_delete=models.CASCADE)
    owner = models.ForeignKey(Users, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Kochmas mulk'
        verbose_name_plural = 'Kochmas mulklar'
        ordering = ['-created']

    def __str__(self):
        return self.name


class PictureModel(models.Model):
    pic = models.ImageField(upload_to='home/')
    home = models.ForeignKey(HomeModel, on_delete=models.CASCADE)
    owner = models.ForeignKey(Users, on_delete=models.CASCADE)

    def __str__(self):
        return self.home.name
