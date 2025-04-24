from django.contrib import admin
from .models import Lctec_User, Cart


# Register your models here.
# @admin.register(Lctec_User)
# class CustomUserAdmin(admin.ModelAdmin):
#     list_display = (
#         'username',
#     )
#     readonly_fields = ['id','date_added']


from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import Lctec_User

class CustomUserAdmin(BaseUserAdmin):
    # Define fieldsets to control the layout of the "change" form.
    fieldsets = (
        ('User Info', {
            'fields': ('username', 'email', 'password', 'id', 'date_added', 'last_login')
            }
        ),
        ('Personal info', {
            'fields': ('first_name', 'last_name', 'profile_pic', 'favorite_color')
            }
        ),
        ('Permissions', {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')
            }
        ),
    )

    # When adding a new user in the admin page
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 
                       'first_name', 
                       'last_name',
                       'profile_pic',
                       'favorite_color',
                       'password1', 
                       'password2',
                       'is_staff',
                       'is_superuser',
                       'is_active'),
        }),
    )

    # Define read-only fields
    readonly_fields = ['date_added','id',]
    # how users are displayed in Admin page
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff')
    search_fields = ('username', 'email', 'first_name', 'last_name')
    ordering = ('username',)

admin.site.register(Lctec_User, CustomUserAdmin)



@admin.register(Cart)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('cart_name', 'Flps', 'Tracks')
    readonly_fields = ['id',]

    def cart_name(self, obj):
        return obj.user.username + "'s cart" + " (" + str(obj.total_cart_quantity) + ")"

    def Flps(self, obj):
        return ", ".join([flp.flp_name for flp in obj.flps_in_cart.all()])

    def Tracks(self, obj):
        return ", ".join([track.title for track in obj.tracks_in_cart.all()])