from django.contrib import admin
from .models import *

@admin.register(Track)
class AdminClassName(admin.ModelAdmin):
    
    list_display = ('title', 'song_dur', 'is_free')
    readonly_fields = ['pk', 'sample','song_dur', 'downloads','date_added']