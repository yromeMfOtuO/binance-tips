"""
get top gainer and compare with previous day
"""

from client.binance_client import get_market_data_with_24hr_price_change

from operator import itemgetter


def get_top_gainer(origin_market_data: list) -> list:
    """
    获取币安现货市场24小时涨幅最大的币种
    """

    market_data = get_market_data_with_24hr_price_change(origin_market_data)
    if market_data is None:
        return None

    # market_data = list_util.sort_by(market_data, "priceChange", reverse=True)
    market_data.sort(key=itemgetter("priceChangePercent"), reverse=True)


    # 找到涨幅最大的币种
    return market_data[:10]  # 返回前10个涨幅最大的币种
