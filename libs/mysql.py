import time, logging, os, datetime
import pymysql
from dbutils.pooled_db import PooledDB, SharedDBConnection
from django.conf import settings

db_host = settings.DATABASES['default']['HOST']
db_pass = settings.DATABASES['default']['PASSWORD']
db_port = settings.DATABASES['default']['PORT']
db_name = settings.DATABASES['default']['NAME']
db_user = settings.DATABASES['default']['USER']
db_charset = settings.DATABASES['default']['OPTIONS']['charset']


def str_filter(str, max_length=20):
    dirty_stuff = ["\"", "\\", "/", "*", "'", "=", "-", "#", ";", "<", " ", "+", "%", "$", "(", ")", "%", "@", "!"]
    for stuff in dirty_stuff:
        str = str.replace(stuff, "")
    return str[:max_length]


def sqlparam_filter(param, max_length=20):
    dirty_stuff = ["\"", "\\", "/", "*", "'", "=", "-", "#", ";", "<", " ", "+", "%", "$", "(", ")", "%", "@", "!"]
    new_param = []
    if isinstance(param, list):
        for par in param:
            for stuff in dirty_stuff:
                par = par.replace(stuff, "")
                par = par[:max_length]
            new_param.append(par)
    elif isinstance(param, str):
        new_param = str_filter(param)
    return new_param


def exe_time(func):
    def new_func(*args, **args2):
        t0 = time.time()
        t0local = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        back = func(*args, **args2)
        t1 = time.time()
        t1local = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        msg = "Function: %s, start: @%s, end: @%s,  elapsed: @%.4fs." % (func.__name__, t0local, t1local, t1 - t0)
        logging.info(msg)
        return back

    return new_func


class MysqlC(object):
    """the class to connect mysql database and execute sql"""

    def __init__(self):
        self.pool = PooledDB(
            creator=pymysql,  # 使用链接数据库的模块
            maxconnections=6,  # 连接池允许的最大连接数，0和None表示不限制连接数
            mincached=2,  # 初始化时，链接池中至少创建的空闲的链接，0表示不创建
            maxcached=5,  # 链接池中最多闲置的链接，0和None不限制
            maxshared=3,
            # 链接池中最多共享的链接数量，0和None表示全部共享。PS: 无用，因为pymysql和MySQLdb等模块的 threadsafety都为1，所有值无论设置为多少，_maxcached永远为0，所以永远是所有链接都共享。
            blocking=True,  # 连接池中如果没有可用连接后，是否阻塞等待。True，等待；False，不等待然后报错
            maxusage=None,  # 一个链接最多被重复使用的次数，None表示无限制
            setsession=[],  # 开始会话前执行的命令列表。如：["set datestyle to ...", "set time zone ..."]
            ping=0,
            # ping MySQL服务端，检查是否服务可用。# 如：0 = None = never, 1 = default = whenever it is requested, 2 = when a cursor is created, 4 = when a query is executed, 7 = always
            host=db_host,
            port=int(db_port),
            user=db_user,
            password=db_pass,
            database=db_name,
            charset=db_charset
        )

    def get_cursor(self):
        try:
            conn = self.pool.connection()
            cursor = conn.cursor()
        except Exception as e:
            logging.error("Database Connection error: " + str(e))
            return None
        return conn, cursor

    def get_cursor2(self):
        try:
            conn = self.pool.connection()
            cursor = conn.cursor(pymysql.cursors.SSDictCursor)
        except Exception as e:
            logging.error("Database Connection error: " + str(e))
            return None
        return conn, cursor

    @exe_time
    def execute(self, sql, param=None):
        """执行单条SQL。用于：delete、update、insert。

        :param sql: 标准SQL
        :param param: SQL参数
        :return: 影响行数
        """
        logging.info(sql)
        logging.info(param)
        conn, cursor = self.get_cursor()
        param = sqlparam_filter(param)
        try:
            cursor.execute(sql, param)
            conn.commit()
            affected_row = cursor.rowcount
        except Exception as e:
            logging.error("mysql execute error: " + str(e))
            raise Exception("mysql execute error: " + str(e))
        finally:
            cursor.close()
            conn.close()
        return affected_row

    @exe_time
    def executemany(self, sql, param=None):
        """执行多条SQL。

        :param sql: 标准SQL
        :param param: SQL参数
        :return: 影响行数
        """
        logging.info(sql)
        conn, cursor = self.get_cursor()
        try:
            cursor.executemany(sql, param)
            conn.commit()
            affected_row = cursor.rowcount
        except Exception as e:
            logging.error("mysql execute error: " + str(e))
            raise Exception("mysql execute error: " + str(e))
        finally:
            cursor.close()
            conn.close()
        return affected_row

    @exe_time
    def query(self, sql):
        """查询SQL。执行select语句。

        :param sql: 标准SQL
        :return: 返回元组类型的结构
        """
        logging.info(sql)
        conn, cursor = self.get_cursor()
        try:
            cursor.execute(sql, None)
            result = cursor.fetchall()
        except Exception as e:
            logging.error("mysql query error: " + str(e))
            return None
        finally:
            cursor.close()
            conn.close()
        return result

    @exe_time
    def query2(self, sql):
        """查询SQL。执行select语句。

        :param sql: 标准SQL
        :return: 返回SQL执行的记录，列表类型的结构，键值对形式
        """
        logging.info(sql)
        conn, cursor = self.get_cursor2()
        try:
            cursor.execute(sql, None)
            result = cursor.fetchall()
        except Exception as e:
            logging.error("database query error: " + str(e))
            return None
        finally:
            cursor.close()
            conn.close()
        return result

# conn = MysqlC()

# insert_sql = """insert into hdd_temp(hostname,hdd_device,hdd_temp,timestamp) values(%s,%s,%s,%s);"""
# print(insert_sql)
# now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
# conn.execute(insert_sql,param=['big4','wd','31',now])

# select_sql = """select * from hdd_temp;"""
# res = conn.query(select_sql)
# print(res)

# select_sql = """select * from hdd_temp;"""
# res2 = conn.query2(select_sql)
# print(res2)
