from rest_framework.test import APITestCase
from rest_framework.reverse import reverse
from rest_framework import status
from .models import Order
import pandas as pd

import json

# Create your tests here.
class StatsAPITestCase(APITestCase):

    def setUp(self):
        Order.objects.create(num=1, side='asks', symbol='BTC-USD', px='54030', qty='0.002')
        Order.objects.create(num=3, side='asks', symbol='BTC-USD', px='50003', qty='0.03')

        Order.objects.create(num=2, side='bids', symbol='BTC-USD', px='53030', qty='0.123')
        Order.objects.create(num=4, side='bids', symbol='BTC-USD', px='48002', qty='1.2')

        Order.objects.create(num=5, side='bids', symbol='ETH-USD', px='4023', qty='1.2')
        Order.objects.create(num=6, side='asks', symbol='LTC-USD', px='325', qty='4.2')
        return super().setUp()

    def test_stats_detail_endpoint(self):
        '''
        Testing Detail Stats Endpoint
        '''
        endpoint = reverse('detail_stats', kwargs={'symbol': 'BTC-USD', 'side': 'asks'})
        response = self.client.get(endpoint)
        content_dict = json.loads(response.content)

        recs = Order.objects.filter(symbol='BTC-USD').values()
        df = pd.DataFrame(recs)
        total_qty_asks = df[df['side'] == 'asks'].qty.sum()

        assert content_dict['asks']['total_qty'] == total_qty_asks # Testing calculation of the enpoint
        assert 'bids' not in content_dict # Testing that the endpoint returns the right type

    def test_stats_endpoint(self):
        '''
        Testing Detail Stats Endpoint
        '''
        endpoint = reverse('global_stats')
        response = self.client.get(endpoint)
        content_dict = json.loads(response.content)

        recs = Order.objects.all().values()
        df = pd.DataFrame(recs)
        total_coins = len(list(df.symbol.unique()))

        # Test that the General stats reports report all the available coinds
        assert total_coins == len(content_dict)
