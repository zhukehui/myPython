# 这些参数都有默认值，当调用parser.print_help()或者运行程序时由于参数不正确(此时python解释器其实也是调用了pring_help()方法)时 会打印这些描述信息，一般只需要传递description参数，如上。
# 读取配置
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--config', default="dev", help="The path of address")
config_args = parser.parse_args().config