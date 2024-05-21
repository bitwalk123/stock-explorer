from html.parser import HTMLParser


class MyHTMLParser(HTMLParser):

    def handle_starttag(self, tag, attrs):
        dict_attrs = dict(attrs)
        print("タグのはじめ　 :", tag)
        if len(dict_attrs) > 0:
            print(" └ タグの属性 =", dict_attrs)

    def handle_endtag(self, tag):
        print("タグのおわり　 :", tag)

    def handle_data(self, data):
        print("タグ内の文字列 :", data.strip())


if __name__ == '__main__':
    parser = MyHTMLParser()
    parser.feed(
        '<html><head><title>テスト（タイトル）</title></head>'
        '<body><h1 id="title">ページタイトル</h1>'
        '<p style="font-family: monospace;">これはテスト用です。</p>'
        '</body></html>'
    )
