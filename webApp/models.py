from django.db import models

from .cryptography import *

class Users(models.Model):
    pri_key, pub_key = rsakeys()

    user_id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=25)
    username = models.CharField(unique=True, max_length=25)
    email = models.EmailField(unique=True)
    password = models.TextField(max_length=250)
    private_key = models.TextField(default=pri_key)
    # public_key = models.TextField(default=pub_key)
