from django.contrib import admin
from .models import UserProfile

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display=('username', 'Smart_tkn', 'Smart_id')
    search_fields = ('username',)
