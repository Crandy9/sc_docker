# manually created serializers.py file created to turn DB data into JSON to be used by frontend
from rest_framework import serializers
from .models import *
# import User
from django.contrib.auth.models import User


# sample audio files
class SampleTrackSerializer(serializers.ModelSerializer):
    class Meta:
        model = Track 
        # configure which fields we want to use in frontend. Data is a tuple
        # will be shown in API at DOMAIN/api/v1/tracks/
        fields = (
            "id",
            # "track",
            "title",
            "description",
            "usd_price",
            "jpy_price",         
            "get_sample",
            "get_cover_art",
            "is_free",
            "get_track_duration",
        )

    def to_representation(self, instance):
        data = super().to_representation(instance)
        if instance.is_free:
            data['get_track'] = instance.get_track()
        return data

# audio files
class TrackSerializer(serializers.ModelSerializer):
    class Meta:
        model = Track 
        # configure which fields we want to use in frontend. Data is a tuple
        # will be shown in API at DOMAIN/api/v1/tracks/
        fields = (
            "id",
            "track",
            "title",
            "description",
            "usd_price",
            "jpy_price",         
            "get_track",
            "get_sample",
            "get_cover_art",
            "is_free",
            "get_track_duration",
        )

# get purchased tracks
class GetPurchasedTrackSerializer(serializers.ModelSerializer):
    class Meta:
        model = Track 
        # configure which fields we want to use in frontend. Data is a tuple
        # will be shown in API at DOMAIN/api/v1/tracks/
        fields = (
            "id",
            "track",
            "opus_track",         
            "title",
            "description",      
            "get_track",
            "get_cover_art",
            "get_track_duration",
        )