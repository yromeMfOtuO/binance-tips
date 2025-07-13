"""
get and write previous data

TODO: 四小时执行一次，会记录一次数据

TODO: top volume的数据记录
"""

import json

def get_previous_top_gainer():
    """
    获取前一次的涨幅最大的币种
    """
    try:
        with open('./previous_top_gainer.json', 'r', encoding='utf-8') as f:
            top_gainer = json.load(f)
            return top_gainer
    except FileNotFoundError:
        return []


def write_previous_top_gainer(data: list):
    """
    将前一次的涨幅最大的币种数据写入文件
    """
    try:
        with open('./previous_top_gainer.json', 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4)
    except Exception as e:
        print(f"Error writing previous top gainer data: {e}")


def get_previous_top_volume():
    """
    获取前一次的交易量最大的币种
    """
    try:
        with open('./previous_top_volume.json', 'r', encoding='utf-8') as f:
            top_volume = json.load(f)
            return top_volume
    except FileNotFoundError:
        return []


def write_previous_top_volume(data: list):
    """
    将前一次的交易量最大的币种数据写入文件
    """
    try:
        with open('./previous_top_volume.json', 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4)
    except Exception as e:
        print(f"Error writing previous top volume data: {e}")
