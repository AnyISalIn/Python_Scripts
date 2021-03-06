import re
import sys
import requests
from bs4_base import to_bs

SUMMER_BLOG_URL = 'http://yanruohan.blog.51cto.com'
FOOT_PATTERN = re.compile(
    r'类别：.*\|阅读\((?P<number>[0-9]+)\)\|回复\((?P<comment>[0-9]+)\)\|赞\((?P<vote>[0-9]+)\)阅读全文>> ')


class BlogItem(object):

    def __init__(self, bs_obj):
        self._bs_obj = bs_obj
        self._art_content = bs_obj.find('div', {'class': 'artContent'})
        self._art_foot = bs_obj.find('div', {'class': 'artFoot'})
        self.__dict__.update(FOOT_PATTERN.match(
            self._art_foot.text).groupdict())

    @property
    def title(self):
        return self._bs_obj.h3.text.strip('\n')

    @property
    def href(self):
        for item in self._art_foot.find_all('a'):
            if item.text == '阅读':
                return SUMMER_BLOG_URL + item.get('href')

    @property
    def id(self):
        return self.href.split('/')[-1]

    @property
    def content(self):
        return self._art_content.text

    def __repr__(self):
        return '<BlogItem {}>'.format(self.title)


def fetch_blogs():
    res = requests.get(SUMMER_BLOG_URL)
    res.encoding = 'gbk'
    bs_obj = to_bs(res.text)

    return [BlogItem(item) for item in bs_obj.find_all('div', {'class': 'blogList'})]


def printer(limit=5):
    blogs = fetch_blogs()
    for blog in blogs[:limit]:
        for key in blog.__dir__():
            if not key.startswith('_'):
                print('{}: {}'.format(key, getattr(blog, key)))
        print()


def main():
    if len(sys.argv) > 1 and sys.argv[1].isdigit():
        printer(int(sys.argv[1]))
    else:
        printer()


if __name__ == '__main__':
    main()
