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
log_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'flps_app.txt')
fh = logging.FileHandler(log_file)
fh.setLevel(logging.INFO)

# create formatter
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
fh.setFormatter(formatter)
logger.addHandler(fh)


# get limited flps using APIView from django rest_framework
class LimitedFlpsList(APIView):
    
    def get(self, request, format=None):
        flps = Flp.objects.all()
        serializer = LimitedFlpSerializer(flps, many=True)
        return Response(serializer.data)

# get newest flps using APIView from django rest_framework
class FlpsList(APIView):
    
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self, request, format=None):
        flps = Flp.objects.all()
        serializer = FlpSerializer(flps, many=True)
        return Response(serializer.data)