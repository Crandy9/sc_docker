# manually created serializers.py file created to turn DB data into JSON to be used by frontend
from rest_framework import serializers
from .models import *
# import User
from django.contrib.auth.models import User

# flps
class LimitedFlpSerializer(serializers.ModelSerializer):
    class Meta:
        model = Flp 
        fields = (
            "id",
            "flp_name",
            # "flp_zip",
            # "get_absolute_url",
            "description",
            "usd_price",
            "jpy_price",         
            # "date_added",
            "flp_is_free",
        )

# flps
class FlpSerializer(serializers.ModelSerializer):
    class Meta:
        model = Flp 
        fields = (
            "id",
            "flp_name",
            "flp_zip",
            "get_absolute_url",
            "description",
            "usd_price",
            "jpy_price",         
            "get_zips",
            "date_added",
            "flp_is_free",
        )