# python manage.py runserver 8001

from django.db import models


class Users(models.Model):

    user_id = models.BigAutoField(primary_key=True)
    username = models.CharField(unique=True, max_length=25)
    password = models.TextField(max_length=250)
    
