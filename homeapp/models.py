from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator, MaxLengthValidator
from usersapp.models import Users
from django.db.models import UniqueConstraint
from django.core.validators import FileExtensionValidator
from geopy.geocoders import Nominatim

CHOICES = (
    (1, '1 xona'),
    (2, '2 xona'),
    (3, '3 xona'),
    (4, '4 xona'),
    (5, '5 xona'),
    (6, '6 va undan ortiq xonalar'),
    (7, 'Studiya'),
    (8, 'Ochiq plan'),
)

REPAIR_CHOICES = (
    ('Avtorlik loyhasi', 'Avtorlik loyhasi'),
    ('Evroremont', 'Evroremont'),
    ('O`rta', 'O`rta'),
    ('Tamir talab', 'Tamir talab'),
    ('Oddiy suvoq', 'Oddiy suvoq')
)

Building_Material = (
    ('G`isht', 'G`isht'),
    ('Monolit', 'Monolit'),
    ('Panel', 'Panel'),
    ('Bloklar', 'Bloklar'),
    ('Boshqa', 'Boshqa')
)


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


class ComforsTypeModel(models.Model):
    name = models.CharField(max_length=50)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class HomeModel(models.Model):
    type = models.ForeignKey(TypeModel, on_delete=models.CASCADE)
    home_type = models.ForeignKey(HomeTypeModel, on_delete=models.CASCADE)
    location = models.CharField(max_length=100)
    count_rooms = models.IntegerField(default=1,
                                      choices=CHOICES)
    vip = models.BooleanField(default=False)
    area = models.DecimalField(max_digits=5,
                               decimal_places=2,
                               validators=[MinValueValidator(0)])
    floor = models.IntegerField(null=True,
                                blank=True,
                                validators=[MinValueValidator(0)])
    building_floor = models.IntegerField(null=True,
                                         blank=True,
                                         validators=[MinValueValidator(0)])
    repair = models.CharField(max_length=100,
                              choices=REPAIR_CHOICES)
    building_material = models.CharField(max_length=100,
                                         choices=Building_Material)
    price = models.DecimalField(max_digits=8,
                                decimal_places=2,
                                validators=[MinValueValidator(0)])
    description = models.TextField(validators=[MaxLengthValidator(1000)])
    comforts = models.ManyToManyField(ComforsTypeModel, null=True, blank=True)
    owner = models.ForeignKey(Users, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Ko`chmas mulk'
        verbose_name_plural = 'Ko`chmas mulklar'
        ordering = ['-created']

    def __str__(self):
        return f"{self.type} - {self.home_type} - {self.owner}"


class PictureModel(models.Model):
    pic = models.ImageField(upload_to='home/', null=True, blank=True,
                            validators=[
                                FileExtensionValidator(allowed_extensions=[
                                    'jpg', 'jpeg', 'png', 'heic', 'heif'
                                ])])
    home = models.ForeignKey(HomeModel, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.home.type} - {self.home.home_type} - {self.home.owner}"


# CHOICES = (
#     (1, 'Up'),
#     (0, 'Down'),
# )


class SearchModel(models.Model):
    type = models.ForeignKey(TypeModel, on_delete=models.CASCADE, null=True, blank=True)
    home_type = models.ForeignKey(HomeTypeModel, on_delete=models.CASCADE, null=True, blank=True)
    location = models.CharField(max_length=100, null=True, blank=True)
    count_rooms = models.IntegerField(default=1,
                                      choices=CHOICES,
                                      null=True,
                                      blank=True)
    from_area = models.DecimalField(max_digits=5, decimal_places=2,
                                    validators=[MinValueValidator(0)],
                                    null=True,
                                    blank=True)
    up_area = models.DecimalField(max_digits=5, decimal_places=2,
                                  validators=[MinValueValidator(0)],
                                  null=True,
                                  blank=True)
    floor = models.IntegerField(null=True,
                                blank=True,
                                validators=[MinValueValidator(0)])
    building_floor = models.IntegerField(null=True,
                                         blank=True,
                                         validators=[MinValueValidator(0)])
    repair = models.CharField(max_length=100,
                              choices=REPAIR_CHOICES,
                              null=True, blank=True)
    building_material = models.CharField(max_length=100,
                                         choices=Building_Material,
                                         null=True, blank=True)
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


class HomeLike(models.Model):
    author = models.ForeignKey(Users, on_delete=models.CASCADE)
    home = models.ForeignKey(HomeModel, on_delete=models.CASCADE, related_name='likes')

    # home.likes buyrugi berilsa shu homga tegishli barcha likelar keladi

    class Meta:  # 1 ta modelga 1 user ko'p like bosmasligi uchun
        constraints = [
            UniqueConstraint(
                fields=['author', 'home'],
                # ko'rsatilgan author ko'rsatilgan postga 1 marta like bosadi (2 - sini qbulqilmaydi)
                name='postLikeUnique'
            )
        ]

    def __str__(self):
        return f"{self.author} -- {self.home}"
