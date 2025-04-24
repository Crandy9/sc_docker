from django.urls import path

from order_app import views

urlpatterns = [
    
    # multifile cart checkout
    path('checkout/cart/<int:id>/<str:isSingleFile>/<str:isfree>', views.cartCheckout),
    # track checkout
    path('checkout/track/<int:id>/<str:isfree>', views.trackCheckout),
    # flp checkout
    path('checkout/flp/<int:id>/<str:isfree>', views.flpCheckout),    
    path('get_track_orders/', views.get_track_orders)
]