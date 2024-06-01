import hashlib
import os

from PIL import Image
from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

from Fallstudie_Calendar import settings


def upload_location(instance, filename, **kwargs):
    file_path = 'profile_images/{filename}'.format(filename=hashlib.md5(str(instance.email).encode()).hexdigest() + os.path.splitext(filename)[1])
    return file_path


# Create your models here.
class MyAccountManager(BaseUserManager):

    def create_user(self, email, username, password, profile_image=None):
        user = self.model(email=email, username=username, profile_image=profile_image)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password, profile_image=None):
        user = self.create_user(email, username, password, profile_image)
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class Account(AbstractBaseUser):
    email = models.EmailField(verbose_name="E-Mail", max_length=60, unique=True)
    username = models.CharField(verbose_name="Username", max_length=30, unique=True)
    profile_image = models.ImageField(verbose_name="Profile Image", max_length=255, upload_to=upload_location, null=True, blank=True)

    # necessary fields
    date_joined = models.DateTimeField(verbose_name='Date Joined', auto_now_add=True)
    last_login = models.DateTimeField(verbose_name='Last Login', auto_now=True)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    # to user email as login
    USERNAME_FIELD = 'email'

    REQUIRED_FIELDS = []

    objects = MyAccountManager()

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def post_save_compress_img(sender, instance, *args, **kwargs):
    if instance.profile_image:
        picture = Image.open(instance.profile_image.path)
        picture.save(instance.profile_image.path, quality=30, optimize=True)
