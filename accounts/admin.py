from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group

from .models import User, Profile

admin.site.register(User, UserAdmin)
admin.site.unregister(Group)


class ProfileAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Personal info', {'fields': ('user', 'birth_date',
                                      'country', 'city')}),
        ('Status', {'fields': ('email_confirmed',)}),
    )
    list_display = ('id', 'user', 'email_confirmed')

admin.site.register(Profile, ProfileAdmin)
