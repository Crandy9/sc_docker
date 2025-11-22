from django.shortcuts import render
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import *
from .serializers import *


# set up logger
import logging
import os
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# create file handler and set level to INFO
import logging
logger = logging.getLogger('main')

# get sample_tracks only
class SampleTracksList(APIView):

    # get music objects
    def get(self, request, format=None):

        # Get sample tracks (all tracks excluding free tracks)
        sample_tracks = Track.objects.exclude(is_free=True)
        
        # Get full free tracks
        free_tracks = Track.objects.filter(is_free=True)

        # Concatenate the queryset of sample tracks and full free tracks
        tracks = sample_tracks | free_tracks

        # convert these objects into JSON. Pass in tracks and set many=True because we have more than one obj
        serializer = SampleTrackSerializer(tracks, many=True)

        return Response(serializer.data)

# get newest songs using APIView from django rest_framework
class TracksList(APIView):

    # authentication_classes = [TokenAuthentication]
    # permission_classes = [IsAuthenticated]
    # get music objects
    def get(self, request, format=None):

        tracks = Track.objects.all()

        # convert these objects into JSON. Pass in tracks and set many=True because we have more than one obj
        serializer = TrackSerializer(tracks, many=True)
        return Response(serializer.data)