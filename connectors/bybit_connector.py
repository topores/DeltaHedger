import math
import os
from decimal import Decimal

import pandas as pd
from pybit import unified_trading

from tqdm import tqdm

from connectors.base import BaseConnector
from logging_utils.generator import generate_logger

tqdm.pandas()


class BybitConnector(BaseConnector):
    def __init__(self,api_key=None,api_secret=None):
        self.logger = generate_logger('BybitConnector')

        if None in [api_key,api_secret]:
            self.logger.critical('Not all auth data for bybit_unified is in  env-vars')
            self.valid=False
            return
        self.session = unified_trading.HTTP(
            testnet=False,
            api_key=api_key,
            api_secret=api_secret,
        )
        self.timeout = 0


    def get_ticker_info(self):
        data = self.session.get_instruments_info(category='linear')
        df = pd.json_normalize(data['result']['list'])
        df = df.set_index('symbol')
        return df

    def update_ticker_info(self):
        self.ticker_info = self.get_ticker_info()
        return self

    def round_price(self, quantity, step_size):
        quantity = Decimal(str(quantity))
        return float(quantity-quantity % Decimal(str(step_size)))

    def market(self, ticker=None, quantity=None):

        if ticker is None:
            raise RuntimeError('ticker is undefined')
        if quantity is None:
            raise RuntimeError('quantity is undefined')
        if ticker not in self.ticker_info.index:
            self.update_ticker_info()
        self.timeout = 0.5

        qprec = float(self.ticker_info.loc[ticker, 'lotSizeFilter.qtyStep'])
        qty = abs(quantity)
        qty = int(qty / float(qprec)) * float(qprec)
        rnd = len(str(qprec).split('.')[1])
        fmt = "{:." + str(rnd) + "f}"
        qty = fmt.format(qty)
        if qty == fmt.format(0.00):
            raise ValueError('cutted quantity is 0')

        self.logger.debug(f'params1{ticker =},{qty =}')
        result = self.session.place_order(
            category='linear',
            symbol=ticker,
            side=('Sell', 'Buy')[quantity >= 0],
            order_type= "Market",
            qty=qty
            # reduce_only=False,
            # close_on_trigger=False,
            # position_idx=0
        )
        return result

    def ioc(self, ticker=None, quantity=None,price=None):

        if ticker is None:
            raise RuntimeError('tickers is undefined')
        if quantity is None:
            raise RuntimeError('quantity is undefined')
        self.timeout = 0.5

        qprec = float(self.ticker_info.loc[ticker, 'lotSizeFilter.qtyStep'])
        qty = abs(quantity)
        qty = int(qty / float(qprec)) * float(qprec)
        rnd = len(str(qprec).split('.')[1])
        fmt = "{:." + str(rnd) + "f}"
        qty = fmt.format(qty)
        if qty == fmt.format(0.00):
            raise ValueError('cutted quantity is 0')
        prc = self.round_price(price, self.ticker_info.loc[ticker, 'priceFilter.tickSize'])
        result = self.session.place_order(
            category='linear',
            symbol=ticker,
            side=('Sell', 'Buy')[quantity >= 0],
            order_type="Limit",
            qty=qty,
            price=prc,
            time_in_force="IOC",
            close_on_trigger=False,
            position_idx=0
        )
        return result

    def get_positions(self):
        data = self.session.get_positions(category='linear',settleCoin='USDT')
        position = dict()
        for el in data['result']['list']:
            side = -1 if el['side'].lower() == 'sell' else 1
            position[el['symbol']] = float(el['size']) * side
        return position

        pass
    def get_option_positions(self):
        data = self.session.get_positions(category='option')
        position = dict()
        for el in data['result']['list']:
            side = -1 if el['side'].lower() == 'sell' else 1
            position[el['symbol']] = float(el['size']) * side
        return position

        pass

    def get_balance(self, quote='USDT'):
        balance = self.session.get_wallet_balance(accountType='CONTRACT',coin=quote)
        result=balance['result']['list'][0]['coin'][0]['equity']
        return float(result)


if __name__ == "__main__":
    # debugging
    API_KEY = os.getenv('BYBIT_API_KEY')
    API_SECRET = os.getenv('BYBIT_API_SECRET')
    bbc = BybitConnector(api_key=API_KEY, api_secret=API_SECRET)
    _=bbc.get_option_positions()
    print(_)

