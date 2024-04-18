import pandas as pd
import requests


def get_ob():
    url = 'https://api.bybit.com/v5/market/tickers?category=linear'
    response = requests.get(url, timeout=30)
    data_all = response.json()
    data = data_all['result']['list']
    df = pd.DataFrame(data)
    df = df.rename(columns={'symbol': 'ticker'}).set_index('ticker')

    df = df.rename(columns={'bid1Price': 'bidPrice', 'ask1Price': 'askPrice'})
    df = df[['bidPrice', 'askPrice']]
    for col in ['bidPrice', 'askPrice']:
        df[col] = pd.to_numeric(df[col], errors='coerce')
    return df


def get_info():
    url = 'https://api.bybit.com/v5/market/instruments-info?category=linear'
    response = requests.get(url, timeout=30)
    data_all = response.json()
    data = data_all['result']['list']
    df = pd.DataFrame(data)
    df = df.rename(columns={'symbol': 'ticker'}).set_index('ticker')

    for col in ['fundingInterval']:
        df[col] = pd.to_numeric(df[col], errors='coerce')
    return df


if __name__ == '__main__':
    # debugging
    _ = get_info()
    print(_['fundingInterval'].value_counts())
