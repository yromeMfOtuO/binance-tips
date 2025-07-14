"""

"""
import markdown

from client.binance_client import get_binance_spot_market_data
from client.config import Config
from client.email_client import EmailClient
from previous_data import get_previous_top_gainer, write_previous_top_gainer, get_previous_top_volume, \
    write_previous_top_volume
from top_gainer import get_top_gainer
from top_volume import get_top_volume, compare_top_volume


def compare(current: list, previous: list):
    """
    获取当前和前一天的涨幅最大的币种，并进行比较
    """

    # if current_top_gainer is None or previous_top_gainer is None:
    #     return None

    current_symbols = list(map(lambda x: x['symbol'], current))
    previous_symbols = list(map(lambda x: x['symbol'], previous))
    not_in_prev = [symbol for symbol in current_symbols if symbol not in previous_symbols]

    # 比较当前和前一天的涨幅最大的币种
    comparison = {
        "current": current,
        "previous": previous,
        "notInPrevious": not_in_prev,
    }

    return comparison


def top_gainer_item(coin_data: dict) -> str:
    return f"| {coin_data['symbol'][:-4]} | {str(coin_data['lastPrice'])} | {str(coin_data['priceChangePercent']) + '%'} |"


def top_volume_item(coin_data: dict) -> str:
    return f"| {coin_data['symbol'][:-4]} | {str(coin_data['lastPrice'])}| {str(coin_data['quoteVolume'])} |"


def build_email(top_gainer_comparison: dict, top_volume_comparison: dict) -> dict:
    md_str = f"""
## Top Gainer

### Difference:
    {'\n- ' if top_gainer_comparison['notInPrevious'] else ''}{", ".join(list(map(lambda x: x[:-4], top_gainer_comparison['notInPrevious'])))}

### Current top gainer:
    {'\n | Symbol | Price(U) | Change |\n|:---|:--------|---:|\n' if top_gainer_comparison['current'] else ''} {"\n".join(list(map(top_gainer_item, top_gainer_comparison['current'])))}

### Previous top gainer: 
    {'\n | Symbol | Price(U) | Change |\n|:---|:--------|---:|\n' if top_gainer_comparison['previous'] else ''} {"\n".join(list(map(top_gainer_item, top_gainer_comparison['previous'])))}


## Top Volume

### Difference:
    {'\n- ' if top_volume_comparison['notInPrevious'] else ''}{", ".join(list(map(lambda x: x[:-4], top_volume_comparison['notInPrevious'])))}

### Current top volume:
    {'\n | Symbol | Price(U) | Volume(U) |\n|:---|:-------|---:|\n' if top_volume_comparison['current'] else ''} {"\n".join(list(map(top_volume_item, top_volume_comparison['current'])))}

### Previous top volume: 
    {'\n | Symbol | Price(U) | Volume(U) |\n|:---|:-------|---:|\n' if top_volume_comparison['previous'] else ''} {"\n".join(list(map(top_volume_item, top_volume_comparison['previous'])))}

"""

    # 添加CSS样式
    css_style = """
        <style>
        table {
            border-collapse: collapse;
            margin: 20px 0;
        }
        th, td {
            border: 1px solid #ddd;
            padding: 8px;
            text-align: left;
        }
        th {
            background-color: #f2f2f2;
        }
        </style>
    """

    html_content = markdown.markdown(
        md_str,
        extensions=[
            'markdown.extensions.tables',
            'markdown.extensions.fenced_code'
        ]
    )

    return {
        "subject": "BINANCE.COM Market Data Tips",
        "content":  css_style + html_content,
    }


def tips():
    # 1. 获取市场数据
    origin_market_data = get_binance_spot_market_data()

    # 2. 获取 top gainer 并比较
    current_top_gainer = get_top_gainer(origin_market_data)
    previous_top_gainer = get_previous_top_gainer()
    top_gainer_comparison = compare(current_top_gainer, previous_top_gainer)
    write_previous_top_gainer(current_top_gainer)

    # 3. 获取 top volume 并比较
    current_top_volume = get_top_volume(origin_market_data)
    previous_top_volume = get_previous_top_volume()
    top_volume_comparison = compare(current_top_volume, previous_top_volume)
    write_previous_top_volume(current_top_volume)

    # -1. 拼接通知邮件的内容
    # TODO: 增加 top volume 部分
    email = build_email(top_gainer_comparison, top_volume_comparison)
    config = Config()
    email_client = EmailClient(config)
    email_client.send(email['subject'], email['content'])


if __name__ == '__main__':
    tips()
    # omd = get_binance_spot_market_data()
    # data = get_market_data_with_24hr_price_change(omd)
    # # top_volume = get_top_volume(omd)
    # # list(map(lambda x: x['symbol'][:-4], top_volume))
    # print(data)
