import logging
import os
import time

import colorlog
from colorama import init, Fore, Back, Style

class ColorHandler(logging.StreamHandler):
    GRAY8 = "38;5;8"
    GRAY7 = "38;5;2"
    ORANGE = "33"
    RED = "31"
    WHITE = "0"
    PURPLE = "35"
    BLUE = "34"

    def emit(self, record):
        try:
            msg = self.format(record)
            level_color_map = {
                logging.DEBUG: self.BLUE,
                logging.INFO: self.GRAY7,
                logging.WARNING: self.ORANGE,
                logging.ERROR: self.RED,
                logging.CRITICAL: self.PURPLE

            }

            csi = f"{chr(27)}["  # control sequence introducer
            color = level_color_map.get(record.levelno, self.WHITE)

            self.stream.write(f"{csi}{color}m{msg}{csi}m\n")
            self.flush()
        except RecursionError:
            raise
        except Exception:
            self.handleError(record)

class LogUtil:

    def __init__(self, log_level=logging.DEBUG):
        # 获取logger对象
        self.log_name = '{}.log'.format(time.strftime("%Y-%m-%d", time.localtime()))
        self.log_path_name = os.path.join(get_log_path(), self.log_name)
        self.logger = logging.getLogger(self.log_name)

        # 避免重复打印日志
        self.logger.handlers = []

        # 指定最低日志级别：（critical > error > warning > info > debug）
        self.logger.setLevel(log_level)

        # 日志格化字符串
        # console_fmt = '%(log_color)s%(asctime)s-%(threadName)s-%(filename)s-[line:%(lineno)d]-%(levelname)s: %(message)s'
        file_fmt = '时间：%(asctime)s - 日志等级: %(threadName)s-%(filename)s-日志信息：[line:%(lineno)d]-%(levelname)s: %(message)s'
        # 控制台输出不同级别日志颜色设置
        color_config = {
            'DEBUG': 'cyan',
            'INFO': 'green',
            'WARNING': 'yellow',
            'ERROR': 'red',
            'CRITICAL': 'red,bg_white'
        }

        console_formatter = colorlog.ColoredFormatter(fmt=file_fmt, log_colors=color_config)
        file_formatter = logging.Formatter(fmt=file_fmt)

        # 输出到控制台
        console_handler = ColorHandler()
        # console_handler = logging.StreamHandler()
        # 输出到文件
        file_handler = logging.FileHandler(filename=self.log_path_name, mode='a', encoding='utf-8')

        # 设置日志格式
        console_handler.setFormatter(console_formatter)
        file_handler.setFormatter(file_formatter)

        # 处理器设置日志级别，不同处理器可各自设置级别，默认使用logger日志级别
        # console_handler.setLevel(logging.DEBUG)
        file_handler.setLevel(logging.INFO)  # 只有INFO\warning、error和critical级别才会写入日志文件

        # logger添加处理器
        self.logger.addHandler(console_handler)
        self.logger.addHandler(file_handler)

    def getLogger(self):
        return self.logger

    def debug(self, message):
        self.logger.debug(message)

    def info(self, message):
        self.logger.info(message)

    def warning(self, message):
        self.logger.warning(message)

    def error(self, message):
        self.logger.error(message)

    def critical(self, message):
        self.logger.critical(message)


def get_log_path():
    return os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__)))), "log")


if __name__ == '__main__':
    log = LogUtil(log_level=logging.DEBUG)
    log.debug('debug---------')
    log.info('info-------------')
    log.warning('warning-----------')
    log.error('error----------')
    log.critical('critical-----------')
