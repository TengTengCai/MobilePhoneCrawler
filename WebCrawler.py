import re
import time
from threading import Thread

import requests

import config
from WebParser import WebParser, CrawlerStatus
from utils.db_tool import MysqlConn, RedisConn


def is_any_spider_alive(crawler_threads):
    """
    判断爬虫线程是否忙绿
    :param crawler_threads:
    :return:
    """
    return any([crawler_thread.parser.status == CrawlerStatus.WORKING
                for crawler_thread in crawler_threads])


def main():
    m_conn = MysqlConn(config.DB_HOST,
                       config.DB_PORT,
                       config.DB_USER,
                       config.DB_PASSWORD,
                       config.DB_NAME)
    m_conn.init_db()
    r_conn = RedisConn(config.REDIS_HOST,
                       config.REDIS_PORT,
                       config.REDIS_AUTH,
                       config.REDIS_DB)
    start_url = 'http://detail.zol.com.cn/cell_phone_index/subcate57_list_1.html'

    r_conn.wait_request_push(start_url)

    crawler_threads = [WebCrawlerThread('Thread-%d' % i, r_conn, m_conn)
                       for i in range(10)]
    # 开启10个爬虫
    for crawler_thread in crawler_threads:
        crawler_thread.start()

    while is_any_spider_alive(crawler_threads):
        time.sleep(60)


class WebCrawlerThread(Thread):
    def __init__(self, name, redis_conn, m_conn):
        """

        :param url_manager:
        :type url_manager UrlManager:
        """
        super().__init__(name=name)
        self.name = name
        self.redis_conn = redis_conn
        self.m_conn = m_conn
        self.parser = WebParser(self.redis_conn)

    @staticmethod
    def is_page_url(url):
        m = re.search(r"http://detail\.zol\.com\.cn/cell_phone/index\d+\.shtml",
                      url)
        if m is not None:
            return True
        return False

    def run(self):
        while True:
            current_url = self.redis_conn.wait_request_pop()
            if current_url is None:
                time.sleep(1)
                continue
            current_url = current_url.decode('utf8')

            self.redis_conn.update_url_set(current_url)
            try:
                r = requests.get(current_url)
            except Exception as e:
                print(e)
                continue
            print('{} is download {} status:{}'
                  .format(self.name, current_url, r.status_code))
            if r.status_code != 200:
                continue
            self.parser.set_status_working()
            html_page = r.text
            if WebCrawlerThread.is_page_url(current_url):
                data = self.parser.parser_phone_page(html_page, current_url)
                self.m_conn.add_one_phone(data)
            self.parser.parser_normal_page(html_page, current_url)
            self.parser.set_status_idle()


if __name__ == '__main__':
    main()
