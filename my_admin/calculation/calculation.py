import datetime

from _decimal import Decimal
from flask import request, Blueprint

from config.mysql_file import mysql_info_local
from utils.mysql import Mysql

# 查询历史电费信息列表  可以指定前缀路由url_prefix='/manage'
query_calculation_blue = Blueprint('query_calculation', __name__)


@query_calculation_blue.route('/query_calculation_all', methods=['POST'])
def query_calculation():
    if request.method == 'POST':
        pageSize = request.json['pageSize']
    else:
        pageSize = request.args.get('pageSize')
    return {'errorCode': 0, 'data': query_calculation_all(pageSize)}


# 计算电费 可以指定前缀路由url_prefix='/manage'
contract_blue = Blueprint('calculation', __name__)


@contract_blue.route('/calculation', methods=['POST'])
def calculation():
    params = {
        "electric_quantity_1": Decimal(request.json['electric_quantity_1']),
        "electric_quantity_2": Decimal(request.json['electric_quantity_2']),
        "electric_quantity_3": Decimal(request.json['electric_quantity_3']),
        "amount": Decimal(request.json['amount'])
    }
    return {'errorCode': 0, 'data': calculation_amount(params)}


def calculation_amount(params):
    amount = params["amount"]
    electric_quantity_1 = params["electric_quantity_1"]
    electric_quantity_2 = params["electric_quantity_2"]
    electric_quantity_3 = params["electric_quantity_3"]
    dict_map = {
        "①": electric_quantity_1,
        "②": electric_quantity_2,
        "③": electric_quantity_3
    }
    last_month_calculation_list = query_month_calculation(get_last_month())
    if len(last_month_calculation_list) != 3:
        raise RuntimeError("获取上月电费信息异常，请检查数据!!!")
    # 上月总电量
    last_total_electric_quantity = sum(list(map(lambda v: v["electric_quantity"], last_month_calculation_list)))
    # 当月总电量
    total_electric_quantity = electric_quantity_1 + electric_quantity_2 + electric_quantity_3
    # 当月已用电量
    used_total_electricity = total_electric_quantity - last_total_electric_quantity
    # 单价
    unit_price = (amount / used_total_electricity).quantize(Decimal('0.00000'))
    print("单价 %s" % unit_price)

    # 查询清理本月记录
    month = get_month()
    month_calculation_list = query_month_calculation(month)
    for month_calculation in month_calculation_list:
        update_calculation(month_calculation["id"])

    info_list = list()
    file_path = "../sql/电费记录表初始化语句.sql"
    # 删除文件的最后一个字符
    del_file_last_character(file_path)
    for last_month_calculation in last_month_calculation_list:
        name_ = last_month_calculation["name"]
        month_calculation = dict_map[name_]
        electric_quantity_ = month_calculation - last_month_calculation["electric_quantity"]
        amount = (unit_price * electric_quantity_).quantize(Decimal('0.00000'))
        avg_calculation_list = query_avg_calculation()
        avg_calculations = list(filter(lambda v: v["name"] == name_, avg_calculation_list))
        average_used_electricity = round(sum(map(lambda v: v["average_used_electricity"], avg_calculations)))
        average_amount = round(sum(map(lambda v: v["average_amount"], avg_calculations)))
        body = {
            "name_": name_,
            "month_calculation": month_calculation,
            "electric_quantity": electric_quantity_,
            "unit_price": str(unit_price) + "元",
            "amount": amount,
            "average_used_electricity": str(average_used_electricity) + "°",
            "average_amount": str(average_amount) + "元"
        }
        values = (name_, month_calculation, electric_quantity_, unit_price, amount, month)
        insert_calculation(values)
        # 追加内容至指定文件
        open_file(file_path,
                  """,\n('{}', {}, {}, '{}', '{}', '{}')""".format(name_, month_calculation, electric_quantity_,
                                                                   unit_price, amount,
                                                                   month))
        info_list.append(body)
    open_file(file_path, ";")
    return info_list


def query_calculation_all(pageSize):
    sqlStr = f"""SELECT
                        id,
                     	`name`,
                     	electric_quantity,
                     	used_electricity,
                     	unit_price,
                     	amount,
                     	date_calculation 
                     FROM
                     	calculation 
                     WHERE
                     	deleted = 0
                     ORDER BY date_calculation DESC
                     LIMIT {pageSize}"""

    db = Mysql(mysql_info_local)
    calculation_list = db.get_data_all(sqlStr)
    db.close_mysql()
    return calculation_list

# 删除指定文件的最后一个字符
def del_file_last_character(file_path):
    # 读取文件
    with open(file_path, "r", encoding='utf-8') as file:
        old_content = file.read()
    # 删除文件内最后一个字符
    old_content = old_content[:-1]
    # 重新写入文件
    with open(file_path, "w", encoding='utf-8') as file:
        file.write(old_content)


# 将内容写入指定目录文件内
def open_file(file_path, content):
    # with open(file_path, 'w') as f:  'w' 每次覆盖 'a' 追加
    with open(file_path, 'a', encoding='utf-8') as f:
        f.write(content)
        f.close()

# 查询近6个月的平均电费及用电量
def query_avg_calculation():
    sqlStr = f"""SELECT
                    `name`,
                    AVG( amount ) AS average_amount,
                    AVG( used_electricity ) AS average_used_electricity 
                FROM
                    `calculation` 
                WHERE
                    deleted = 0 
                    AND date_calculation > date_format( DATE_SUB( CURDATE(), INTERVAL 6 MONTH ), '%Y-%m' ) 
                GROUP BY
                    `name`"""

    db = Mysql(mysql_info_local)
    avg_calculation_list = db.get_data_all(sqlStr)
    db.close_mysql()
    return avg_calculation_list


# 查询某月电费信息
def query_month_calculation(month):
    if month is None:
        raise RuntimeError("查询电量月份为空!")
    sqlStr = f"""SELECT
                    id,
                 	`name`,
                 	electric_quantity,
                 	used_electricity,
                 	unit_price,
                 	amount,
                 	date_calculation 
                 FROM
                 	calculation 
                 WHERE
                 	deleted = 0 
                 	AND date_calculation = + '{month}'"""

    db = Mysql(mysql_info_local)
    month_calculation_list = db.get_data_all(sqlStr)
    db.close_mysql()
    return month_calculation_list


def insert_calculation(values):
    insert_sql = """INSERT INTO `calculation` (`name`, `electric_quantity`, `used_electricity`, `unit_price`, `amount`, `date_calculation`)
                        VALUES(%s, %s, %s, %s, %s, %s)"""
    db = Mysql(mysql_info_local)
    db.insert_data(insert_sql, values)
    db.close_mysql()


def update_calculation(calculation_id):
    update_sql = f"""UPDATE `calculation` 
                    SET `deleted` = 1 
                    WHERE
                    	`id` = {calculation_id}"""
    db = Mysql(mysql_info_local)
    db.update_data(update_sql)
    db.close_mysql()


# 获取上月日期
def get_last_month():
    today = datetime.date.today()
    first_day = today.replace(day=1)
    last_month = first_day - datetime.timedelta(days=1)
    return last_month.strftime('%Y-%m')


# 获取当月日期
def get_month():
    today = datetime.date.today()
    first_day = today.replace()
    last_month = first_day - datetime.timedelta()
    return last_month.strftime('%Y-%m')

# if __name__ == '__main__':
#     i = int(input("当前①电量："))
#     int1 = int(input("当前②电量："))
#     int2 = int(input("当前③电量："))
#     int3 = int(input("本月电费："))
#     parms = {
#         "electric_quantity_1": i,
#         "electric_quantity_2": int1,
#         "electric_quantity_3": int2,
#         "amount": int3
#     }
#     print(calculation_amount(parms))
#     print(get_month())
