# python manage.py runserver 8001

from django.db import models

from .cryptography import *

class Users(models.Model):
    pri_key, pub_key = rsakeys()

    user_id = models.BigAutoField(primary_key=True)
    username = models.CharField(unique=True, max_length=25)
    password = models.TextField(max_length=250)
    private_key = models.TextField(default=pri_key)
    public_key = models.TextField(default=pub_key)
