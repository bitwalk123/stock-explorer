import requests

from parser.htmlparser import ParserKabuYoho, Parser8035


def get_news_kabuyoho(ticker: str) -> list:
    # 株予想
    parser = ParserKabuYoho()
    url = parser.url
    params = {
        'action': 'tp1',
        'sa': 'report_top',
        'bcode': ticker,
    }
    response = requests.get(url, params=params)
    parser.feed(response.text)
    parser.close()
    results = parser.news

    return results


def get_news_8035() -> list:
    # 株予想
    parser = Parser8035()
    url = parser.url
    response = requests.get(url)
    parser.feed(response.text)
    parser.close()
    results = parser.news

    return results
