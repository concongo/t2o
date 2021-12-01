from rest_framework.views import APIView
from django.http import JsonResponse

from .models import Order
import pandas as pd

# Create your views here.
class DetailedStatsOrdersAPIView(APIView):

    def get(self, request, *args, **kwargs):

        symbol = kwargs.get('symbol', 'BTC-USD')
        side = kwargs.get('side', 'asks')

        # Validation for EndPoint request
        if side not in ['asks', 'bids']:
            return JsonResponse({'message': 'Not a valid enpoint!'})

        # Validation for Symbol request
        orders = Order.objects.filter(symbol=symbol, side=side).values()
        if not orders.count():
            return JsonResponse({'message': 'Not a valid Symbol!'})

        # All valid
        orders_df = pd.DataFrame(orders)

        orders_df['value'] = orders_df.px * orders_df.qty
        average_value = orders_df.value.mean()
        total_qty = orders_df.qty.sum()
        total_px = orders_df.px.sum()

        max_value_order = orders_df[orders_df.value == orders_df.value.max()]
        min_value_order = orders_df[orders_df.value == orders_df.value.min()]
        
        # Converting to Dict for serilizing
        min_value_order = min_value_order[['px', 'qty', 'num', 'value']].to_dict(orient='records')[0]
        max_value_order = max_value_order[['px', 'qty', 'num', 'value']].to_dict(orient='records')[0]

        json_dict = {
            'bids' if side == 'bids' else 'asks': {
                "average_value": average_value,
                "greater_value": max_value_order,
                "lesser_value": min_value_order,
                "total_qty": total_qty,
                "total_px": total_px
            }
        }

        return JsonResponse(json_dict)

class StatsOrdersAPIView(APIView):

    def get(self, request, *args, **kwargs):

        # Validation for Symbol request
        orders = Order.objects.all().values()
        if not orders.count():
            return JsonResponse({'message': 'Not a valid Symbol!'})

        # All valid
        orders_df = pd.DataFrame(orders)
        orders_df['value'] = orders_df.px * orders_df.qty

        symbols = list(orders_df.symbol.unique()) # Get unique symbols from DB
        sides = ['bids', 'asks']
        json_dict = {}

        for symbol in symbols:
            json_dict[symbol] = {}
            for side in sides:
                json_dict[symbol][side] = {}
                json_dict[symbol][side]['count'] = int(orders_df[(orders_df.side == side) & (orders_df.symbol == symbol)].num.count())
                json_dict[symbol][side]['qty'] = orders_df[(orders_df.side == side) & (orders_df.symbol == symbol)].qty.sum()
                json_dict[symbol][side]['value'] = orders_df[(orders_df.side == side) & (orders_df.symbol == symbol)].value.sum()

        return JsonResponse(json_dict)
