from django.contrib.auth.models import AbstractUser
from django.db import models
import random
import uuid  # takrorlanishlar ehtimoli kam
from django.core.validators import MaxValueValidator, MinValueValidator, FileExtensionValidator
from datetime import datetime, timedelta

from rest_framework_simplejwt.tokens import RefreshToken
from .utils import BaseModel

# Create your models here.
ORDINARY_USER, MANAGER, ADMIN = ("ordinary_user", 'manager', 'admin')
VIA_EMAIL, VIA_PHONE = ("via_email", "via_phone")
NEW, CODE_VERIFIED, DONE, PHOTO_DONE = ('new', 'code_verified', 'done', 'photo_done')


class Users(AbstractUser, BaseModel):
    USER_ROLES = (
        (ORDINARY_USER, ORDINARY_USER),
        (MANAGER, MANAGER),
        (ADMIN, ADMIN)
    )
    AUTH_TYPE_CHOICES = (
        (VIA_PHONE, VIA_PHONE),
        (VIA_EMAIL, VIA_EMAIL)
    )
    AUTH_STATUS = (
        (NEW, NEW),
        (CODE_VERIFIED, CODE_VERIFIED),
        (DONE, DONE),
        (PHOTO_DONE, PHOTO_DONE)
    )

    user_roles = models.CharField(max_length=31, choices=USER_ROLES, default=ORDINARY_USER)
    auth_type = models.CharField(max_length=31, choices=AUTH_TYPE_CHOICES)
    auth_status = models.CharField(max_length=31, choices=AUTH_STATUS, default=NEW)
    email = models.EmailField(null=True, blank=True, unique=True)
    phone_number = models.CharField(max_length=13, null=True, blank=True, unique=True)
    photo = models.ImageField(upload_to='user_photos/', null=True, blank=True,
                              validators=[
                                  FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png', 'heic', 'heif'])])

    def __str__(self):
        return self.username

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    # cod yaratib beradi tasodifi jonatish uchun
    def create_verify_code(self, verify_type):
        code = "".join([str(random.randint(0, 10000) % 10) for _ in range(4)])
        UserConfirmation.objects.create(
            user_id=self.id,
            verify_type=verify_type,
            code=code
        )
        return code

    # userga tasodifiy nom berib turadi
    def check_username(self):
        if not self.username:
            temp_username = f'user-{uuid.uuid4().__str__().split("-")[-1]}'  # instagram-23324fsdf
            while Users.objects.filter(username=temp_username):
                temp_username = f"{temp_username}{random.randint(0, 9)}"
            self.username = temp_username

    def check_email(self):
        if self.email:
            normalize_email = self.email.lower()  # aKhamdjon@gmail.com -> akhamdjon@gmail.com
            self.email = normalize_email

    # parolga tasodifiy qiymat berib turadi
    def check_pass(self):
        if not self.password:
            temp_password = f'pass-{uuid.uuid4().__str__().split("-")[-1]}'  # 123456mfdsjfkd
            self.password = temp_password

    # parolni heshlaydi
    def hashing_password(self):
        if not self.password.startswith('pbkdf2_sha256'):
            self.set_password(self.password)

    # tokenlarni olib beradi
    def token(self):
        refresh = RefreshToken.for_user(self)
        return {
            "access": str(refresh.access_token),
            "refresh_token": str(refresh)
        }

    def save(self, *args, **kwargs):
        self.clean()
        super(Users, self).save(*args, **kwargs)

    # hamma metodlarni tartib bilan ishga tushiradi
    def clean(self):
        self.check_email()
        self.check_username()
        self.check_pass()
        self.hashing_password()


PHONE_EXPIRE = 5
EMAIL_EXPIRE = 5


# Code yaratib va uni userga saqlash u-n
class UserConfirmation(BaseModel):
    TYPE_CHOICES = (
        (VIA_PHONE, VIA_PHONE),
        (VIA_EMAIL, VIA_EMAIL)
    )
    code = models.CharField(max_length=4)
    verify_type = models.CharField(max_length=31, choices=TYPE_CHOICES)
    user = models.ForeignKey(Users, models.CASCADE, related_name='verify_codes')
    expiration_time = models.DateTimeField(null=True)
    is_confirmed = models.BooleanField(default=False)

    def __str__(self):
        return str(self.user.__str__())

    # yaratilgan codni yaroqlilik muddatini belgilaydi
    def save(self, *args, **kwargs):
        if self.verify_type == VIA_EMAIL:  # 30-mart 11-33 + 5minutes
            self.expiration_time = datetime.now() + timedelta(minutes=EMAIL_EXPIRE)
        else:
            self.expiration_time = datetime.now() + timedelta(minutes=PHONE_EXPIRE)
        super(UserConfirmation, self).save(*args, **kwargs)


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
