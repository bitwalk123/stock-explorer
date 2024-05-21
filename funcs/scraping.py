import requests

from parser.kabuyoho import ParserKabuYoho


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
