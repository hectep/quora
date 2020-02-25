from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from profiles.models import Profile


class ProfileAdmin(UserAdmin):
    model = Profile
    list_display = ['username', 'email', 'is_staff']


admin.site.register(Profile, ProfileAdmin)
