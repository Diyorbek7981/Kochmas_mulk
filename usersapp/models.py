from django.contrib.auth.models import AbstractUser
from django.db import models
import random
import uuid  # takrorlanishlar ehtimoli kam
from django.core.validators import FileExtensionValidator, MaxLengthValidator
from datetime import datetime, timedelta

from rest_framework_simplejwt.tokens import RefreshToken


# Users uchun--------------------------------->
class BaseModel(models.Model):
    id = models.UUIDField(unique=True, default=uuid.uuid4, editable=False, primary_key=True)
    created_time = models.DateTimeField(auto_now_add=True)
    updated_time = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


# Create your models here.
ORDINARY_USER, MANAGER, ADMIN = ("ordinary_user", 'manager', 'admin')
VIA_EMAIL, VIA_PHONE = ("via_email", "via_phone")
NEW, CODE_VERIFIED, DONE, PHOTO_DONE, FORGET_PASS, NEW_PHONE = ('new', 'code_verified', 'done',
                                                                'photo_done', 'forget_password', 'new_phone')


class Users(AbstractUser, BaseModel):
    USER_ROLES = (
        (ORDINARY_USER, ORDINARY_USER),
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
        (PHOTO_DONE, PHOTO_DONE),
        (FORGET_PASS, FORGET_PASS)
    )

    user_roles = models.CharField(max_length=31,
                                  choices=USER_ROLES,
                                  default=ORDINARY_USER)
    auth_type = models.CharField(max_length=31,
                                 choices=AUTH_TYPE_CHOICES)
    auth_status = models.CharField(max_length=31,
                                   choices=AUTH_STATUS,
                                   default=NEW)  # signup jarayonini birin-ketin bo'lishi uchun
    email = models.EmailField(null=True, blank=True, unique=True)
    phone_number = models.CharField(max_length=13, null=True, blank=True, unique=True)
    new_phone = models.CharField(max_length=13, null=True, blank=True, unique=True)
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
            code=code,
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


PHONE_EXPIRE = 2
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
    # related_name berishning sababi shu nomga murojat qilsak userga tegishli barcha codlarni olish uchun -
    # - yani user = verify_codesni barcha codlariga
    expiration_time = models.DateTimeField(null=True)
    is_confirmed = models.BooleanField(default=False)

    class Meta:
        ordering = ['-created_time']

    def __str__(self):
        return str(self.user)

    # yaratilgan codni yaroqlilik muddatini belgilaydi
    def save(self, *args, **kwargs):
        if self.verify_type == VIA_EMAIL:  # 30-mart 11-33 + 5minutes
            self.expiration_time = datetime.now() + timedelta(minutes=EMAIL_EXPIRE)
        else:
            self.expiration_time = datetime.now() + timedelta(minutes=PHONE_EXPIRE)
        super(UserConfirmation, self).save(*args, **kwargs)


class UserMessage(models.Model):
    message = models.TextField(validators=[MaxLengthValidator(1000)])
    to_user = models.ForeignKey(Users, models.CASCADE, related_name='to_user')
    the_user = models.ForeignKey(Users, models.CASCADE, related_name='from_user')
    created_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.the_user} -> {self.to_user}"
