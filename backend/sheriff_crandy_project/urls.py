from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
# needed to check if we are in development mode
import environ
env = environ.Env()
environ.Env.read_env()

# 'api/' is the URL endpoint nginx will serve the Django backend API
# need to change vuejs VUE_APP_BACKEND_URL env var to
# VUE_APP_BACKEND_URL=https://sheriffcrandymusic.local:9443/api


urlpatterns = [
    path('api/sheriffcrandyadmin-6A6573757363687269737469736B696E67/', admin.site.urls),
    # djoser library is a REST implementation of Django authentication system
    path('api/sc/v1/', include('djoser.urls')),
    path('api/sc/v1/', include('djoser.urls.authtoken')),
    # include tracks app urls --can check api at http://localhost:8000/v1/tracks/
    path('api/sc/v1/', include ('tracks_app.urls')),
    path('api/sc/v1/', include ('flps_app.urls')),
    path('api/sc/v1/', include ('order_app.urls')),
    path('api/sc/v1/', include ('lctec_user.urls')),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# yellow header title and login title
admin.site.site_header = 'Sheriff Crandy Music Admin Portal'
# white header under and left side browser tab title
admin.site.index_title = ' '
# right side browser tab title
admin.site.site_title = 'Admin'