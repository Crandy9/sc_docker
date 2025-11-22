from django.contrib import admin
from .models import Order, AnonOrder


# Register your models here.
@admin.register(Order)
class AdminClassName(admin.ModelAdmin):
    list_display = ('user', 'stripe_token', 'get_track_titles', 'get_flp_titles', 'usd_paid_amount', 'jpy_paid_amount', 'date_order_created')

    readonly_fields = ['date_order_created', 'id']

    def get_track_titles(self, obj):
        # Get all tracks associated with the order
        tracks = obj.track.all()

        # Concatenate titles of all tracks into a single string
        track_titles = ', '.join(track.title for track in tracks)

        return track_titles if track_titles else "No Tracks"    
    
    def get_flp_titles(self, obj):
        # Get all tracks associated with the order
        flps = obj.flp.all()

        # Concatenate titles of all tracks into a single string
        flp_titles = ', '.join(flp.flp_name for flp in flps)

        return flp_titles if flp_titles else "No FLPs"        
    
    get_track_titles.short_description = 'Tracks'
    get_flp_titles.short_description = 'Flps'


@admin.register(AnonOrder)
class AdminClassName(admin.ModelAdmin):
    list_display = ('stripe_token', 'get_track_titles', 'get_flp_titles', 'usd_paid_amount', 'jpy_paid_amount', 'date_order_created')

    readonly_fields = ['date_order_created', 'id']

    def get_track_titles(self, obj):
        # Get all tracks associated with the order
        tracks = obj.track.all()

        # Concatenate titles of all tracks into a single string
        track_titles = ', '.join(track.title for track in tracks)

        return track_titles if track_titles else "No Tracks"    
    
    def get_flp_titles(self, obj):
        # Get all tracks associated with the order
        flps = obj.flp.all()

        # Concatenate titles of all tracks into a single string
        flp_titles = ', '.join(flp.flp_name for flp in flps)

        return flp_titles if flp_titles else "No FLPs"        
    
    get_track_titles.short_description = 'Tracks'
    get_flp_titles.short_description = 'Flps'    