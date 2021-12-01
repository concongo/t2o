from django.core.management.base import BaseCommand
from rest_framework import status
from bc_orders.models import Order

import requests
import json
import pandas as pd


class Command(BaseCommand):
    help = 'Get Current L3 Orders from Blockchain API'

    def add_arguments(self, parser):
        '''
        Definition for Extra commands
        '''
        parser.add_argument('--get-coin',
                            help='Include the Coin Symbol')
        parser.add_argument('--clean-database',
                            action='store_true',
                            help='Clean Local Orders Database',
        )

    def handle(self, *args, **options):
        '''
        Command handler
        '''
        
        if options['clean_database']:
            Order.objects.all().delete()
            print('Database has been cleaned and is now empty!')
            return
        if not options['get_coin']:
            print('You must specify a coin using additionaly the parameter --getcoin [symbol]')
            return
        coin = options['get_coin']

        print('Getting data...')

        user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, \
            like Gecko) Chrome/39.0.2171.95 Safari/537.36'
        headers = {'User-Agent': user_agent}
        page = requests.get(f"https://api.blockchain.com/v3/exchange/l3/{coin}", headers=headers)

        if page.status_code == status.HTTP_200_OK:
            json_content = json.loads(page.content)

            bids_dict = json_content.get('bids', None)
            asks_dict = json_content.get('asks', None)

            if not bids_dict:
                print('Something went wrong - No bids data present')
                return

            if not asks_dict:
                print('Something went wrong - No bids data present')
                return

            bids_df = pd.DataFrame(bids_dict)
            bids_df['side'] = 'bids'
            asks_df = pd.DataFrame(asks_dict)
            asks_df['side'] = 'asks'
            orders_df = pd.concat([asks_df, bids_df], axis=0)
            orders_df['symbol'] = coin
            print('Saving Data...')
            
            for r in orders_df.to_dict(orient='records'):
                Order.objects.update_or_create(num=r['num'], defaults=r)
            
            print('Process complete!')

        else:
            print(f"Something went wrong. API return code {page.status_code}. Try again.")
