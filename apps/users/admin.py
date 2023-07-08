from django.contrib import admin

from .models import UserProfile


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):

    list_display = ('id','username','name','birthday','gender','email')
    '''filter options'''
    list_filter = ('username', )
    list_per_page = 10

