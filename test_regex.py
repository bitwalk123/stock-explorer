import os
import pickle
import re

from funcs.parser import parser_remove_link


def parser_timestamp(content):
    pattern = r'※.+?<br>\n\s*［(\d{4})年(\d{1,2})月(\d{1,2})日］\s*<br>'
    result = re.findall(pattern, content, re.DOTALL)
    for element in result:
        print(element)


def parser_1(content):
    dict_news = dict()
    pattern = r'【(.+?)】'
    result = re.split(pattern, content, re.DOTALL)
    for i, element in enumerate(result):
        if (element == '好材料') or (element == '悪材料') or (element == '好悪材料が混在'):
            dict_news[element] = result[i + 1]
    for key in dict_news.keys():
        print('################################')
        print('###', key)
        parser_2(dict_news[key])


def parser_2(content):
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
        list_desc.append(element[3])
    for desc in list_desc:
        print(desc)
        print(parser_remove_link(desc))


def main_old():
    desc = 'デジタルハーツホールディングス &lt;<a href="/stock/?code=3676">3676</a>&gt; 子会社のAGESTと国内ソフトウェアテスト市場に向けたセキュリティサービス提供に関する業務提携。また、沖縄県のセキュリティ専業企業であるセキュアイノベーションと資本業務提携。'
    print(desc)

    pattern = r'&lt;\s*<a href=".+?">\s*(.+?)\s*</a>\s*&gt;'
    desc_new = re.sub(pattern, r'(\1)', desc)
    #desc_new = re.sub(pattern, r'ABC', desc)
    print(desc_new)

def main():
    pkl_content = 'pkl/content.pkl'
    if os.path.isfile(pkl_content):
        with open(pkl_content, 'rb') as f:
            content = pickle.load(f)
            # print(content)
            parser_1(content)
            parser_timestamp(content)



if __name__ == '__main__':
    main()
