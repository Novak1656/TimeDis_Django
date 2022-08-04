from django.contrib.auth.models import AbstractUser
from django.db import models


class Users(AbstractUser):
    email = models.EmailField('Email', unique=True)
    date_of_birth = models.DateField('Дата рождения', null=True, blank=True)

    def __str__(self):
        return self.username
