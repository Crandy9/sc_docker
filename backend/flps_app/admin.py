from django.contrib import admin
from .models import *

@admin.register(Flp)
class AdminClassName(admin.ModelAdmin):
    list_display = ('flp_name', 'flp_is_free')
    readonly_fields = ['pk', 'downloads', 'date_added']