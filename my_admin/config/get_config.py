class Config:
    def __get_config(self, config):
        if 'dev' == config or 'd' == config:
            from config.mysql_file import mysql_info_dev as mysql
            from config.url_file import url_info_dev as url
        elif 'test' == config or 't' == config:
            from config.mysql_file import mysql_info_test as mysql
            from config.url_file import url_info_test as url
        elif 'uat' == config or 'u' == config:
            from config.mysql_file import mysql_info_uat as mysql
            from config.url_file import url_info_uat as url
        elif 'prod' == config or 'p' == config:
            from config.mysql_file import mysql_info_prod as mysql
            from config.url_file import url_info_prod as url
        else:
            from config.mysql_file import mysql_info_local as mysql
            from config.url_file import url_info_local as url
        return mysql, url

    def return_config(self, config):
        mysql, url = self.__get_config(config)
        return mysql, url
