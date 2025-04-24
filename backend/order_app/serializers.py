# manually created serializers.py file created to turn DB data into JSON to be used by frontend
from rest_framework import serializers
# from .models import Order, OrderFlpItem, OrderTrackItem
from .models import Order

# import serializers from flp and track apps
# from flps_app.serializers import FlpSerializer
# from tracks_app.serializers import TrackSerializer
from tracks_app.models import Track
from flps_app.models import Flp



# import logger
import logging

# Get the logger named 'main' as defined in settings.py
logger = logging.getLogger('main')


# OrderItem Flp Serializer
# class OrderItemFlpSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = OrderFlpItem
#         fields = (
#             "flp",
#         )

# OrderItem Track Serializer
# class OrderItemTrackSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = OrderTrackItem
#         fields = (
#             "track",
#         )

        
# Order Flp Serializer
class OrderFlpSerializer(serializers.ModelSerializer):

    flp_items = serializers.ListField(child=serializers.DictField())

    class Meta:
        model = Order
        fields = (
            "id",
            "name",
            "email",
            "phone",
            "address1",
            "address2",
            "statePref",
            "country",
            "zipcode",
            "stripe_token",
            "flp_items",
        )

    def create(self, validated_data):
        flp_items = validated_data.pop('flp_items')
        order = Order.objects.create(**validated_data)

        flps = []
        for flp_item in flp_items:
            flp_pk = flp_item.get('flp')
            flp = Flp.objects.get(pk=flp_pk)
            order.flp.add(flp)
            flps.append(flp)

        return flps


# Order Track Serializer
class OrderTrackSerializer(serializers.ModelSerializer):
    
    track_items = serializers.ListField(child=serializers.DictField())
    class Meta:
        model = Order
        fields = (
            "id",
            "name",
            "email",
            "phone",
            "address1",
            "address2",
            "statePref",
            "country",
            "zipcode",
            "stripe_token",
            "track_items"
        )

    def create(self, validated_data):
        track_items = validated_data.pop('track_items')
        order = Order.objects.create(**validated_data)

        tracks = []
        for track_item in track_items:
            track_pk = track_item.get('track')
            track = Track.objects.get(pk=track_pk)
            order.track.add(track)
            tracks.append(track)

        return tracks