from django.db import models

class UserProfile(models.Model):
    username = models.CharField(max_length=50)
    email = models.EmailField(max_length=100)
    password = models.CharField(max_length=50)
    region = models.CharField(max_length=50)
    comuna = models.CharField(max_length=50)
    Smart_id = models.CharField(max_length=50)
    Smart_tkn = models.CharField(max_length=50)

def create_user(self, username, email, password, region, comuna, Smart_id, Smart_tkn ):
        
        if not email:
            raise ValueError('Users must have an email address')
        
        email = self.model(email=self.normalize_email(email))
        user = self.model(username=username, email=email, region=region, comuna=comuna, Smart_id=Smart_id, Smart_tkn=Smart_tkn)
        user.set_password(password)
        user.save()
        return user