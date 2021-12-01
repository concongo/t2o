from django.db import models
from django.utils import timezone


# Create your models here.
class Order(models.Model):
    '''
    Model Class for storing Orders from the Order Book
    '''

    num = models.BigIntegerField(primary_key=True, blank=False, default=0)
    side = models.CharField(blank=False, default='Ask', max_length=3)
    symbol = models.CharField(blank=False, default='', max_length=15)
    px = models.FloatField(blank=False, default=0)
    qty = models.FloatField(blank=False, default=0)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)

    class Meta:
        ordering = ('side', 'symbol', 'px',)
        verbose_name = 'Order'
        verbose_name_plural = 'Orders'
