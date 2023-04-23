import logging
import os
import random

from flask import request, Blueprint

from config.get_config import Config
from parser.parser import config_args
from utils.LoggerUtil import LogUtil
from utils.httpUtil import httpUtils
from utils.login import get_token
from utils.mysql import Mysql

mysql, url = Config().return_config(config_args)

url_host = url["host"]
LOGIN_URL = url_host + "/api/auth/login"
PROCESS_URL = url_host + "/process/process"
IMG_URL = url_host + "/work/flow/query/view/process/img"

http = httpUtils()
log = LogUtil(log_level=logging.DEBUG).getLogger()

# 可以审批的表单状态
form_status_list = [1, 2, 3]
# 表单特殊节点流程定义id
task_definition_key_map = {
    "customer_main_process_v2": ["A2"],  # 客户信息
    "customer_sub_process_v2": [],  # 子账号信息
    "customer_contact_process_v2": [],  # 联系人信息
    "project_main_process_v2": [],  # 立项信息
    "contract_main_process_v2": ["contract_management", "apply_user"],  # 法审信息
    "customer_access_process_v2": ["deploymentGroup", "creditConsignManager"],  # 客户接入信息
    "data_extract_approval_main_process_v2": ["complianceReviewGroup4", "dataExtractAdministrato",
                                              "dataExtractAdministrato2",
                                              "dataExtractAdministrato3",
                                              "dataExtractStaff2",
                                              "dataExtractStaff3",
                                              "demandDepartmentAnalyst",
                                              "demandDepartmentAnalyst2",
                                              "dataExtractStaff"],  # 提数申请信息
    "quote_approval_main_process_v2": [],  # 报价信息
    "customer_invoice_process_v2": ["headOfficeFinance", "beijingBranchFinance"],  # 开票信息
    "calculate_approval_main_process_v2": ["repoweb_group", "debug_group"],  # 计费管理信息
    "api_become_regular_process_v2": [],  # 接口转正流程
    "bill_approval_main_process_v2": [],  # 直连账单
    "bill_approval_commission_process_v2": []  # 代理账单
}

# 登录
login_blue = Blueprint('login', __name__)


@login_blue.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.json['username']
        password = request.json['password']
    else:
        username = request.args.get('username')
        password = request.args.get('password')
    code = 0 if ('HuiGeGe' == username) & ('123123' == password) else 8888
    return {'errorCode': code, 'data': 'ok'}


# 根据formNo获取表单信息集合
query_form_all_blue = Blueprint('query_form_all', __name__)


@query_form_all_blue.route('/query_form_all', methods=['GET', 'POST'])
def query_form_all():
    if request.method == 'POST':
        params = {
            "form_no": request.json['form_no'],
            "apply_user": request.json['apply_user'],
            "form_key": request.json['form_key'],
            "form_status": request.json['form_status'],
            "process_ins_id": request.json['process_ins_id'],
            "form_title": request.json['form_title'],
            "pageSize": request.json['pageSize']
        }
    else:
        params = {
            "form_no": request.args.get('form_no'),
            "apply_user": request.args.get('apply_user'),
            "form_key": request.args.get('form_key'),
            "form_status": request.args.get('form_status'),
            "process_ins_id": request.args.get('process_ins_id'),
            "form_title": request.args.get('form_title'),
            "pageNum": request.args.get('pageNum'),
            "pageSize": request.args.get('pageSize')
        }
    return {'errorCode': 0, 'data': query_form_list(params)}


# 根据formNo获取表单当前节点
query_process_node_by_form_no_blue = Blueprint('query_process_node_by_form_no', __name__)


@query_process_node_by_form_no_blue.route('/query_process_node_by_form_no', methods=['GET', 'POST'])
def query_process_node_by_form_no():
    if request.method == 'POST':
        form_no = request.json['formNo']
    else:
        form_no = request.args.get('formNo')
    return {'errorCode': 0, 'data': queryProcessNode(form_no)}


# 单节点审批
approval_blue = Blueprint('approval', __name__)


@approval_blue.route('/approval', methods=['GET', 'POST'])
def approval():
    if request.method == 'POST':
        form_no = request.json['formNo']
    else:
        form_no = request.args.get('formNo')
    check_form_no = empty_check(form_no)
    if check_form_no:
        return {'errorCode': 8888, 'errorMessage': "表单单号不能为空。。。"}
    # 查询表单信息
    form = query_task_by_form_no(form_no)
    # 检查表单情况
    response = check_form(form, form_no)
    if response is not None:
        return response
    # 审批
    rep, approval_info = process(form)

    # 返回下个节点审批信息
    # return {'errorCode': 0, 'data': queryProcessNode(form_no)}
    return {'errorCode': 0}


# 一键审批
one_key_approval_blue = Blueprint('one_key_approval', __name__)


@one_key_approval_blue.route('/one_key_approval', methods=['GET', 'POST'])
def one_key_approval():
    if request.method == 'POST':
        form_no = request.json['formNo']
    else:
        form_no = request.args.get('formNo')
    result = empty_check(form_no)
    if result:
        return {'errorCode': 8888, 'errorMessage': "表单单号不能为空..."}
    # approval_info_list = list()
    while (True):
        # 查询表单信息
        form = query_task_by_form_no(form_no)
        # 检查表单情况
        response = check_form(form, form_no)
        if response is not None:
            return response
        # 审批
        rep, approval_info = process(form)
        # approval_info_list.append(approval_info)


# 查看流程图
view_process_img_blue = Blueprint('view_process_img', __name__)


@view_process_img_blue.route('/view_process_img', methods=['GET', 'POST'])
def view_process_img():
    if request.method == 'POST':
        form_no = request.json['formNo']
    else:
        form_no = request.args.get('formNo')
    result = empty_check(form_no)
    if result:
        return {'errorCode': 8888, 'errorMessage': "表单单号不能为空..."}
    form = query_task_by_form_no(form_no)
    result = empty_check(form)
    if result:
        return {'errorCode': 8888, 'errorMessage': "表单信息缺失..."}
    url = IMG_URL + f"""?formNo={form_no}&processDefinitionKey={form["form_key"]}"""
    rep = http.get(url=url, headers=build_headers('shouzhen.qu'))
    return {'errorCode': 0, 'data': rep.json()['data']}


# 根据formNo获取表单发起流程图，修改
query_flow_chart_by_form_no_blue = Blueprint('query_flow_chart_by_form_no', __name__)


@query_flow_chart_by_form_no_blue.route('/query_flow_chart_by_form_no', methods=['GET', 'POST'])
def query_flow_chart_by_form_no():
    global update_sql
    if request.method == 'POST':
        form_no = request.json['formNo']
    else:
        form_no = request.args.get('formNo')
    sqlStr = f"""SELECT DISTINCT 
                    RES.PROC_DEF_ID_,
                    ARP.DEPLOYMENT_ID_,
                    AGB.ID_,
                    AGB.NAME_,
                    AGB.BYTES_,
                    AGB.DEPLOYMENT_ID_,
                    DEF.KEY_ AS PROC_DEF_KEY_,
                    DEF.NAME_ AS PROC_DEF_NAME_,
                    DEF.VERSION_ AS PROC_DEF_VERSION_,
                    DEF.DEPLOYMENT_ID_ AS DEPLOYMENT_ID_ 
                FROM tbs_activity_form TAF 
                LEFT JOIN ACT_HI_PROCINST RES ON RES.PROC_INST_ID_ = TAF.process_ins_id 
                LEFT OUTER JOIN ACT_RE_PROCDEF DEF ON RES.PROC_DEF_ID_ = DEF.ID_  
                LEFT JOIN ACT_RE_PROCDEF ARP ON ARP.ID_ = RES.PROC_DEF_ID_ 
                LEFT JOIN ACT_GE_BYTEARRAY AGB ON AGB.DEPLOYMENT_ID_ = ARP.DEPLOYMENT_ID_ 
                WHERE TAF.form_no = + '{form_no or ''}'
                ORDER BY RES.ID_,AGB.NAME_ ASC"""

    db = Mysql(mysql)
    data = db.get_data(sqlStr)

    for i in range(len(data)):
        id_ = data[i]["ID_"]
        xml_name_ = data[i]["NAME_"]
        content_ = data[i]["BYTES_"]
        deployment_id_ = data[i]["DEPLOYMENT_ID_"]
        print(xml_name_)
        if not ('xml' in xml_name_):
            continue
        if content_ == '':
            continue

        parent_path = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))),
                                   xml_name_)  # 获取当前文件所在目录的父级目录的绝对路径
        print(parent_path)
        write_file(content_, parent_path)  # 文件写入本地

        result = input('是否修改完成(Y/N): ')
        resultList = ['y', 'Y', 'YES', 'yes']
        while not resultList.__contains__(result):
            result = input('是否修改完成(Y/N): ')

        new_content_ = convert_to_binary_data(parent_path)  # 本地文件写入数据库

        update_sql = f"""UPDATE 
                            `ACT_GE_BYTEARRAY` 
                        SET `BYTES_` = + {new_content_ or ''} 
                        WHERE `ID_`  = + {id_ or ''} 
                        AND `NAME_`  = + {xml_name_ or ''} 
                        AND `DEPLOYMENT_ID_` =  = + {deployment_id_ or ''} """
    db.update_data(update_sql)
    db.close_mysql()
    return '执行成功！'


# 查询所有表单信息
def query_form_list(params):
    form_no = params["form_no"]
    apply_user = params["apply_user"]
    form_key = params["form_key"]
    form_status = params["form_status"]
    process_ins_id = params["process_ins_id"]
    form_title = params["form_title"]
    pageSize = params["pageSize"]
    sqlStr = f"""SELECT
                	form_no,
                	form_title,
                	apply_user,
                	form_key,
                	process_ins_id,
                	form_status,
                	DATE_FORMAT( create_time,'%Y-%m-%d %H:%i:%s' ) create_time,
                	update_time 
                FROM
                	tbs_activity_form 
                WHERE
                	deleted = 0"""
    if (form_no is not None) & (len(form_no) > 0):
        sqlStr += f""" AND form_no = '{form_no}'"""
    if (apply_user is not None) & (len(apply_user) > 0):
        sqlStr += f""" AND apply_user = '{apply_user}'"""
    if (form_key is not None) & (len(form_key) > 0):
        sqlStr += f""" AND form_key = '{form_key}'"""
    if (form_status is not None) & (len(form_status) > 0):
        sqlStr += f""" AND form_status = {form_status}"""
    if (process_ins_id is not None) & (len(process_ins_id) > 0):
        sqlStr += f""" AND process_ins_id = {process_ins_id}"""
    if (form_title is not None) & (len(form_title) > 0):
        sqlStr += f""" AND form_title like '{form_title}'"""
    sqlStr += f"""
                ORDER BY update_time DESC 
                LIMIT {pageSize} """
    db = Mysql(mysql)
    form_list = db.get_data_all(sqlStr)
    db.close_mysql()
    return form_list


# 审批
def process(form):
    form_no = form["form_no"]
    # 查询审批人
    assignee_list = query_assignee_list(form)
    result = empty_check(assignee_list)
    if result:
        return {'errorCode': 8888, 'errorMessage': "审批人员为空，请确保表单正常。。。form_no= %s" % form_no}
    # 构建审批参数
    body = build_body(form_no)
    user_name = assignee_list[random.randrange(len(assignee_list))]
    header = build_headers(user_name)
    approval_info = "开始执行自动审批任务：表单单号=[%s] 当前节点=[%s] 当前审批人=[%s] 发起人=[%s] 表单标题=[%s]" % (
        form_no, form["NAME_"], user_name, form["apply_user"], form["form_title"])
    log.critical(approval_info)
    # 执行审批
    rep = http.post(url=PROCESS_URL, body=body, headers=header)
    return rep, approval_info


'''
0-保存待发, 草稿状态 撤回,回退发起人
1-发起审批流程, 进行中状态
2-流程审批, 审批中状态
3-定向回退(流程中节点)
4-审批结束, 完成状态
5-审批终止, 终止状态
6-审批拒绝
7-撤回
12-表示进行中+审批中状态仅用于查询列表使用'''


# 检查表单信息
def check_form(form, form_no):
    check_form_result = empty_check(form)
    if check_form_result:
        return {'errorCode': 8888, 'errorMessage': "不存在的表单%s..." % form_no}

    form_status = form["form_status"]
    if form["form_status"] == 4:
        return {'errorCode': 0, 'data': "表单已经全部审批通过啦!"}

    # 支持审批的表单状态
    result_check_contains = not_contains_check(form_status_list, form_status)
    if result_check_contains:
        return {'errorCode': 8888, 'errorMessage': "不支持的表单审批状态，请确认后开审...form_no= %s" % form_no}

    form_key = form["form_key"]
    task_def_key_ = form["TASK_DEF_KEY_"]
    task_def_name__ = form["NAME_"]

    # 获取表单特殊节点
    definition_key_List = task_definition_key_map[form_key]
    result_definition_check = contains_check(definition_key_List, task_def_key_)
    if result_definition_check:
        errorMessage = "表单form_no[%s] 节点[%s] 为特殊节点，task_def_key_=[%s] 不支持自动审批，请手动处理！" % (
            form_no, task_def_name__, task_def_key_)
        return {'errorCode': 8888, 'errorMessage': errorMessage}
    log.debug(form)


# 查询待办人
def query_assignee_list(form):
    process_ins_id = form["process_ins_id"]
    form_no = form["form_no"]
    # 查询当前任务节点
    form_task_list = query_task_list_by_process_ins_id(process_ins_id)
    result = empty_check(form_task_list)
    if result:
        return {'errorCode': 8888, 'errorMessage': "当前表单单号查询审批任务节点不存在...form_no= %s" % form_no}
    # 待办人集合
    assignee_set = set()
    log.debug(form_task_list)
    for form_task in form_task_list:
        run_task_id = form_task["ID_"]
        run_task_assignee = form_task["ASSIGNEE_"]
        if run_task_assignee is not None:
            assignee_set.add(run_task_assignee)
        # 查询任务参与着(自定义角色组)
        identity_link_list = query_ru_identity_link(run_task_id)
        if identity_link_list is None:
            continue
        log.debug(identity_link_list)
        for identity_link in identity_link_list:
            user_id_ = identity_link["USER_ID_"]
            if user_id_ is not None:
                assignee_set.add(user_id_)
    return list(assignee_set)


# 根据formNo获取当前表单节点信息
def query_task_by_form_no(form_no):
    sqlStr = f"""SELECT  
                ACF.form_no, 
                ACF.form_title, 
                ACF.process_ins_id, 
                ACF.apply_user, 
                ACF.form_key, 
                ACF.form_status, 
                ACF.form_data,
                ART.TASK_DEF_KEY_,
	            ART.NAME_,
	            ART.ASSIGNEE_ 
             FROM  
                `tbs_activity_form` ACF  
             LEFT JOIN ACT_RU_TASK ART ON ACF.process_ins_id = ART.PROC_INST_ID_ 
             WHERE ACF.deleted = 0  
             AND ACF.form_no = + '{form_no or ''}'"""

    db = Mysql(mysql)
    form_task_list = db.get_data_one(sqlStr)
    db.close_mysql()
    return form_task_list


# 根据process_ins_id获取当前表单审批task_list
def query_task_list_by_process_ins_id(process_ins_id):
    sqlStr = f"""SELECT 
                RES.ID_, 
                RES.ASSIGNEE_, 
                RES.NAME_  
             FROM  
                `ACT_RU_TASK` RES  
             WHERE RES.PROC_INST_ID_ = + '{process_ins_id or ''}'"""

    db = Mysql(mysql)
    form_task_list = db.get_data_all(sqlStr)
    db.close_mysql()
    return form_task_list


# 根据run_task_id获取当前task审批人员
def query_ru_identity_link(run_task_id):
    sqlStr = f"""SELECT
	                ID_,
	                TYPE_,
	                USER_ID_
                FROM
	               ACT_RU_IDENTITYLINK
	            WHERE
	               TASK_ID_ = + '{run_task_id or ''}'"""

    db = Mysql(mysql)
    form_identity_link_list = db.get_data_all(sqlStr)
    db.close_mysql()
    return form_identity_link_list


# 根据form_no获取当前表单节点信息
def queryProcessNode(form_no):
    # sqlStr = "SELECT
    # AC.form_no,
    # AC.apply_user,
    # PROC_INST_ID_,
    # AC.form_key,
    # ACT_ID_,
    # ACT_NAME_,
    # ASSIGNEE_,
    # START_TIME_
    # FROM tbs_activity_form AC
    # LEFT JOIN ACT_HI_ACTINST ON AC.process_ins_id = PROC_INST_ID_
    # WHERE AC.deleted = 0 AND AC.form_no =" + "'" + _form_no + "'" +
    # "AND ID_ IN (SELECT MAX( ID_ )
    # FROM ACT_HI_ACTINST GROUP BY PROC_INST_ID_)"
    sqlStr = f"""SELECT
                    AC.form_no,
                    AC.apply_user,
                    PROC_INST_ID_,
                    AC.form_key,
                    AC.form_title,
                    ID_,
                    TASK_DEF_KEY_,
                    NAME_,
                    ASSIGNEE_,
                    DATE_FORMAT( CREATE_TIME_,'%Y-%m-%d %H:%i:%s' ) CREATE_TIME_
                FROM tbs_activity_form AC
                LEFT JOIN ACT_RU_TASK ON AC.process_ins_id = PROC_INST_ID_
                WHERE AC.deleted = 0
                AND AC.form_no = + '{form_no or ''}'"""

    db = Mysql(mysql)
    data = db.get_data_all(sqlStr)
    db.close_mysql()
    for item in data:
        if item["ASSIGNEE_"] is None:
            item["ASSIGNEE_"] = ",".join(list(map(lambda v: v["USER_ID_"], query_ru_identity_link(item["ID_"]))))
    return data


def empty_check(obj):
    return True if not obj else False


def contains_check(list_obj, obj):
    return True if list_obj.__contains__(obj) else False


def not_contains_check(list_obj, obj):
    return True if not list_obj.__contains__(obj) else False


def build_body(form_no):
    body = {
        "formNo": form_no,
        "comment": "管理员自动审批跳过"
    }
    return body


def build_headers(user_name):
    # 获取token
    password = "upa.123"
    headers = {
        'X-Content-Auth': get_token(LOGIN_URL, user_name, password),
        "Content-Type": "application/json;charset=UTF-8"
    }
    return headers


def convert_to_binary_data(filename):
    # Convert digital data to binary format
    with open(filename, 'rb') as file:
        binaryData = file.read()
    return binaryData


def write_file(data, filename):
    # Convert binary data to proper format and write it on Hard Disk
    with open(filename, 'wb') as file:
        file.write(data)
