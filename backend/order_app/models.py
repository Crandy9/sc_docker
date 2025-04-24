# import lctec custom user
from django.contrib.auth import get_user_model
from django.db import models

# import flps/tracks models
from flps_app.models import Flp
from tracks_app.models import Track


# set up logger
import logging
import os
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# create file handler and set level to INFO
log_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'orders_app_logs.txt')
fh = logging.FileHandler(log_file)
fh.setLevel(logging.INFO)

# create formatter
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
fh.setFormatter(formatter)
logger.addHandler(fh)

# connect orders to users
User = get_user_model()

# order model with customer's billing info
class Order(models.Model):
    user = models.ForeignKey(User, related_name='orders', on_delete=models.CASCADE)
    name = models.CharField(max_length=100, null=True, blank=True)
    email = models.CharField(max_length=100, null=True, blank=True)
    phone = models.CharField(max_length=100, null=True, blank=True)
    address1 = models.CharField(max_length=100, null=True, blank=True)
    address2 = models.CharField(max_length=100, null=True, blank=True)
    statePref = models.CharField(max_length=100, null=True, blank=True)
    country = models.CharField(max_length=100, null=True, blank=True)
    zipcode = models.CharField(max_length=100, null=True, blank=True)
    date_order_created = models.DateTimeField(auto_now=True)
    usd_paid_amount= models.DecimalField(default=0, max_digits=8, decimal_places=2, blank=True, null=True)
    jpy_paid_amount = models.IntegerField(default=0, null=True, blank=True)
    free_download = models.BooleanField(default=False, null= True, blank=True)
    stripe_token = models.CharField(max_length=100, null=True, blank=True)
    track = models.ManyToManyField(Track, related_name='track_orders', default=None, blank=True)
    flp = models.ManyToManyField(Flp, related_name='flp_orders', default=None, blank=True)

    class Meta: 
        db_table = 'orders'
        verbose_name = "Order"
        verbose_name_plural = "Orders"

    # def __str__(self):

    #     dtformat = self.date_order_created.strftime("%Y/%m/%d, %H:%M:%S")
    #     # string representation of object using name
    #     if self.free_download is True:
    #         return "(free) Order ID: " + '%s' % self.id + f' - User: {self.user.username} - Order Date: ' + str(dtformat)
    #     elif self.usd_paid_amount > 0:
    #         return "Order ID: " + '%s' % self.id + f' User: {self.user.username} Order Date: ' + str(dtformat) + ' - Subtotal: $' + str(self.usd_paid_amount)
    #     elif self.jpy_paid_amount > 0:
    #         return "Order ID: " + '%s' % self.id + f' User: {self.user.username} Order Date: ' + str(dtformat) + ' - Subtotal: ¥' + str(self.jpy_paid_amount)