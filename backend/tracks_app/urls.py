# manually created urls.py file

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from tracks_app import views

urlpatterns = [
    path('tracks/', views.TracksList.as_view()),
    # only return samples to anon users
    path('sample-tracks/', views.SampleTracksList.as_view()),
] 