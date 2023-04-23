import logging

import pymysql

from utils.LoggerUtil import LogUtil

log = LogUtil(log_level=logging.DEBUG).getLogger()


# 创建一个类
class Mysql:
    # 将数据库连接和创建游标写成实例属性，可以全局使用
    # 将数据库的基本信息作为参数，因为实际应用中我们需要在不同的环境跑
    def __init__(self, mysql_info):
        self.conn = pymysql.connect(host=mysql_info["host"],
                                    port=mysql_info["port"],
                                    user=mysql_info["user"],
                                    password=mysql_info["password"],
                                    db=mysql_info["db"],
                                    charset=mysql_info["charset"],
                                    autocommit=mysql_info["autocommit"],
                                    cursorclass=pymysql.cursors.DictCursor  # 数据源
                                    )
        self.cur = self.conn.cursor()

    # 创建执行sql的方法，将sql语句作为参数
    def get_data_all(self, sqlStr):
        log.info("sql=%s" % sqlStr)
        self.cur.execute(sqlStr)
        return self.cur.fetchall()  # 返回全部数据
        # print(cur.fetchone())  # 返回第一条
        # print(cur.fetchmany(2))  # 返回自定义条数，不传默认返回第一条

    def get_data_one(self, sqlStr):
        log.info("sql=%s" % sqlStr)
        self.cur.execute(sqlStr)
        return self.cur.fetchone()  # 返回第一条
        # print(cur.fetchall())  #
        # print(cur.fetchmany(2))  # 返回自定义条数，不传默认返回第一条

    def update_data(self, sqlStr):
        log.info("sql=%s" % sqlStr)
        try:
            # 执行SQL语句
            self.cur.execute(sqlStr)
            # 提交到数据库执行
            self.conn.commit()
        except Exception as e:
            print(e)
            # 发生错误时回滚
            self.conn.rollback()

    def insert_data(self, sqlStr, values):
        log.info("sql=%s values=%s" % (sqlStr, values))
        try:
            # 执行SQL语句
            self.cur.execute(sqlStr, values)
            # 提交到数据库执行
            self.conn.commit()
        except Exception as e:
            print(e)
            # 发生错误时回滚
            self.conn.rollback()

    # 创建连接关闭方法
    def close_mysql(self):
        self.cur.close()
        self.conn.close()

# if __name__ == '__main__':
#     sqlStr = "select * from `tbs_activity_form` where id = 1"
#
#     db = Mysql(mysql_info_dev)
#
#     data = db.get_data(sqlStr)
#     db.close_mysql()
#     print(data)
