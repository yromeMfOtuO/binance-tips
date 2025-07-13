"""
get top volume and compare with previous day
"""

from client.binance_client import get_binance_spot_market_data_with_24hr_volume

from operator import itemgetter

def get_top_volume(origin_market_data: list) -> list:
    """
    获取币安现货市场24小时成交量最大的币种
    """
    if origin_market_data is None:
        return []

    market_data = get_binance_spot_market_data_with_24hr_volume(origin_market_data)
    market_data.sort(key=itemgetter("quoteVolume"), reverse=True)

    # 找到成交量最大的币种
    return market_data[:10]  # 返回前10个成交量最大的币种


def compare_top_volume(current_top_volume, current_top_gainer):
    # TODO
    ...
