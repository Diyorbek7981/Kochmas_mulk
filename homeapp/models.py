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
    count_rooms = models.IntegerField(default=0,
                                      validators=[MaxValueValidator(10), MinValueValidator(0)])
    # vip = models.BooleanField(default=False)
    description = models.TextField()
    price = models.DecimalField(max_digits=8,
                                decimal_places=2,
                                validators=[MinValueValidator(0)])
    location = models.CharField(max_length=100)
    owner = models.ForeignKey(Users, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Ko`chmas mulk'
        verbose_name_plural = 'Ko`chmas mulklar'
        ordering = ['-created']

    def __str__(self):
        return self.name


class PictureModel(models.Model):
    pic = models.ImageField(upload_to='home/')
    home = models.ForeignKey(HomeModel, on_delete=models.CASCADE)

    def __str__(self):
        return self.home.name


# CHOICES = (
#     (1, 'Up'),
#     (0, 'Down'),
# )


class SearchModel(models.Model):
    type = models.ForeignKey(TypeModel, on_delete=models.CASCADE)
    home_type = models.ForeignKey(HomeTypeModel, on_delete=models.CASCADE)
    count_rooms = models.IntegerField(default=1, validators=[MaxValueValidator(10), MinValueValidator(1)])
    from_price = models.DecimalField(max_digits=8, decimal_places=2,
                                     validators=[MinValueValidator(0)],
                                     null=True,
                                     blank=True)
    up_to_price = models.DecimalField(max_digits=8, decimal_places=2,
                                      validators=[MinValueValidator(0)],
                                      null=True,
                                      blank=True)
    # up_low = models.IntegerField(default=0,
    #                              choices=CHOICES,
    #                              null=True,
    #                              blank=True
    #                              )
    location = models.CharField(max_length=100, null=True, blank=True)
