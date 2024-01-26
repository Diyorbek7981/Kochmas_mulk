from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator


# Create your models here.
class HomeModel(models.Model):
    name = models.CharField(max_length=150)
    description = models.TextField()
    price = models.DecimalField(max_digits=8, decimal_places=2)
    rate = models.IntegerField(default=0, validators=[MaxValueValidator(5), MinValueValidator(0)])
    location = models.TextField(blank=True, null=True, default='Tashkent')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class PictureModel(models.Model):
    pic = models.ImageField(upload_to='home/')
    home = models.ForeignKey(HomeModel, on_delete=models.CASCADE)

    def __str__(self):
        return self.home.name
