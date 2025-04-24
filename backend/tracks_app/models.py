import datetime
from django.db import models
from sheriff_crandy_project import settings, dev_settings
# audio libs
from pydub import AudioSegment
from django.core.files import File
from pathlib import Path
import os
import shutil
import subprocess
# img processing libs
from PIL import Image
from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFill
import zipfile
import subprocess



# set up logger
import logging
import os
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# create file handler and set level to INFO
log_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'tracks_app.txt')
fh = logging.FileHandler(log_file)
fh.setLevel(logging.INFO)

# create formatter
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
fh.setFormatter(formatter)
logger.addHandler(fh)

class Track(models.Model):

    # track name
    title = models.CharField(default='', max_length=255)
    # description (not req'd)
    description = models.CharField(default='', max_length=255, blank=True, null=True)
    # price usd
    usd_price = models.DecimalField(default =0, max_digits=10, decimal_places=2, blank=True, null=True)
    # price jpy
    jpy_price = models.IntegerField(default =0, blank=True, null=True)
    # aURL ddress of song title
    slug = models.SlugField()
    # song files
    # blank=True is for forms (like admin page)
    # null=True is for null values in DB
    # uploads to /media/tracks dir
    track = models.FileField(upload_to='tracks', blank=True, null=True)
    opus_track = models.FileField(upload_to='opus_tracks', blank=True, null=True)
    # sample (approx 30 seconds preview of song to prevent free downloads)
    # uploads to /media/samples dir
    sample = models.FileField(upload_to='samples', blank=True, null=True)
    # thumbail for audio track art
    # uploads to /media/cover_art dir
    # cover_art = models.ImageField(upload_to='cover_art', blank=True, null=True)
    # django image processor automatically resizes images when uploaded
    cover_art_v2 = ProcessedImageField(upload_to='cover_art', blank=True, null=True, processors=[ResizeToFill(2048, 2048)], format='JPEG', options={'quality': 90},max_length=255)
    # datetime stamp
    date_added = models.DateTimeField(auto_now_add=True)
    # check if download is free
    is_free = models.BooleanField(default=False, blank=True, null=True)
    # track length
    song_dur = models.CharField(default='',max_length=255, null=True, blank=True)
    downloads = models.IntegerField(default=0, blank=True)


    # order Tracks by title in the backend
    class Meta:
        db_table = 'tracks'

    # when deleting a track, remove the tracks, samples, cover_art, and opus_tracks associated files 
    def delete(self, *args, **kwargs):

        if self.track:
            track_path = os.path.join(settings.MEDIA_ROOT, str(self.track))
            if os.path.exists(track_path):
                os.remove(track_path)
        if self.opus_track:
            opus_track_path = os.path.join(settings.MEDIA_ROOT, str(self.opus_track))
            if os.path.exists(opus_track_path):
                os.remove(opus_track_path)
        if self.sample:
            sample_path = os.path.join(settings.MEDIA_ROOT, str(self.sample))
            if os.path.exists(sample_path):
                os.remove(sample_path)
        if self.cover_art_v2:
            cover_art_path = os.path.join(settings.MEDIA_ROOT, str(self.cover_art_v2))
            if os.path.exists(cover_art_path):
                os.remove(cover_art_path)

        super(Track, self).delete(*args, **kwargs)

    # similiar to what we're doing when deleting. We're replacing tracks in the filesystem as well
    def save(self, *args, **kwargs):

        # Check if the track is being updated
        try:
            existing_track = Track.objects.get(pk=self.pk)
            # Check if each field is being updated and delete the associated file
            if existing_track.track != self.track:
                existing_track_path = os.path.join(settings.MEDIA_ROOT, str(existing_track.track))
                if os.path.exists(existing_track_path):
                    os.remove(existing_track_path)

            if existing_track.opus_track != self.opus_track:
                existing_opus_track_path = os.path.join(settings.MEDIA_ROOT, str(existing_track.opus_track))
                if os.path.exists(existing_opus_track_path):
                    os.remove(existing_opus_track_path)

            if existing_track.sample != self.sample:
                existing_sample_path = os.path.join(settings.MEDIA_ROOT, str(existing_track.sample))
                if os.path.exists(existing_sample_path):
                    os.remove(existing_sample_path)

            if existing_track.cover_art_v2 != self.cover_art_v2:
                existing_cover_art_path = os.path.join(settings.MEDIA_ROOT, str(existing_track.cover_art_v2))
                if os.path.exists(existing_cover_art_path):
                    os.remove(existing_cover_art_path)
        except:
            pass

        super(Track, self).save(*args, **kwargs)


    def __str__(self):
        if self.is_free is True:
            return '(free) ' + self.title + ' - Downloads: ' + str(self.downloads)
        else:
            return self.title + ' - Downloads: ' + str(self.downloads)
    
    # get url of track for frontend
    def get_absolute_url(self):
        return f'/{self.slug}/'

    # get all static files (images, audio tracks, etc) for frontend
    def get_track(self):
        if self.track:
            if settings.env('DEV_MODE') == 'True':
                return settings.env('DEV_DOMAIN') + self.track.url
            else:
                return settings.env('DOMAIN') + self.track.url
        return ''
    
    def get_sample(self):
        # if this sample is already created
        if self.sample:
            if settings.env('DEV_MODE') == 'True':
                return settings.env('DEV_DOMAIN') + self.sample.url
            else:
                return settings.env('DOMAIN') + self.sample.url
        # else if the song is uploaded but the sample hasn't been created, create it and save it to DB
        else:
            if self.track:
                self.sample = self.make_sample(self.track)
                if self.sample and self.sample.file:
                    self.save()
                    if settings.env('DEV_MODE') == 'True':
                        return settings.env('DEV_DOMAIN') + self.sample.url
                    else:
                        return settings.env('DOMAIN') + self.sample.url
        # else if the track isn't created, return an empty string
        return ''

    # need to resize images to 2048px x 2048px
    def get_cover_art(self):
        if self.cover_art_v2:
            if settings.env('DEV_MODE') == 'True':
                return settings.env('DEV_DOMAIN') + self.cover_art_v2.url
            else:
                return settings.env('DOMAIN') + self.cover_art_v2.url
        return ''

    # get the length of the track in mm:ss
    # should be the same for opus, don't need to call this twice
    def get_track_duration(self):
        if self.song_dur:
            return self.song_dur
        else:
            if self.track:
                self.song_dur = self.track_duration(self.track)
                self.save()
                return self.song_dur
        return ''


    # generate the 30 second splice sample
    # audio file product model check out pydub https://github.com/jiaaro/pydub
    # also used https://hvitis.dev/how-to-convert-audio-files-with-python-and-django
    def make_sample(self, track):
        # make a new temp path var to temporarily store the sample
        tmp_path = '/tmp/'
        # track dir
        song_full_path = str(track)
        song_file = song_full_path.replace('tracks/','')
        song_name = ''
        full_song = ''

        if 'wav' in song_file:
            song_name = song_file.replace('.wav','')
            full_song = AudioSegment.from_wav(track)

        elif 'mp3' in song_file:
            song_name = song_file.replace('.mp3','')
            full_song = AudioSegment.from_mp3(track)


        # 50 seconds (in miliseconds)
        if full_song.duration_seconds > 50:
            song_limit = 50 * 1000
            sample = full_song[:song_limit]
        else:
            song_limit = 30 * 1000
            sample = full_song[:song_limit]

        # fade in/out the sample
        faded_sample = sample.fade_in(2000).fade_out(3000)
        
        # full sample path
        sample_path = tmp_path + song_name + "_sample.mp3"

        # export to /tmp path
        try:
            faded_sample.export(sample_path, format="mp3")
        # couldn't export file
        except:
            return ''

        # now open that sample as a file object so Django can read it
        try:
            converted_sample = File(
                    file=open(sample_path, 'rb'),
                    name=Path(sample_path)
                )
        # TODO when file couldn't be opened
        except:
            return ''
        # don't know if I need these lines
        converted_sample.name = Path(sample_path).name
        converted_sample.content_type = 'audio/mpeg'
        converted_sample.size = os.path.getsize(sample_path)

        # finally delete the sample file in /tmp/ dir
        try:
            os.remove(sample_path)
        except:
            return ''
        

        return converted_sample
    

    def track_duration(self, track):

        # Get the file name from the FieldFile object
        song_full_path = str(track)
        song_file = song_full_path.replace('tracks/','')


        if ".wav" in song_file:
            full_song = AudioSegment.from_wav(track)

        elif ".mp3" in song_file:
            full_song = AudioSegment.from_mp3(track)

            song_length = full_song.duration_seconds

        # convert song length to human-readable
        human_readable_song_length = str(datetime.timedelta(seconds=song_length))

        # min and seconds only
        if human_readable_song_length[2] == '0':
            min_secs = human_readable_song_length[3:-7]
        else:            
            min_secs = human_readable_song_length[2:-7]

        return min_secs