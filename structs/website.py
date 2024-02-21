class WebSite:
    sites = {
        'domestic': '国内株式トップ | 株価検索 | 国内株式トップ | 国内株式 | 楽天証券[PC]',
        'home': 'ホーム | 楽天証券[PC]',
    }

    def checkSite(self, title: str, keyword: str) -> bool:
        if title == self.sites[keyword]:
            return True
        else:
            return False
