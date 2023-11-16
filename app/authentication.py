from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model

class CustomEmailBackend(ModelBackend):
    def authenticate(self, request, email=None, password=None, **kwargs):
        print(email, password)
        UserModel = get_user_model()
        try:
            user = UserModel.objects.get(email=email)
            
        except UserModel.DoesNotExist:
            print(UserModel)
            print('adios')
            return None

        if user.check_password(password):
            print('hola')
            return user

    def get_user(self, user_id):
        UserModel = get_user_model()
        try:
            return UserModel.objects.get(pk=user_id)
        except UserModel.DoesNotExist:
            return None
