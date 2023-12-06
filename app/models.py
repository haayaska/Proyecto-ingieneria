from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

class UserProfileManager(BaseUserManager):
    def create_user(self, username, email, password, region, comuna, Smart_id, Smart_tkn, consumo):
        if not email:
            raise ValueError('Users must have an email address')

        email = self.normalize_email(email)
        user = self.model(username=username, email=email, password=password, region=region, comuna=comuna, Smart_id=Smart_id, Smart_tkn=Smart_tkn, consumo=consumo)
        user.save()
        return user
    
    def create_superuser(self, email, username, password=None, region=None, comuna=None, Smart_id=None, Smart_tkn=None, consumo=None):
        user = self.create_user(email, username, password, region, comuna, Smart_id, Smart_tkn, consumo)
        user.is_staff = True
        user.is_superuser = True
        user.save()
        return user

class UserProfile(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=50, unique=True)
    email = models.EmailField(max_length=100, unique=True)
    password = models.CharField(max_length=50)
    region = models.CharField(max_length=50)
    comuna = models.CharField(max_length=50)
    Smart_id = models.CharField(max_length=50)
    Smart_tkn = models.CharField(max_length=50)
    consumo = models.DecimalField(decimal_places=0, max_digits=60, default=0)
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)
    objects = UserProfileManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    def __str__(self):
        return self.email
    

    