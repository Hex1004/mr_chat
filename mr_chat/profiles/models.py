from django.db import models
from django.contrib.auth.models import User
import uuid
from django.contrib.auth.hashers import make_password
from django.utils.crypto import get_random_string


class Profile(models.Model):
    username = models.CharField(max_length=20, unique=True)
    password = models.CharField(max_length=128)  # Securely hashed passwords
    email = models.EmailField(unique=True)

    def __str__(self):
        return self.username

    def set_password(self, raw_password):
        """Hash and set the password."""
        self.password = make_password(raw_password)

