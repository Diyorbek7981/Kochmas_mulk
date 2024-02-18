from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from usersapp.models import Users



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
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.home.name


# CHOICES = (
#     (1, 'Up'),
#     (0, 'Down'),
# )
CHOICES = (
    (1, '1 xona'),
    (2, '2 xona'),
    (3, '3 xona'),
    (4, '4 xona'),
    (5, '5 xona'),
    (6, '6 va undan ortiq xonalar'),
)


class SearchModel(models.Model):
    type = models.ForeignKey(TypeModel, on_delete=models.CASCADE)
    home_type = models.ForeignKey(HomeTypeModel, on_delete=models.CASCADE)
    count_rooms = models.IntegerField(default=1,
                                      choices=CHOICES,
                                      null=True,
                                      blank=True)
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


# coment u-n
class CommentModel(models.Model):
    Author = models.ForeignKey(Users, on_delete=models.CASCADE)
    CreatedDate = models.DateTimeField(auto_now_add=True)
    ModifiedDate = models.DateTimeField(auto_now=True, editable=False)
    CommentText = models.CharField(max_length=150)
    Post = models.ForeignKey(HomeModel, on_delete=models.CASCADE)
    Parent = models.ForeignKey(
        "self",
        on_delete=models.CASCADE,
        null=True, blank=True,
        related_name="replies")

    class Meta:
        ordering = ("CreatedDate",)

    def __str__(self):
        return f'{self.Author.username} - {self.CommentText[:10]} >> {self.Parent}'

    def children(self):
        return CommentModel.objects.filter(Parent=self)

    @property
    def any_children(self):
        return CommentModel.objects.filter(Parent=self).exists()
