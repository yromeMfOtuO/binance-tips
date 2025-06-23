"""
binance open api client
"""

import requests


def calculate_price_change(open_price, current_price):
    """
    计算涨幅
    """
    price_change = current_price - open_price
    if price_change == 0:
        return 0.0
    return price_change / open_price


def get_binance_spot_market_data():
    """
    获取币安现货市场的价格数据
    """
    url = "https://data-api.binance.vision/api/v3/ticker/24hr"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        print("Error fetching ticker data:", response.status_code, response.text)
        return None


def get_market_data_with_24hr_price_change():
    """
    获取币安现货市场的价格数据，并计算24小时内的价格变化
    """
    market_data = get_binance_spot_market_data()
    if market_data is None:
        return None

    # 过滤出USDT交易对
    market_data = list(filter(lambda x: x['symbol'][-4:] == 'USDT', market_data))

    for coin_data in market_data:
        open_price = float(coin_data["openPrice"])
        current_price = float(coin_data["lastPrice"])

        # 计算涨幅
        price_change = calculate_price_change(open_price, current_price)
        coin_data['priceChange'] = price_change

    # market_data = list_util.sort_by(market_data, "priceChange", reverse=True)

    return market_data
