from django.db import models

class UserProfile(models.Model):
    username = models.CharField(max_length=50)
    email = models.EmailField()
    password = models.CharField(max_length=50)
    region = models.CharField(max_length=50)
    comuna = models.CharField(max_length=50)
    Smart_id = models.CharField(max_length=50)
    Smart_tkn = models.CharField(max_length=50)
