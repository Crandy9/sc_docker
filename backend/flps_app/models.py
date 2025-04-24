import datetime
from django.db import models
from sheriff_crandy_project import settings
# audio libs
from pydub import AudioSegment
from django.core.files import File
from pathlib import Path
import os


# set up logger
import logging
import os
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# create file handler and set level to INFO
log_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'flps_app.txt')
fh = logging.FileHandler(log_file)
fh.setLevel(logging.INFO)

# create formatter
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
fh.setFormatter(formatter)
logger.addHandler(fh)

class Flp(models.Model):

    flp_name = models.CharField(default='', max_length=255)
    description = models.CharField(default='', max_length=255, blank=True, null=True)
    usd_price = models.DecimalField(default =0, max_digits=10, decimal_places=2, blank=True, null=True)
    jpy_price = models.IntegerField(default =0, blank=True, null=True)
    slug = models.SlugField()
    flp_zip = models.FileField(upload_to='flp_zips', blank=True, null=True)
    date_added = models.DateTimeField(auto_now_add=True)
    # calling it flp_is_free to distinguish from free tracks in frontend
    flp_is_free = models.BooleanField(default=False, blank=True, null=True)
    downloads = models.IntegerField(default=0, blank=True)

    class Meta:
        db_table = 'flps'

    # when deleting an flp, remove the flp_zips associated file
    def delete(self, *args, **kwargs):

        if self.flp_zip:
            flp_zip_path = os.path.join(settings.MEDIA_ROOT, str(self.flp_zip))
            if os.path.exists(flp_zip_path):
                os.remove(flp_zip_path)

        super(Flp, self).delete(*args, **kwargs)        

    # similiar to what we're doing when deleting. We're replacing tracks in the filesystem as well
    def save(self, *args, **kwargs):

        # Check if the track is being updated
        try:

            existing_flp = Flp.objects.get(pk=self.pk)
            # Check if each field is being updated and delete the associated file
            if existing_flp.flp_zip != self.flp_zip:
                existing_flp_path = os.path.join(settings.MEDIA_ROOT, str(existing_flp.flp_zip))
                if os.path.exists(existing_flp_path):
                    os.remove(existing_flp_path)
        except:
            pass
        super(Flp, self).save(*args, **kwargs)        

    # def __str__(self):
    #     if self.flp_is_free is True:
    #         return '(free) ' + self.flp_name + ' - Downloads: ' + str(self.downloads)
    #     else:
    #         return self.flp_name + ' - Downloads: ' + str(self.downloads)
    
    def get_absolute_url(self):
        return f'/{self.slug}/'

    # get flp_zip files
    def get_zips(self):
        if self.flp_zip:

            if settings.env('DEV_MODE') == 'True':
                return settings.env('DEV_DOMAIN') + self.flp_zip.url
            else:
                return settings.env('DOMAIN') + self.flp_zip.url

        return ''