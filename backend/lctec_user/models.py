from django.db import models
# import classes needed for custom user model
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
# import tracks and flp models for cart model
from flps_app.models import Flp
from tracks_app.models import Track
from sheriff_crandy_project import settings
from django.core.files.uploadedfile import SimpleUploadedFile


# set up logger
import os


# custom user manager
class Lctec_CustomUserManager(BaseUserManager):


    # called when creating user through drf terminal and frontend
    # only pass in req params, all other unrequired params like
    # first/lastname, favorite color, etc. will be held in **extra_fields param
    def create_user(self, email, username, password, **extra_fields):

        if not email:
            raise ValueError("Email must be provided")
        if not username:
            raise ValueError("Username must be provided")

        user = Lctec_User(
            email = self.normalize_email(email),
            username = username,
            **extra_fields
        )

        print('password: ' + str(password))
        user.set_password(password)
        user.save(using=self._db)

        return user

    # called when creating superuser through terminal and presumably drf
    def create_superuser(self, email, username, password, **extra_fields):

        extra_fields.setdefault('is_staff',True)
        extra_fields.setdefault('is_superuser',True)
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        return self.create_user(email, username, password, **extra_fields)


# Custom User Model; define fields you want to be included in User Model, can be updated changed later
class Lctec_User(AbstractBaseUser, PermissionsMixin):

    # define fields you want to be included in User Model, can be updated changed later
    # authenticate with either username or email
    email = models.EmailField(db_index=True, max_length=100, unique=True)
    username = models.CharField(db_index=True, max_length=64, unique=True)

    # non-req'd fields
    first_name = models.CharField(max_length=50, blank=True, null=True)
    last_name = models.CharField(max_length=50, blank=True, null=True)
    profile_pic = models.ImageField(upload_to='pfps', blank=True, null=True)
    favorite_color = models.CharField(max_length=20, blank=True, null=True)
    date_added = models.DateTimeField(auto_now_add=True)

    # if user is allowed access to admin site. 
    is_staff = models.BooleanField(default=False)
    # if user is currently active
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)

    # connect user class to manager class
    objects = Lctec_CustomUserManager()

    # choose wisely, password resets will use this field
    # needs to have unique=True
    USERNAME_FIELD = 'username'
    # used by python manage.py createsuperuser and presumably drf for token authentication
    # should not contain the USERNAME_FIELD or password as these fields will always be prompted for.
    REQUIRED_FIELDS = ['first_name', 'last_name', 'email']

    class Meta:
        db_table = 'users'
        verbose_name = "users"
        verbose_name_plural = "Users"

    def __str__(self):
        # return self.email
        return self.username

    @staticmethod
    def has_perm(perm, obj=None, **kwargs):
        return True

    @staticmethod
    def has_module_perms(app_label, **kwargs):
        return True
    
    # delete pfp file if it exists on delete
    def delete(self, *args, **kwargs):

        if self.profile_pic:
            profile_pic_path = os.path.join(settings.MEDIA_ROOT, str(self.profile_pic))
            if os.path.exists(profile_pic_path):
                os.remove(profile_pic_path)

        super(Lctec_User, self).delete(*args, **kwargs)      

    # similiar to what we're doing when deleting. Replace previously existing pfp for new one on save
    def save(self, *args, **kwargs):

        # Check if the track is being updated
        try:
            existing_pfp = Lctec_User.objects.get(pk=self.pk)
            # Check if each field is being updated and delete the associated file
            if existing_pfp.profile_pic != self.profile_pic:
                existing_pfp_path = os.path.join(settings.MEDIA_ROOT, str(existing_pfp.profile_pic))
                if os.path.exists(existing_pfp_path):
                    os.remove(existing_pfp_path)
            
        except:
            pass
        super(Lctec_User, self).save(*args, **kwargs)           

    # get user profile pic
    def get_profile_pic(self):

        if self.profile_pic:
            if settings.env('DEV_MODE') == 'True':
                return settings.env('DEV_DOMAIN') + self.profile_pic.url
            else:
                return settings.env('DOMAIN') + self.profile_pic.url
        return ''



# set custom user model
from django.contrib.auth import get_user_model
User = get_user_model()


# user's cart
class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    flps_in_cart = models.ManyToManyField(Flp, default=None, blank=True)
    tracks_in_cart = models.ManyToManyField(Track, default=None, blank=True)
    flp_cart_quantity = models.IntegerField(default = 0, null=True, blank=True)
    track_cart_quantity = models.IntegerField(default = 0, null=True, blank=True)
    total_cart_quantity = models.IntegerField(default = 0, null=True, blank=True)

    class Meta:
        db_table = 'user_cart'