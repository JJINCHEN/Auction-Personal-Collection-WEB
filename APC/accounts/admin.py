from django.contrib import admin
from .models import UserProfile


# Register your models here.


class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'mtype', 'money')
    list_filter = ['mtype']
    list_editable = ["mtype"]
    search_fields = ['username']


admin.site.register(UserProfile, UserProfileAdmin)