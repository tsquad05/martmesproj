from django.contrib import admin
from .models import User
from django.contrib.auth.models import Group

admin.site.unregister(Group)

class UserAdmin(admin.ModelAdmin):
    list_display = ['full_name','email',"phone_number"]

admin.site.register(User, UserAdmin)

admin.site.site_header = 'Martmes Administration'