import re


class WebSite:
    """
    sites = {
        'domestic': '国内株式トップ | 株価検索 | 国内株式トップ | 国内株式 | 楽天証券[PC]',
        'home': 'ホーム | 楽天証券[PC]',
    }
    """
    sites = {
        'buynew': '信用取引（新規注文 / 受付）-新規注文',
        'domestic': '国内株式トップ',
        'home': 'ホーム',
        'ticker': '%s-株価',
        'order': '国内株式取引（注文照会・訂正・取消）-注文照会・訂正・取消',
    }
    pattern = re.compile(r'^(.*?)\s+\|.*')

    def checkSite(self, title: str, keyword: str, ticker: str = '') -> bool:
        m = self.pattern.match(title)
        if not m:
            return False

        top_title = m.group(1)

        if keyword == 'ticker':
            name_web = self.sites[keyword] % ticker
        else:
            name_web = self.sites[keyword]

        if top_title == name_web:
            return True
        else:
            return False
