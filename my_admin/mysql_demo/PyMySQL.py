import pymysql

# 连接数据库
db = pymysql.connect(host='172.16.86.51'  # 连接名称
                     , user='tb_boss'  # 用户名
                     , passwd='Upa!23qwe'  # 密码
                     , port=3306  # 端口，默认为3306
                     , db='tb_boss_dev'  # 数据库名称
                     , charset='utf8'  # 字符编码
                     )
cur = db.cursor()  # 生成游标对象
sql = "select * from `tbs_final_bill` "  # SQL语句
cur.execute(sql)  # 执行SQL语句
data = cur.fetchall()  # 通过fetchall方法获得数据 返回所有
# print(cur.fetchone())  # 返回第一条
print("===============================================================")
# print(cur.fetchmany(2))  # 返回自定义条数，不传默认返回第一条
print("===============================================================")
for i in data[:2]:  # 打印输出前2条数据
    print(i)
cur.close()  # 关闭游标
db.close()  # 关闭连接
