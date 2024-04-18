import os
import time

import numpy as np
import pandas as pd

from bybit_unified.config import THRESHOLDS, SLEEP_TIME
from bybit_unified.market_data.bybit_options import get_options_info
from connectors.bybit_connector import BybitConnector
from logging_utils.generator import generate_logger

API_KEY = os.getenv('BYBIT_API_KEY')
API_SECRET = os.getenv('BYBIT_API_SECRET')
connector = BybitConnector(api_key=API_KEY, api_secret=API_SECRET)

logger = generate_logger('DeltaHedger.bybit.app')

coins = ['BTC', 'ETH']

context = {
    'last_deltas': None
}


def make_options_info():
    options_info = pd.concat([get_options_info(coin) for coin in ['BTC', 'ETH']])
    option_pos = connector.get_option_positions()
    info = options_info.loc[option_pos.keys()]
    info['pos'] = np.nan
    for k, v in option_pos.items():
        info['pos'].at[k] = v

    return info


def get_deltas(info):
    info['pos_delta'] = info['pos'] * info['delta']
    deltas = {}
    for coin in coins:
        deltas[coin] = info[info['coin'] == coin]['pos_delta'].sum()
    return deltas


def calc_orders(deltas, pos):
    orders = {}
    for coin in deltas:
        orders[coin + 'USDT'] = -deltas.get(coin, 0) - pos.get(coin + 'USDT', 0)
    return orders


def execute_orders(orders):
    executed = []
    for ticker, value in orders.items():
        if abs(value) < THRESHOLDS[ticker]:
            continue
        result = connector.market(ticker, quantity=value)
        executed.append({'ticker': ticker, 'quantity': value, 'result': result is not None})
    return executed


def log_executed(deltas, pos, executed):
    if len(executed) > 0:
        logger.warning(f'Executed: {executed}\ndeltas:{deltas}\npos:{pos}')
    else:
        logger.debug(f'Executed: {executed}\ndeltas:{deltas}\npos:{pos}')


def pipeline():
    connector.update_ticker_info()
    info = make_options_info()
    deltas = get_deltas(info)

    pos = connector.get_positions()
    orders = calc_orders(deltas, pos)

    executed = execute_orders(orders)
    log_executed(deltas, pos, executed)


if __name__ == '__main__':
    while True:
        time.sleep(SLEEP_TIME)
        try:
            pipeline()
        except Exception as e:
            logger.critical(f'Exception during pipeline{e}')
