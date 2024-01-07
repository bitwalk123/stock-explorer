import re

import pandas as pd


def parser_good_bad_1(content) -> dict:
    dict_news = dict()
    dict_df = dict()
    pattern = r'【(.+?)】'
    result = re.split(pattern, content, re.DOTALL)
    for i, element in enumerate(result):
        if (element == '好材料') or (element == '悪材料') or (element == '好悪材料が混在'):
            dict_news[element] = result[i + 1]
    for key in dict_news.keys():
        dict_df[key] = parser_good_bad_2(dict_news[key])
    return dict_df


def parser_good_bad_2(content) -> pd.DataFrame:
    pattern = r'■(.+?)\s*&lt;<a href=".+?">(.+?)</a>&gt;\s*\[(.+?)\]\s*<br>\s*\n(.+?)<br>'
    list_name = list()
    list_code = list()
    list_market = list()
    list_desc = list()
    result = re.findall(pattern, content, re.DOTALL)
    for element in result:
        list_name.append(element[0])
        list_code.append(element[1])
        list_market.append(element[2])
        desc = parser_remove_link(element[3])
        list_desc.append(desc)
    df = pd.DataFrame({
        '銘柄': list_name,
        'コード': list_code,
        '市場': list_market,
        '説明': list_desc,
    })
    return df


def parser_timestamp(content) -> list:
    list_timestamp = list()
    pattern = r'※.+?<br>\n\s*［(\d{4})年(\d{1,2})月(\d{1,2})日］\s*<br>'
    result = re.findall(pattern, content, re.DOTALL)
    if len(result) > 0:
        for element in result[0]:
            list_timestamp.append(element)
    return list_timestamp


def parser_remove_link(content) -> str:
    pattern = r'&lt;\s*<a href=".+?"\s*>\s*(.+?)\s*</a>\s*&gt;'
    content_new = re.sub(pattern, r'(\1)', content)
    # print(content_new)
    return content_new
