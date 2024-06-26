import hashlib
import os

from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.db import models
from PIL import Image

# Create your models here.
from django.db.models.signals import post_save
from django.dispatch import receiver

from Fallstudie_Calendar import settings


class MyAccountManager(BaseUserManager):

    def create_user(self, email, username, password, profile_image=None):
        user = self.model(email=email, username=username, profile_image=profile_image)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password, profile_image=None):
        user = self.create_user(email=email, username=username, profile_image=profile_image, password=password)
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


def upload_location(instance, filename, **kwargs):
    file_path = 'profile_images/{filename}'.format(
        filename=hashlib.md5(str(instance.email).encode()).hexdigest() + os.path.splitext(filename)[1]
    )
    return file_path


class Account(AbstractBaseUser):
    # person
    id = models.AutoField(primary_key=True)
    email = models.EmailField(verbose_name="E-Mail", max_length=60, unique=True)
    username = models.CharField(verbose_name="username", max_length=20)
    profile_image = models.ImageField(upload_to=upload_location, null=True, blank=True)

    # necessary
    date_joined = models.DateTimeField(verbose_name="date joined", auto_now_add=True)
    last_login = models.DateTimeField(verbose_name="last login", auto_now_add=True)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    # to use email as a login field
    USERNAME_FIELD = 'email'

    REQUIRED_FIELDS = ["username"]

    objects = MyAccountManager()

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def post_save_compress_img(sender, instance, *args, **kwargs):
    if instance.profile_image:
        picture = Image.open(instance.profile_image.path)
        picture.save(instance.profile_image.path, optimize=True, quality=30)