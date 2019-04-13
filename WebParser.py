import re
from enum import unique, Enum
from urllib.parse import urlparse, urljoin

from bs4 import BeautifulSoup


@unique
class CrawlerStatus(Enum):
    """枚举对象"""
    IDLE = 0  # 闲置
    WORKING = 1  # 繁忙


class WebParser(object):
    def __init__(self, redis_conn):
        self.redis_conn = redis_conn
        self._status = CrawlerStatus.IDLE

    def set_status_idle(self):
        """
        改变状态为闲置
        :return: None
        """
        self._status = CrawlerStatus.IDLE

    def set_status_working(self):
        """
        改变状态为繁忙
        :return: None
        """
        self._status = CrawlerStatus.WORKING

    @property
    def status(self):
        """
        获取当前爬虫状态
        :return: int
        """
        return self._status

    def parser_normal_page(self, html, url):
        soup = BeautifulSoup(html, 'xml')
        for a_tag in soup.find_all('a'):
            href = a_tag.get('href')
            result = urlparse(href)
            if result.scheme == '':
                href = urljoin(url, href)
            if href == 'javascript:;' or href is None:
                continue
            if not self.redis_conn.set_exists(href):
                self.redis_conn.wait_request_push(href)

    @staticmethod
    def parser_phone_page(html, url):
        data = {}
        m = re.search(r'http://detail\.zol\.com\.cn/cell_phone/index(\d+)\.shtml', url)
        if m is not None:
            data['zol_id'] = m.group(1)
        soup = BeautifulSoup(html, 'lxml')
        data['p_name'] = soup.find('h1', 'product-model__name').text
        price = soup.find('span', {'class': 'price-type'})
        if price is None:
            price = soup.find('b', {'class': 'price-type'}).text
        else:
            price = price.text[1:]
        if str(price).isnumeric():
            data['price'] = price
        else:
            data['price'] = -1
        image_div = soup.find('div', {'class': 'small-pic'})
        data['image_url'] = image_div.img['src']
        ul = soup.find('ul', {'class': 'product-param-item pi-57 clearfix'})
        ps = ul.find_all('p')
        data['screen'] = str(ps[0].get_text()).split('：')[1]
        data['resolution'] = str(ps[1].get_text()).split('：')[1]
        data['rear_camera'] = str(ps[2].get_text()).split('：')[1]
        data['front_camera'] = str(ps[3].get_text()).split('：')[1]
        data['battery'] = str(ps[4].get_text()).split('：')[1]
        data['p_cpu'] = str(ps[6].get_text()).split('：')[1]
        ram = ps[7].get_text().split('：')[1].replace('GB', '').replace(' ', '')
        if str(ram).isnumeric():
            data['ram'] = ram
        else:
            data['ram'] = 0
        data['web_url'] = url
        print(data)
        return data
