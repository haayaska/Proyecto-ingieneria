from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

class UserProfileManager(BaseUserManager):
    def create_user(self, username, email, password, region, comuna, Smart_id, Smart_tkn):
        if not email:
            raise ValueError('Users must have an email address')

        email = self.normalize_email(email)
        user = self.model(username=username, email=email, password=password, region=region, comuna=comuna, Smart_id=Smart_id, Smart_tkn=Smart_tkn)
        user.save()
        return user

class UserProfile(models.Model):
    username = models.CharField(max_length=50)
    email = models.EmailField(max_length=100)
    password = models.CharField(max_length=50)
    region = models.CharField(max_length=50)
    comuna = models.CharField(max_length=50)
    Smart_id = models.CharField(max_length=50)
    Smart_tkn = models.CharField(max_length=50)

    objects = UserProfileManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.username
