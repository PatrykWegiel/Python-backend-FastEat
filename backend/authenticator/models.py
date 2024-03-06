import os
from django_resized import ResizedImageField

from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager, PermissionsMixin


def user_image_upload(instance, filename):
    path = "user/"
    file_extension = filename.split(".")[1]
    format = "user" + str(instance.id) + "." + file_extension
    return os.path.join(path, format)


class UserManager(BaseUserManager):
    def create_user(self, username, email, password):
        user = self.model(username=username, email=self.normalize_email(email))
        user.set_password(password)
        user.save()

        return user

    def create_superuser(self, username, email, password):
        user = self.create_user(username, email, password)
        user.is_superuser = True
        user.is_staff = True
        user.save()

        return user


class User(AbstractUser, PermissionsMixin):
    username = models.CharField(db_index=True, unique=True, max_length=100)
    email = models.EmailField(db_index=True, unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    image = ResizedImageField(
        size=[150, 150],
        upload_to=user_image_upload,
        null=True,
        blank=True,
        force_format="PNG",
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    objects = UserManager()

    def __str__(self):
        return self.username
