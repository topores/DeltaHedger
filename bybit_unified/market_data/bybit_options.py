import pandas as pd
import requests


def get_options_info(coin='BTC'):
    url = f'https://api.bybit.com/v5/market/tickers?category=option&baseCoin={coin}'
    response = requests.get(url, timeout=30)
    data_all = response.json()
    data = data_all['result']['list']
    df = pd.DataFrame(data)
    df = df.rename(columns={'symbol': 'ticker'}).set_index('ticker')

    for col in df.columns:
        df[col] = pd.to_numeric(df[col], errors='coerce')

    df['coin'] = coin

    return df


if __name__ == '__main__':
    # debugging
    _ = get_options_info()
    print(_)
