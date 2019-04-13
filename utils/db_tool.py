import logging

import pymysql
import redis

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

URL_REMEMBER_SET = "url_remember_set"
WAIT_REQUEST_URLS = "wait_request_urls"


class MysqlConn(object):
    def __init__(self, host, port, user, password, db):
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.db = db

    def run_sql(self, sql):
        conn = pymysql.connect(host=self.host,
                               port=self.port,
                               user=self.user,
                               password=self.password,
                               db=self.db,
                               charset='utf8mb4',
                               cursorclass=pymysql.cursors.DictCursor)
        try:
            with conn.cursor() as cursor:
                cursor.execute(sql)
            conn.commit()
        except Exception as e:
            logger.error(e)
        finally:
            conn.close()

    def run_select(self, sql):
        conn = pymysql.connect(host=self.host,
                               port=self.port,
                               user=self.user,
                               password=self.password,
                               db=self.db,
                               charset='utf8mb4',
                               cursorclass=pymysql.cursors.DictCursor)
        try:
            with conn.cursor() as cursor:
                cursor.execute(sql)
                result = cursor.fetchall()
            return result
        except Exception as e:
            logger.error(e)
        finally:
            conn.close()

    def add_one_phone(self, data):
        zol_id = data.get('zol_id')
        p_name = data.get('p_name')
        price = data.get('price')
        image_url = data.get('image_url')
        p_cpu = data.get('p_cpu')
        front_camera = data.get('front_camera')
        rear_camera = data.get('rear_camera')
        ram = data.get('ram')
        battery = data.get('battery')
        screen = data.get('screen')
        resolution = data.get('resolution')
        web_url = data.get('web_url')
        sql = "INSERT INTO `phone` (`zol_id`, `p_name`, `price`, `image_url`," \
              " `p_cpu`, `front_camera`, `rear_camera`, `ram`, `battery`, " \
              "`screen`, `resolution`, `web_url`) " \
              "VALUES ({}, '{}', {}, '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}');"\
            .format(zol_id, p_name, price, image_url, p_cpu, front_camera,
                    rear_camera, ram, battery, screen, resolution, web_url)
        print(sql)
        self.run_sql(sql)

    def select_phone(self, name, sort, order, limit, offset):
        if name is None or name == '':
            sql = "select * from phone order by `{}` {} limit {} offset {};"\
                .format(sort, order, limit, offset)
            count_sql = "select count(*) from phone;"
        else:
            sql = "select * from phone where (p_name like '%{}%') " \
                  "order by `{}` {} limit {} offset {};"\
                .format(name, sort, order, limit, offset)
            count_sql = "select count(*) from phone where (p_name like '%{}%');".format(name)
        total = self.run_select(count_sql)[0]['count(*)']
        return self.run_select(sql), total

    def init_db(self):
        with open('utils/init.sql', 'r') as f:
            sqls_str = ''
            for line in f.readlines():
                sqls_str += line
        conn = pymysql.connect(host=self.host,
                               port=self.port,
                               user=self.user,
                               password=self.password,
                               charset='utf8mb4',
                               cursorclass=pymysql.cursors.DictCursor)
        try:
            with conn.cursor() as cursor:
                sqls_str = sqls_str.replace('\n', '')
                sqls = sqls_str.split(';')
                for sql in sqls:
                    logger.info(sql)
                    cursor.execute(sql+';')
            conn.commit()
        except Exception as e:
            logger.error(e)
        finally:
            conn.close()


class RedisConn(object):

    def __init__(self, host, port, auth, db):
        self.redis_pool = redis.ConnectionPool(host=host,
                                               port=port,
                                               db=db,
                                               password=auth)
        self.conn = redis.Redis(connection_pool=self.redis_pool)

    def get_redis_conn_pool(self):
        return redis.Redis(connection_pool=self.redis_pool)

    def update_url_set(self, url):
        conn = self.get_redis_conn_pool()
        conn.sadd(URL_REMEMBER_SET, url)

    def set_exists(self, url):
        conn = self.get_redis_conn_pool()
        return conn.sismember(URL_REMEMBER_SET, url)

    def wait_request_push(self, url):
        conn = self.get_redis_conn_pool()
        conn.sadd(WAIT_REQUEST_URLS, url)

    def wait_request_pop(self):
        conn = self.get_redis_conn_pool()
        return conn.spop(WAIT_REQUEST_URLS)
