import argparse

parser = argparse.ArgumentParser()  # 这些参数都有默认值，当调用parser.print_help()或者运行程序时由于参数不正确(此时python解释器其实也是调用了pring_help()方法)时，                                                                     # 会打印这些描述信息，一般只需要传递description参数，如上。
parser.add_argument('--config', default="dev", help="The path of address")
config = parser.parse_args().config


def __init__(self, config):
    if 'dev' == config:
        from config.mysql_file import mysql_info_dev as mysql
        from config.url_file import url_info_dev as url
    elif 'test' == config:
        from config.mysql_file import mysql_info_test as mysql
        from config.url_file import url_info_test as url
    elif 'uat' == config:
        from config.mysql_file import mysql_info_uat as mysql
        from config.url_file import url_info_uat as url
    elif 'prod' == config:
        from config.mysql_file import mysql_info_prod as mysql
        from config.url_file import url_info_prod as url
    else:
        from config.mysql_file import mysql_info_local as mysql
        from config.url_file import url_info_local as url
    self.cur = self.conn.cursor()
