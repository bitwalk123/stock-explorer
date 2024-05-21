from html.parser import HTMLParser
import re


class ParserKabuYoho(HTMLParser):
    url = 'https://kabuyoho.ifis.co.jp/index.php'
    pattern = re.compile(r'index\.php\?(action=tp1\&sa=consNewsDetail\&nid=.+)')

    def __init__(self):
        HTMLParser.__init__(self)

        self.flag_news = False
        self.flag_date = False
        self.flag_link = False

        self.news = list()
        self.element = None
        self.link = ''

    def handle_starttag(self, tag, attrs):
        dict_attrs = dict(attrs)

        if tag == 'table':
            if 'class' in dict_attrs:
                if dict_attrs['class'] == 'tb_new_news':
                    self.flag_news = True
                    return
                return
            return

        if tag == 'span' and self.flag_news is True:
            self.flag_date = True
            return

        if tag == 'a' and self.flag_news is True:
            if 'href' in dict_attrs:
                m = self.pattern.match(dict_attrs['href'])
                if m:
                    self.link = '%s?%s' % (self.url, m.group(1))
                    self.flag_link = True
                    return
                return
            return

        if tag == 'tr' and self.flag_news is True:
            self.element = list()
            return

    def handle_data(self, data):
        content = data.strip()
        if self.flag_news and self.flag_date:
            self.element.append(content)
            self.flag_date = False
            return

        if self.flag_news and self.flag_link:
            self.element.append(content)
            self.element.append(self.link)
            self.flag_link = False
            self.link = ''
            return

    def handle_endtag(self, tag):
        if tag == 'table' and self.flag_news is True:
            self.flag_news = False
            return

        if tag == 'tr' and self.flag_news is True:
            if len(self.element) > 0:
                self.news.append(self.element)
            return
