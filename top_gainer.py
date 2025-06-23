"""
get top gainer and compare with previous day
"""
import json

from little_finger.utils import list_util

from client.binance_client import get_market_data_with_24hr_price_change
from client.config import Config
from client.email_client import EmailClient


def get_top_gainer():
    """
    获取币安现货市场24小时涨幅最大的币种
    """
    market_data = get_market_data_with_24hr_price_change()
    if market_data is None:
        return None

    market_data = list_util.sort_by(market_data, "priceChange", reverse=True)

    # 找到涨幅最大的币种
    return market_data[:10]  # 返回前10个涨幅最大的币种


def get_previous_top_gainer():
    """
    获取前一天的涨幅最大的币种
    """
    try:
        with open('./previous_day_top_gainer.json', 'r', encoding='utf-8') as f:
            top_gainer = json.load(f)
            return top_gainer
    except FileNotFoundError:
        return []


def write_previous_top_gainer(data: list):
    """
    将前一天的涨幅最大的币种数据写入文件
    """
    try:
        with open('./previous_day_top_gainer.json', 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4)
    except Exception as e:
        print(f"Error writing previous top gainer data: {e}")


def compare_top_gainer(current_top_gainer: list, previous_top_gainer: list):
    """
    获取当前和前一天的涨幅最大的币种，并进行比较
    """

    # if current_top_gainer is None or previous_top_gainer is None:
    #     return None

    current_symbols = list(map(lambda x: x['symbol'], current_top_gainer))
    previous_symbols = list(map(lambda x: x['symbol'], previous_top_gainer))
    not_in_prev = [symbol for symbol in current_symbols if symbol not in previous_symbols]

    # 比较当前和前一天的涨幅最大的币种
    comparison = {
        "current": current_top_gainer,
        "previous": previous_top_gainer,
        "notInPrevious": not_in_prev,
    }

    return comparison


def build_email(comparison: dict) -> dict:
    return {
        "subject": "币安现货市场24小时涨幅最大的币种对比",
        "content": f"""
yesterday's top gainer: 
    {",".join(list(map(lambda x: x['symbol'][:-4], comparison['previous'])))}
today's top gainer:
    {",".join(list(map(lambda x: x['symbol'][:-4], comparison['current'])))}
difference:
    {",".join(list(map(lambda x: x['symbol'][:-4], comparison['notInPrevious'])))}
""",
    }


def tips():
    current_top_gainer = get_top_gainer()
    previous_top_gainer = get_previous_top_gainer()
    comparison = compare_top_gainer(current_top_gainer, previous_top_gainer)

    write_previous_top_gainer(current_top_gainer)

    email = build_email(comparison)

    email_client = EmailClient(Config())
    email_client.send(email['subject'], email['content'])

if __name__ == '__main__':
    tips()
