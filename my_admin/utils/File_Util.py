# -*- coding:utf-8 -*-
import operator
import os
import zipfile

import rarfile


# 找交集，差集
def find_diff_str(list1, list2):
    A = set(list1).intersection(set(list2))  # 交集
    B = set(list1).union(set(list2))  # 并集
    C = set(list1).difference(set(list2))  # 差集，在list1中但不在list2中的元素
    D = set(list2).difference(set(list1))  # 差集，在list2中但不在list1中的元素
    return A, B, C, D


# 对个获取指定目录的所有文件
def get_all_files(dir):
    fileList = []
    """遍历获取指定文件夹下面所有文件"""
    if os.path.isdir(dir):
        filelist = os.listdir(dir)
        for ret in filelist:
            filename = dir + "\\" + ret
            if os.path.isfile(filename):
                fileList.append(filename)
    return fileList


# 对个获取指定目录的所有文件
def get_file_list_by_walk(dir):
    fileList = []
    """使用listdir循环遍历"""
    if not os.path.isdir(dir):
        return fileList
    dirlist = os.walk(dir)
    for root, dirs, files in dirlist:
        for fi in files:
            fileList.append(os.path.join(root, fi))
    return fileList


# 指定文件路径获取文件最后文件的路径包含文件
# 如：D:\test\file.txt 返回的结果为：D:\test\
def get_file_root(path):
    # 获取文件名
    # return os.path.split(path)[1]
    # 获取文件路径
    return os.path.split(path)[0]


# 指定文件路径获取文件最后文件的路径包含文件
# 如：D:\test\file.txt 返回的结果为：file.txt
def get_file_name(path):
    return os.path.basename(path)


# 编码转换
def decode(str):
    try:
        string = str.encode('cp437').decode('gbk')
    except:
        string = str.encode('utf-8').decode('utf-8')
    return string


# 创建目录
def mkdir(path):
    # 去除尾部 \ 符号
    pathx = path.strip().rstrip("\\")
    # 判断路径是否存在
    # 存在     True
    # 不存在   False
    isExists = os.path.exists(pathx)
    # 判断结果
    if not isExists:
        # 如果不存在则创建目录创建目录操作函数
        os.makedirs(path)
        print(path + ' 创建成功')
        return True
    else:
        # 如果目录存在则不创建，并提示目录已存在
        print(path + ' 目录已存在')
        return False


"""
参考文章 https://www.jb51.net/article/180325.htm
https://blog.csdn.net/WANGYONGZIXUE/article/details/111576380
在一个数组里面找重复值
python处理去重用set函数
"""


def find_repeat_val_by_list(list):
    values = {}
    for i in list:
        if list.count(i) > 1:
            values[i] = list.count(i)
    return values


"""
通过指定文件路径文件进行读取内容
如：D:\test\file.txt
"""


def reader_file(path):
    # 解决乱码问题
    fi = open(path, 'r', encoding='utf-8', errors='ignore')
    strs = []
    # splitlines解决不换行\n输出
    for line in fi.read().splitlines():
        if (len(line) > 0):
            strs.append(line)
    return str


"""
创建一个txt文件,并向文件写入msg
@file_dir参数 代表文件目录 如：D:\test
@file_name参数 代表文件名称 如：file.txt
@msg参数 代表要写入文件的内容信息
"""


def writer_to_file(file_dir, file_name, msg):
    # 先创建目录
    mkdir(file_dir)
    # 再打开文件
    full_path = file_dir + "\\" + file_name
    fi = open(full_path, 'w')
    # 写入文件
    fi.write(msg)
    fi.close()


# 删除文件
def del_files(dir_path):
    # os.walk会得到dir_path下各个后代文件夹和其中的文件的三元组列表，顺序自内而外排列，
    for root, dirs, files in os.walk(dir_path, topdown=False):
        # 第一步：删除文件
        for file_name in files:
            try:
                os.remove(os.path.join(root, file_name))  # 删除文件
            except Exception as e:
                print(f'删除文件,失败原因为:{e}')
                pass

        # 第二步：删除空文件夹
        for dir in dirs:
            try:
                os.rmdir(os.path.join(root, dir))  # 删除一个空目录
            except Exception as e:
                print(f'删除空文件夹,失败原因为:{e}')
                pass


# 创建目录
def mkdir(path):
    # 去除尾部 \ 符号
    pathx = path.strip().rstrip("\\")
    # print(f'pathx={pathx}')

    # 判断路径是否存在
    # 存在     True
    # 不存在   False
    isExists = os.path.exists(pathx)
    # 判断结果
    if not isExists:
        # 如果不存在则创建目录创建目录操作函数
        os.makedirs(path)
        print(path + ' 创建成功')
        return True
    else:
        # 如果目录存在则不创建，并提示目录已存在
        print(path + ' 目录已存在')
        return False

"""
解压rar文件
需要安装WinRar并且配置环境变量
pip install rarfile
返回失败文件
"""


def un_rar(filepath):
    fail_path = ''
    try:
        if os.path.isdir(filepath + "-file"):
            pass
        else:
            zipname = filepath
            extractpath = filepath.replace(".rar", "") + '-file'
            rar = rarfile.RarFile(zipname)
            rar.extractall(extractpath)
            rar.close()
            # os.remove(extractpath)
            # print(f'成功文件:{get_file_name(filepath)}' )
    except Exception as e:
        print(f'失败文件为:{get_file_name(filepath)}--->>un_rar Exception file fail')
        fail_path = filepath
        pass
    return fail_path


# 删除空文件夹
def del_empty_file(dir_path):
    for root, dirs, files in os.walk(dir_path, topdown=False):
        for dir in dirs:
            try:
                os.rmdir(os.path.join(root, dir))  # 删除一个空目录
            except Exception as e:
                print(f'删除空文件夹,失败原因为:{e}')
                pass


"""
解压zip文件 返回失败文件
"""


def un_zip(filepath):
    fail_path = ''
    # 可以自己定义路径
    zipname = filepath
    extractpath = filepath.replace(".zip", "") + '-file'
    try:

        # 注意压缩格式选择
        frzip = zipfile.ZipFile(zipname, 'r', zipfile.ZIP_DEFLATED)
        # 将所有文件加压缩到指定目录
        frzip.extractall(extractpath)
        frzip.close()
    except Exception as e:
        print(f'失败文件为:{get_file_name(filepath)}')
        fail_path = filepath
        pass

    # 解压完成
    all_path_file = []
    all_path_dir = []
    for root, dirs, files in os.walk(extractpath):
        for file in files:
            file_kv = {'name': file, 'path': root}
            all_path_file.append(file_kv)
        for dir1 in dirs:
            # 文件深度
            deep_count = len(root.split('\\'))
            dir_kv = {'name': dir1, 'path': root, 'deep': deep_count}
            all_path_dir.append(dir_kv)
    # 一定是先文件再文件夹，否者重命名后文件夹内的文件找不到,先是最大深度文件夹，所以需要深度排序
    all_path_dir = sorted(all_path_dir, key=operator.itemgetter('deep'), reverse=True)

    for dic in all_path_file + all_path_dir:
        file_name = dic['name']
        parent_path = dic['path']
        file_name_ok = decode(file_name)
        err_path_name = os.path.join(parent_path, file_name)
        ok_path_name = os.path.join(parent_path, file_name_ok)
        os.rename(err_path_name, ok_path_name)  # 重命名文件

    return fail_path

class File:
    def __init__(self):
        self.fileList = []

    """
    递归列表文件
    """

    def recursion_file(self, filepath):
        files = os.listdir(filepath)
        for file in files:
            fi_d = os.path.join(filepath, file)
            if os.path.isdir(fi_d):
                self.recursion_file(fi_d)
            else:
                self.fileList.append(fi_d)

    """
    获取文件列表
    """

    def get_file_list(self, filepath):
        self.recursion_file(filepath)
        return self.fileList