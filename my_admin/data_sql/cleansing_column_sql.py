import json
import logging
import os
import time

from config.get_config import Config
from parser.parser import config_args
from utils.LoggerUtil import LogUtil
from utils.mysql import Mysql

log = LogUtil(log_level=logging.DEBUG)
mysql, url = Config().return_config(config_args)
# 在分的基础上清洗金额字段
multiply_fen_ = 100
# 在？元的基础上清洗金额字段
multiply_yuan_ = 10000
# 初始文件目录
new_time = time.strftime("%Y_%m_%d_%H_%M_%S", time.localtime())


# 金额列(现为分) 乘 100 单位变为 毫（小数点后4位）
def print_cleansing_column(table_column_map):
    # 判断文件夹是否存在，不存在则创建
    if not os.path.exists(new_time):
        os.makedirs(new_time)
    # 打开文件并将字符串写入文件中
    file_path = '{}/update_column.sql'.format(new_time)
    for table_name, column_names in table_column_map.items():
        sql = '''UPDATE {} \n'''.format(table_name)
        set_clauses = [f"{column_name} = {column_name} * {multiply_fen_}" for column_name in column_names]
        sql += ' SET ' + ', \n'.join(set_clauses) + ';\n'
        print(sql)
        open_file(file_path, sql)


# 特殊处理:分润报价阶梯为金额
def print_quote_ladder_rule_column():
    if not os.path.exists(new_time):
        os.makedirs(new_time)
    # 打开文件并将字符串写入文件中
    rollback_file_path = '{}/rollback_quote_ladder_rule_column.sql'.format(new_time)

    update_file_path = '{}/update_quote_ladder_rule_column.sql'.format(new_time)
    # 查询所有的分润报价获取其报价规则编号集合 List<String> quote_sub_code_list
    quote_sub_code_list = query_quote_sub_code_list()
    for quote_sub_code in quote_sub_code_list:
        quote_product_rule_code = quote_sub_code['quote_product_rule_code']
        quote_ladder_rule_list = query_quote_ladder_rule_list(quote_product_rule_code)
        if quote_ladder_rule_list:
            for quote_ladder_rule in quote_ladder_rule_list:
                start_scope_ = int(quote_ladder_rule['start_scope'])

                rule_end_scope_ = quote_ladder_rule['end_scope']
                end_scope_ = '∞' if rule_end_scope_ == '∞' else int(rule_end_scope_)
                rollback_sql = get_update_quote_ladder(quote_ladder_rule, start_scope_, end_scope_)
                print(rollback_sql)
                open_file(rollback_file_path, rollback_sql + '\n')
                scope__multiply_fen_ = '∞' if end_scope_ == '∞' else end_scope_ * multiply_fen_
                update_sql = get_update_quote_ladder(quote_ladder_rule, start_scope_ * multiply_fen_,
                                                     scope__multiply_fen_)
                print(update_sql)
                open_file(update_file_path, update_sql + '\n')


# 给定字典,修改其字段备注
def print_cleansing_column_comment_remark(table_column_comment_remark_map):
    if not os.path.exists(new_time):
        os.makedirs(new_time)
    file_path = '{}/update_column_remark.sql'.format(new_time)
    for table_name, column_names in table_column_comment_remark_map.items():
        sql = '''ALTER TABLE `{}` \n'''.format(table_name)
        for index, column_name in enumerate(column_names):
            for field, remark in column_name.items():
                new_remark = '分' in remark and remark.replace(":分", ":毫（小数点后4位）") or insert_string(remark,
                                                                                                           ' 单位:毫（小数点后4位）',
                                                                                                           2)
                if index == len(column_names) - 1:
                    sql = sql + '''MODIFY COLUMN `{}` {}; \n'''.format(field, new_remark)
                else:
                    sql = sql + '''MODIFY COLUMN `{}` {}, \n'''.format(field, new_remark)
        print(sql)
        open_file(file_path, sql)


# 更新formData字段
def print_activity_form_data():
    if not os.path.exists(new_time):
        os.makedirs(new_time)
    file_path = '{}/update_activity_form_data.sql'.format(new_time)
    rollback_file_path = '{}/rollback_activity_form_data.sql'.format(new_time)
    form_list = query_form_list()
    for activity_form in form_list:
        # 处理特殊字符被转义的问题
        form_data_ = json.dumps(json.loads(activity_form['form_data']), ensure_ascii=False)
        rollback_sql = get_update_form(form_data_, activity_form['form_no'])
        print(rollback_sql)
        open_file(rollback_file_path, rollback_sql + '\n')
        # 根据流程定义key 处理不同的json
        form_key_ = activity_form['form_key']
        match form_key_:
            case 'data_extract_approval_main_process_v2':
                sql = case_data_extract(activity_form)
            case 'customer_invoice_process_v2':
                sql = case_invoice(activity_form)
            case 'quote_approval_main_process_v2':
                sql = case_quote(activity_form)
            case 'product_launch_process_v2' | 'product_offline_process_v2' | 'product_upgrades_process_v2':
                sql = case_product(activity_form)
            case 'bill_approval_main_process_v2':
                sql = case_bill(activity_form)
            case 'bill_approval_commission_process_v2':
                sql = case_bill_commission(activity_form)
            case 'cost_approval_main_process_v2':
                sql = case_cost(activity_form)
            case _:
                sql = default(activity_form)
        print(sql)
        open_file(file_path, sql + '\n')
    """
        1、查詢所有需要刷的form deleted = 0 所需字段（form_no、form_key、form_data）
        2、根据formKey获取该实体需要清洗的字段属性并计算
        3、生成formData更新语句 UPDATE `tbs_activity_form` SET `form_data` = '' WHERE `form_no` = '';
    """


# 将内容写入指定目录文件内
def open_file(file_path, content):
    # with open(file_path, 'w') as f:  'w' 每次覆盖 'a' 追加
    with open(file_path, 'a', encoding='utf-8') as f:
        f.write(content)
        f.close()


# 在给定字符串original_string给定个数size个字符（字典定义问题）前插入字符 specific_string
def insert_string(original_string, specific_string, size):
    length = len(original_string)
    return original_string[:length - size] + specific_string + original_string[length - size:]


# 将数据库字段转换为驼峰命名
def to_camel_case(s):
    return ''.join([word.capitalize() if i != 0 else word for i, word in enumerate(s.split('_'))])


# 数据提取金额精度调整清洗
def case_data_extract(activity_form):
    form_no_ = activity_form['form_no']
    not_empty, form_data = _get_form_data(activity_form)
    if not not_empty:
        return """# 数据提取表单{} form_data为空! 跳过数据清洗.""".format(form_no_)
    column_list = ['unit_price', 'amt']
    count = 0
    for column_name in column_list:
        # 将数据库字段转换为实体属性(驼峰命名)
        columnName = to_camel_case(column_name)
        try:
            form_data[columnName] = form_data[columnName] * multiply_yuan_
            # 设置成功值加1
            count = count + 1
        except (TypeError, KeyError):
            continue
    if count == 0:
        return "# 该表单,没有任何字段修改 formNo=[{}]".format(form_no_)
    json_data = json.dumps(form_data, ensure_ascii=False)
    return get_update_form(json_data, form_no_)


# 开票单金额精度调整清洗
def case_invoice(activity_form):
    form_no_ = activity_form['form_no']
    not_empty, form_data = _get_form_data(activity_form)
    if not not_empty:
        return """# 开票表单{} form_data为空! 跳过数据清洗.""".format(form_no_)
    column_list = ['invoice_amount', 'prepaid_amount', 'prepaid_used_amount', 'prepaid_left_amount']
    count = 0
    for column_name in column_list:
        # 将数据库字段转换为实体属性(驼峰命名)
        columnName = to_camel_case(column_name)
        try:
            # 开票申请单参数接收注解已转换，在分的基础上乘!
            form_data[columnName] = form_data[columnName] * multiply_fen_
            # 设置成功值加1
            count = count + 1
        except (TypeError, KeyError):
            continue
    if count == 0:
        return "# 该表单,没有任何字段修改 formNo=[{}]".format(form_no_)
    json_data = json.dumps(form_data, ensure_ascii=False)
    return get_update_form(json_data, form_no_)


# 报价单金额精度调整清洗
def case_quote(activity_form):
    form_no_ = activity_form['form_no']
    not_empty, form_data = _get_form_data(activity_form)
    if not not_empty:
        return """# 报价表单{} form_data为空! 跳过数据清洗.""".format(form_no_)
    try:
        quote_product_list = form_data['quoteProductVOList']
    except (TypeError, KeyError) as e:
        return """# 报价表单{} 异常,缺少报价规则! 跳过数据清洗.error={}""".format(form_no_, e)
    if not quote_product_list:
        return """# 报价表单{} 异常,报价规则为空! 跳过数据清洗.""".format(form_no_)
    quote_sub_column_list = ['basic_price', 'channel_price', 'total_price', 'unit_price', 'advance_amt', 'contract_amt']
    count = 0
    for quote_product in quote_product_list:
        try:
            quote_ladder_rule_list = quote_product['quoteLadderRule']
        except (TypeError, KeyError):
            try:
                quote_ladder_rule_list = quote_product['reqRuleJson']
            except (TypeError, KeyError):
                quote_ladder_rule_list = ()
        if quote_ladder_rule_list:
            for quote_ladder_rule in quote_ladder_rule_list:
                try:
                    # 报价申请单参数接收注解已转换，在分的基础上乘!
                    unit_price = to_camel_case('unit_price')
                    quote_ladder_rule[unit_price] = quote_ladder_rule[unit_price] * multiply_fen_
                    # 设置成功值加1
                    count = count + 1
                except (TypeError, KeyError):
                    continue
        for quote_sub_column_name in quote_sub_column_list:
            # 将数据库字段转换为实体属性(驼峰命名)
            columnName = to_camel_case(quote_sub_column_name)
            try:
                # 报价申请单参数接收注解已转换，在分的基础上乘!
                quote_product[columnName] = quote_product[columnName] * multiply_fen_
                # 设置成功值加1
                count = count + 1
            except (TypeError, KeyError):
                continue
    if count == 0:
        return "# 该表单,没有任何字段修改 formNo=[{}]".format(form_no_)
    json_data = json.dumps(form_data, ensure_ascii=False)
    return get_update_form(json_data, form_no_)


# 产品单金额精度调整清洗
def case_product(activity_form):
    form_no_ = activity_form['form_no']
    not_empty, form_data = _get_form_data(activity_form)
    if not not_empty:
        return """# 产品表单{} form_data为空! 跳过数据清洗.""".format(form_no_)
    try:
        segment_price_form_list = form_data['segmentPriceFormRequestList']
    except (TypeError, KeyError) as e:
        return """# 产品表单{} 异常,缺少产品基准价格! 跳过数据清洗.error={}""".format(form_no_, e)
    if not segment_price_form_list:
        return """# 产品表单{} 异常,产品基准价格为空! 跳过数据清洗.""".format(form_no_)
    count = 0
    for segment_price_form in segment_price_form_list:
        try:
            # 产品申请单参数接收注解已转换，在分的基础上乘!
            unitPrice = to_camel_case('unit_price')
            segment_price_form[unitPrice] = segment_price_form[unitPrice] * multiply_fen_
            # 设置成功值加1
            count = count + 1
        except (TypeError, KeyError):
            continue
    if count == 0:
        return "# 该表单,没有任何字段修改 formNo=[{}]".format(form_no_)
    json_data = json.dumps(form_data, ensure_ascii=False)
    return get_update_form(json_data, form_no_)


# 收入账单金额精度调整清洗
def case_bill(activity_form):
    form_no_ = activity_form['form_no']
    not_empty, form_data = _get_form_data(activity_form)
    if not not_empty:
        return """# 收入账单表单{} form_data为空! 跳过数据清洗.""".format(form_no_)
    # 字段特殊json和数据库有差异，按Java实体来 com.upa.vo.bill.req.BillFormRequestVO
    bill_column_list = ['calculateFee', 'billAmt', 'billAmtCalibrate', 'totalAmt', 'contractUntilAmt',
                        'commissionTotal', 'commissionSourceAmt']
    count = 0
    # 主表金额字段清洗
    for bill_column_name in bill_column_list:
        try:
            # 收入账单申请单参数接收注解已转换，在分的基础上乘!
            form_data[bill_column_name] = form_data[bill_column_name] * multiply_fen_
            # 设置成功值加1
            count = count + 1
        except (TypeError, KeyError):
            continue
    # 子表金额字段清洗
    try:
        bill_sub_form_list = form_data['billDetails']
    except (TypeError, KeyError) as e:
        return """# 收入帐单表单{} 异常,缺少子帐单! 跳过数据清洗.error={}""".format(form_no_, e)
    if not bill_sub_form_list:
        return """# 收入帐单表单{} 异常,子帐单为空! 跳过数据清洗.""".format(form_no_)
    for bill_sub_form in bill_sub_form_list:
        # 字段特殊json和数据库有差异，按Java实体来 com.upa.vo.bill.BillDetailVO
        bill_sub_column_list = ['commissionAmt', 'hisTotalAmt', 'calculateAmtCalibrate', 'calculateAmt',
                                'calculateAmtNew', 'subAmtFinal', 'calculateAmtDiff', 'totalPrice']
        for bill_sub_column_name in bill_sub_column_list:
            try:
                # 收入账单申请单参数接收注解已转换，在分的基础上乘!
                bill_sub_form[bill_sub_column_name] = bill_sub_form[bill_sub_column_name] * multiply_fen_
                # 设置成功值加1
                count = count + 1
            except (TypeError, KeyError):
                continue
        # 账单接口查询量信息表金额字段清洗
        try:
            bill_summary_form_list = bill_sub_form['billSummaryDetails']
        except (TypeError, KeyError) as e:
            log.error("""# 收入帐单表单{} 异常,缺少账单接口查询量信息! 跳过数据清洗.error={}""".format(form_no_, e))
            continue
        if bill_summary_form_list:
            for bill_summary_form in bill_summary_form_list:
                # 字段特殊json和数据库有差异，按Java实体来  com.upa.vo.bill.BillSummaryDetailVO
                bill_summary_column_list = ['amtOrg', 'amtNew', 'amtRule', 'amtRuleNew', 'amtDiff', 'price',
                                            'billProgressAmt']
                for bill_summary_column_name in bill_summary_column_list:
                    try:
                        # 收入账单申请单参数接收注解已转换，在分的基础上乘!
                        bill_summary_form[bill_summary_column_name] = bill_summary_form[
                                                                          bill_summary_column_name] * multiply_fen_
                        # 设置成功值加1
                        count = count + 1
                    except (TypeError, KeyError):
                        continue
    if count == 0:
        return "# 该表单,没有任何字段修改 formNo=[{}]".format(form_no_)
    json_data = json.dumps(form_data, ensure_ascii=False)
    return get_update_form(json_data, form_no_)


# 分润账单金额精度调整清洗
def case_bill_commission(activity_form):
    form_no_ = activity_form['form_no']
    not_empty, form_data = _get_form_data(activity_form)
    if not not_empty:
        return """# 分润账单表单{} form_data为空! 跳过数据清洗.""".format(form_no_)
    # 字段特殊json和数据库有差异，按Java实体来 com.upa.vo.bill.req.BillFormRequestVO
    bill_column_list = ['commissionTotal', 'billAmtCalibrate', 'totalAmt', 'billAmt', 'commissionSourceAmt']
    count = 0
    # 主表金额字段清洗
    for bill_column_name in bill_column_list:
        try:
            # 收入账单申请单参数接收注解已转换，在分的基础上乘!
            form_data[bill_column_name] = form_data[bill_column_name] * multiply_fen_
            # 设置成功值加1
            count = count + 1
        except (TypeError, KeyError):
            continue
    # 子表金额字段清洗
    try:
        bill_sub_form_list = form_data['billDetails']
    except (TypeError, KeyError) as e:
        return """# 分润帐单表单{} 异常,缺少子帐单! 跳过数据清洗.error={}""".format(form_no_, e)
    if not bill_sub_form_list:
        return """# 分润帐单表单{} 异常,子帐单为空! 跳过数据清洗.""".format(form_no_)
    for bill_sub_form in bill_sub_form_list:
        # 字段特殊json和数据库有差异，按Java实体来 com.upa.vo.bill.BillDetailVO
        bill_sub_column_list = ['commissionAmt', 'hisTotalAmt', 'calculateAmtCalibrate', 'calculateAmt',
                                'calculateAmtNew', 'subAmtFinal', 'calculateAmtDiff', 'totalPrice']
        for bill_sub_column_name in bill_sub_column_list:
            try:
                # 分润账单申请单参数接收注解已转换，在分的基础上乘!
                bill_sub_form[bill_sub_column_name] = bill_sub_form[bill_sub_column_name] * multiply_fen_
                # 设置成功值加1
                count = count + 1
            except (TypeError, KeyError):
                continue
        # 账单接口查询量信息表金额字段清洗
        try:
            bill_summary_form_list = bill_sub_form['billSummaryDetails']
        except (TypeError, KeyError) as e:
            log.error("""# 分润帐单表单{} 异常,缺少账单接口查询量信息! 跳过数据清洗.error={}""".format(form_no_, e))
            continue
        if bill_summary_form_list:
            for bill_summary_form in bill_summary_form_list:
                # 字段特殊json和数据库有差异，按Java实体来  com.upa.vo.bill.BillSummaryDetailVO
                bill_summary_column_list = ['amtOrg', 'amtNew', 'amtRule', 'amtRuleNew', 'amtDiff', 'price',
                                            'billProgressAmt']
                for bill_summary_column_name in bill_summary_column_list:
                    try:
                        # 收入账单申请单参数接收注解已转换，在分的基础上乘!
                        bill_summary_form[bill_summary_column_name] = bill_summary_form[
                                                                          bill_summary_column_name] * multiply_fen_
                        # 设置成功值加1
                        count = count + 1
                    except (TypeError, KeyError):
                        continue
    # 分润列表
    try:
        bill_commission_form_list = form_data['billCommissionList']
    except (TypeError, KeyError) as e:
        log.error("""# 分润帐单表单{} 异常,缺少分润列表! 跳过数据清洗.error={}""".format(form_no_, e))
        if count == 0:
            return "# 该表单,没有任何字段修改 formNo=[{}]".format(form_no_)
        json_data = json.dumps(form_data, ensure_ascii=False)
        return get_update_form(json_data, form_no_)
    if bill_commission_form_list:
        for bill_commission_form in bill_commission_form_list:
            # 字段特殊json和数据库有差异，按Java实体来 com.upa.vo.bill.req.BillProcessCommissionRequest
            bill_commission_column_list = ['commissionPoolAmt', 'commissionTotal', 'commissionAmt', 'billAmt',
                                           'billAmtCalibrate', 'subAmtFinal', 'leftAmt']
            for bill_commission_column_name in bill_commission_column_list:
                try:
                    # 分润账单申请单参数接收注解已转换，在分的基础上乘!
                    bill_commission_form[bill_commission_column_name] = bill_commission_form[
                                                                            bill_commission_column_name] * multiply_fen_
                    # 设置成功值加1
                    count = count + 1
                except (TypeError, KeyError):
                    continue
    if count == 0:
        return "# 该表单,没有任何字段修改 formNo=[{}]".format(form_no_)
    json_data = json.dumps(form_data, ensure_ascii=False)
    return get_update_form(json_data, form_no_)


# 成本账单金额精度调整清洗
def case_cost(activity_form):
    form_no_ = activity_form['form_no']
    not_empty, form_data = _get_form_data(activity_form)
    if not not_empty:
        return """# 成本账单表单{} form_data为空! 跳过数据清洗.""".format(form_no_)
    # 字段特殊json和数据库有差异，按Java实体来 com.upa.vo.bill.req.BillFormRequestVO
    cost_column_list = ['costAmt', 'costAmtCalibrated', 'amtDiff']
    count = 0
    # 主表金额字段清洗
    for cost_column_name in cost_column_list:
        try:
            # 成本账单申请单参数接收注解已转换，在分的基础上乘!
            form_data[cost_column_name] = form_data[cost_column_name] * multiply_fen_
            # 设置成功值加1
            count = count + 1
        except (TypeError, KeyError):
            continue
    # 子表金额字段清洗
    try:
        cost_sub_form_list = form_data['costSubVOList']
    except (TypeError, KeyError) as e:
        return """# 成本帐单表单{} 异常,缺少子帐单! 跳过数据清洗.error={}""".format(form_no_, e)
    if not cost_sub_form_list:
        return """# 成本帐单表单{} 异常,子帐单为空! 跳过数据清洗.""".format(form_no_)
    for cost_sub_form in cost_sub_form_list:
        # 字段特殊json和数据库有差异，按Java实体来 com.upa.vo.bill.BillDetailVO
        cost_sub_column_list = ['amtOrg', 'amtNew', 'amtRecalculate', 'amtDiff']
        for cost_sub_column_name in cost_sub_column_list:
            try:
                # 成本账单申请单参数接收注解已转换，在分的基础上乘!
                cost_sub_form[cost_sub_column_name] = cost_sub_form[cost_sub_column_name] * multiply_fen_
                # 设置成功值加1
                count = count + 1
            except (TypeError, KeyError):
                continue
        # 流程成本阶梯集合
        try:
            cost_summary_form_list = cost_sub_form['summaryDetailVOList']
        except (TypeError, KeyError) as e:
            log.error("""# 收入帐单表单{} 异常,缺少子帐单! 跳过数据清洗.error={}""".format(form_no_, e))
            continue
        if cost_summary_form_list:
            for cost_summary_form in cost_summary_form_list:
                # 字段特殊json和数据库有差异，按Java实体来  com.upa.vo.bill.BillSummaryDetailVO
                cost_summary_column_list = ['price', 'amtOrg', 'amtNew']
                for cost_summary_column_name in cost_summary_column_list:
                    try:
                        # 成本账单申请单参数接收注解已转换，在分的基础上乘!
                        cost_summary_form[cost_summary_column_name] = cost_summary_form[
                                                                          cost_summary_column_name] * multiply_fen_
                        # 设置成功值加1
                        count = count + 1
                    except (TypeError, KeyError):
                        continue
    if count == 0:
        return "# 该表单,没有任何字段修改 formNo=[{}]".format(form_no_)
    json_data = json.dumps(form_data, ensure_ascii=False)
    return get_update_form(json_data, form_no_)


def default(activity_form):
    return '# 这是异常的表单,表单类型未知,formNo = [{}], formKey=[{}]'.format(activity_form['form_no'],
                                                                              activity_form['form_key'])


# 获取formData数据
def _get_form_data(activity_form):
    try:
        form_data = json.loads(activity_form['form_data'])
    except (TypeError, KeyError):
        return False, None
    # 如果form_data为空打印提示
    if form_data is None:
        return False, None
    return True, form_data


# 打印activity_form更新语句
def get_update_form(form_data, form_no):
    return f"""UPDATE `tbs_activity_form`
SET `form_data` = '{form_data}' 
WHERE `form_no` = '{form_no}';"""


def get_update_quote_ladder(quote_ladder_rule, start_scope, end_scope):
    return f"""UPDATE `tbs_quote_ladder_rule_info` 
SET `start_scope` = '{start_scope}',
`end_scope` = '{end_scope}' 
WHERE `quote_product_rule_code` = '{quote_ladder_rule['quote_product_rule_code']}' 
AND  `idx` = {quote_ladder_rule['idx']};"""


# 查询所有表单信息
def query_form_list():
    sqlStr = """SELECT
                 	form_no,
                 	form_key,
                 	form_data 
                 FROM
                 	tbs_activity_form 
                 WHERE
                 	deleted = 0 
                 	AND form_key IN ( 'data_extract_approval_main_process_v2', 'quote_approval_main_process_v2', 'customer_invoice_process_v2', 'product_launch_process_v2', 'product_offline_process_v2', 'product_upgrades_process_v2', 'bill_approval_main_process_v2', 'bill_approval_commission_process_v2', 'cost_approval_main_process_v2' ) 
                 ORDER BY
                 	update_time DESC"""
    db = Mysql(mysql)
    form_list = db.get_data_all(sqlStr)
    db.close_mysql()
    return form_list


# 查询所有的分润报价获取其报价规则编号集合
def query_quote_sub_code_list():
    sqlStr = """SELECT
	QS.quote_code,
	QS.quote_product_rule_code 
FROM
	`tbs_final_quote` Q
	LEFT JOIN tbs_final_quote_sub QS ON Q.quote_code = QS.quote_code 
	AND QS.deleted = 0 
WHERE
	Q.deleted = 0 
	AND Q.quote_type_dict = 2"""
    db = Mysql(mysql)
    quote_sub_code_list = db.get_data_all(sqlStr)
    db.close_mysql()
    return quote_sub_code_list


# 根据报价规则编号获取报价阶梯价表信息
def query_quote_ladder_rule_list(quote_product_rule_code):
    sqlStr = f"""SELECT
	`quote_product_rule_code`,
	`rule_type`,
	`idx`,
	`start_scope`,
	`end_scope`,
	`unit_price`,
	`share_ratio` 
FROM
	`tbs_quote_ladder_rule_info` 
WHERE
	deleted = 0 
	AND quote_product_rule_code = + '{quote_product_rule_code or ''}'"""
    db = Mysql(mysql)
    quote_ladder_rule_list = db.get_data_all(sqlStr)
    db.close_mysql()
    return quote_ladder_rule_list


if __name__ == '__main__':
    print('# 清洗表金额字段:')

    table_column_map = {
        'tbs_product_price_segment_info': ['unit_price'],
        'tbs_final_segment_price': ['unit_price'],
        'tbs_his_segment_price': ['unit_price'],
        'tbs_final_quote_sub': ['basic_price', 'channel_price', 'total_price', 'unit_price', 'advance_amt',
                                'contract_amt'],
        'tbs_his_quote_sub': ['basic_price', 'channel_price', 'total_price', 'unit_price', 'advance_amt',
                              'contract_amt'],
        'tbs_quote_ladder_rule_info': ['unit_price'],
        'tbs_final_data_extract': ['unit_price', 'amt'],
        'tbs_his_data_extract': ['unit_price', 'amt'],
        'tbs_final_invoice': ['invoice_amount', 'prepaid_amount', 'prepaid_used_amount', 'prepaid_left_amount'],
        'tbs_his_invoice': ['invoice_amount', 'prepaid_amount', 'prepaid_used_amount', 'prepaid_left_amount'],
        'tbs_final_bill': ['bill_amt', 'commission_total', 'bill_amt_calibrate', 'bill_amt_commissioned', 'total_amt'],
        'tbs_his_bill': ['bill_amt', 'commission_total', 'bill_amt_calibrate', 'bill_amt_commissioned', 'total_amt'],
        'tbs_final_bill_sub': ['commission_amt', 'calculate_amt', 'calculate_amt_calibrate', 'sub_amt_final',
                               'his_total_amt'],
        'tbs_his_bill_sub': ['commission_amt', 'calculate_amt', 'calculate_amt_calibrate', 'sub_amt_final',
                             'his_total_amt'],
        'tbs_final_bill_commission_summary': ['commission_amt', 'commission_pool_amt'],
        'tbs_his_bill_commission_summary': ['commission_amt', 'commission_pool_amt'],
        'tbs_final_bill_sub_summary_details': ['price', 'amt_org', 'amt_new', 'bill_progress_amt'],
        'tbs_his_bill_sub_summary_details': ['price', 'amt_org', 'amt_new', 'bill_progress_amt', 'diff_amt'],
        'tbs_final_cost': ['cost_amt', 'cost_amt_calibrated'],
        'tbs_his_cost': ['cost_amt', 'cost_amt_calibrated'],
        'tbs_final_cost_sub': ['amt_org', 'amt_new', 'amt_recalculate'],
        'tbs_his_cost_sub': ['amt_org', 'amt_new', 'amt_recalculate'],
        'tbs_final_cost_sub_summary': ['price', 'amt_org', 'amt_new'],
        'tbs_his_cost_sub_summary': ['price', 'amt_org', 'amt_new'],
        'tbs_final_voucher_cost': ['voucher_cost_amt'],
        'tbs_final_voucher_income': ['org_amt', 'voucher_amt'],
        'tbs_daily_bill': ['bill_amt', 'pre_day_bill_amt', 'daily_amt'],
        'tbs_daily_bill_sub': ['calculate_amt', 'pre_calculate_amt', 'daily_calculate_amt'],
        'tbs_daily_bill_sub_summary': ['price', 'amt_org', 'pre_amt_org', 'daily_amt'],
        'tbs_daily_cost': ['pre_amt', 'due_amt', 'cost_amt'],
        'tbs_daily_cost_sub': ['amt_org', 'day_amt'],
        'tbs_daily_cost_sub_summary': ['price', 'amt_org']
    }
    print_cleansing_column(table_column_map)

    print('\n')
    print('\n')

    print('# 清洗表金额字段备注信息:')
    table_column_comment_remark_map = {
        'tbs_product_price_segment_info': [
            {'unit_price': '''bigint(20) DEFAULT NULL COMMENT '区间基准价格 单位:分' '''}],
        'tbs_final_segment_price': [{'unit_price': '''bigint(20) DEFAULT NULL COMMENT '区间基准价格 单位:分' '''}],
        'tbs_his_segment_price': [{'unit_price': '''bigint(20) DEFAULT NULL COMMENT '区间基准价格 单位:分' '''}],
        'tbs_final_quote_sub': [{'basic_price': '''bigint(20) DEFAULT NULL COMMENT '基准价格 单位:分' '''},
                                {'channel_price': '''bigint(20) DEFAULT NULL COMMENT '渠道原最高单价 单位:分' '''},
                                {'total_price': '''bigint(20) DEFAULT NULL COMMENT '总价' '''},
                                {'unit_price': '''bigint(20) DEFAULT NULL COMMENT '单价' '''},
                                {'advance_amt': '''bigint(20) DEFAULT NULL COMMENT '预付费' '''},
                                {'contract_amt': '''bigint(20) DEFAULT NULL COMMENT '合同金额' '''}],
        'tbs_his_quote_sub': [{'basic_price': '''bigint(20) DEFAULT NULL COMMENT '基准价格 单位:分' '''},
                              {'channel_price': '''bigint(20) DEFAULT NULL COMMENT '渠道原最高单价 单位:分' '''},
                              {'total_price': '''bigint(20) DEFAULT NULL COMMENT '总价' '''},
                              {'unit_price': '''bigint(20) DEFAULT NULL COMMENT '单价' '''},
                              {'advance_amt': '''bigint(20) DEFAULT NULL COMMENT '预付费' '''},
                              {'contract_amt': '''bigint(20) DEFAULT NULL COMMENT '合同金额' '''}],
        'tbs_quote_ladder_rule_info': [{'unit_price': '''bigint(20) DEFAULT '0' COMMENT '价格 单位:分' '''}],
        'tbs_final_data_extract': [{'unit_price': '''bigint(20) DEFAULT NULL COMMENT '单价' '''},
                                   {'amt': '''bigint(20) DEFAULT NULL COMMENT '金额 单位:分' '''}],
        'tbs_his_data_extract': [{'unit_price': '''bigint(20) DEFAULT NULL COMMENT '单价' '''},
                                 {'amt': '''bigint(20) DEFAULT NULL COMMENT '金额 单位:分' '''}],
        'tbs_final_invoice': [{'invoice_amount': '''bigint(20) NOT NULL COMMENT '开票金额 单位:分' '''},
                              {'prepaid_amount': '''bigint(20) DEFAULT NULL COMMENT '预售款总额 单位:分' '''},
                              {'prepaid_used_amount': '''bigint(20) DEFAULT NULL COMMENT '预付款使用金额' '''},
                              {'prepaid_left_amount': '''bigint(20) DEFAULT NULL COMMENT '预付款剩余金额' '''}],
        'tbs_his_invoice': [{'invoice_amount': '''bigint(20) NOT NULL COMMENT '开票金额 单位:分' '''},
                            {'prepaid_amount': '''bigint(20) DEFAULT NULL COMMENT '预售款总额 单位:分' '''},
                            {'prepaid_used_amount': '''bigint(20) DEFAULT NULL COMMENT '预付款使用金额' '''},
                            {'prepaid_left_amount': '''bigint(20) DEFAULT NULL COMMENT '预付款剩余金额' '''}],
        'tbs_final_bill': [{'bill_amt': '''bigint(20) NOT NULL COMMENT '账单总金额 单位:分' '''},
                           {'commission_total': '''bigint(20) DEFAULT '0' COMMENT '累进分润池，含本次 单位:分' '''},
                           {'bill_amt_calibrate': '''bigint(20) DEFAULT NULL COMMENT '调整后账单总金额 单位:分' '''},
                           {
                               'bill_amt_commissioned': '''bigint(20) DEFAULT NULL COMMENT '分润后的账单总金额 单位:分' '''},
                           {'total_amt': '''bigint(20) NOT NULL COMMENT '报价累计总金额（含本次） 单位:分' '''}],
        'tbs_his_bill': [{'bill_amt': '''bigint(20) NOT NULL COMMENT '账单总金额 单位:分' '''},
                         {'commission_total': '''bigint(20) DEFAULT '0' COMMENT '累进分润池，含本次 单位:分' '''},
                         {'bill_amt_calibrate': '''bigint(20) DEFAULT NULL COMMENT '调整后账单总金额 单位:分' '''},
                         {
                             'bill_amt_commissioned': '''bigint(20) DEFAULT NULL COMMENT '分润后的账单总金额 单位:分' '''},
                         {'total_amt': '''bigint(20) NOT NULL COMMENT '报价累计总金额（含本次） 单位:分' '''}],
        'tbs_final_bill_sub': [{'commission_amt': '''bigint(20) DEFAULT NULL COMMENT '分润金额' '''},
                               {'calculate_amt': '''bigint(20) NOT NULL COMMENT '子账单金额(即当前规则计算金额)' '''},
                               {
                                   'calculate_amt_calibrate': '''bigint(20) DEFAULT NULL COMMENT '调整后计算金额 单位:分' '''},
                               {'sub_amt_final': '''bigint(20) DEFAULT NULL COMMENT '最终调整金额 单位:分' '''},
                               {
                                   'his_total_amt': '''bigint(20) NOT NULL COMMENT '历史金额汇总(计费规则内，不含本次) 单位:分' '''}],
        'tbs_his_bill_sub': [{'commission_amt': '''bigint(20) DEFAULT NULL COMMENT '分润金额' '''},
                             {'calculate_amt': '''bigint(20) NOT NULL COMMENT '子账单金额(即当前规则计算金额)' '''},
                             {
                                 'calculate_amt_calibrate': '''bigint(20) DEFAULT NULL COMMENT '调整后计算金额 单位:分' '''},
                             {'sub_amt_final': '''bigint(20) DEFAULT NULL COMMENT '最终调整金额 单位:分' '''},
                             {
                                 'his_total_amt': '''bigint(20) DEFAULT NULL COMMENT '历史金额汇总(计费规则内，不含本次) 单位:分' '''}],
        'tbs_final_bill_commission_summary': [{'commission_amt': '''bigint(50) NOT NULL COMMENT '分润金额 单位:分' '''},
                                              {'commission_pool_amt': '''bigint(20) DEFAULT '0' COMMENT '累进池' '''}],
        'tbs_his_bill_commission_summary': [{'commission_amt': '''bigint(50) NOT NULL COMMENT '分润金额 单位:分' '''},
                                            {'commission_pool_amt': '''bigint(20) DEFAULT '0' COMMENT '累进池' '''}],
        'tbs_final_bill_sub_summary_details': [{'price': '''bigint(20) DEFAULT NULL COMMENT '单价 单位:分' '''},
                                               {'amt_org': '''bigint(20) DEFAULT NULL COMMENT '原金额 单位:分' '''},
                                               {'amt_new': '''bigint(20) DEFAULT NULL COMMENT '金额 单位:分' '''},
                                               {
                                                   'bill_progress_amt': '''bigint(20) DEFAULT NULL COMMENT '账单进度金额' '''}],
        'tbs_his_bill_sub_summary_details': [{'price': '''bigint(20) DEFAULT NULL COMMENT '单价 单位:分' '''},
                                             {'amt_org': '''bigint(20) DEFAULT NULL COMMENT '原金额 单位:分' '''},
                                             {'amt_new': '''bigint(20) DEFAULT NULL COMMENT '金额 单位:分' '''},
                                             {
                                                 'bill_progress_amt': '''bigint(20) DEFAULT NULL COMMENT '账单进度金额' '''},
                                             {'diff_amt': '''bigint(20) NOT NULL COMMENT '差额,单位:分' '''}],
        'tbs_final_cost': [{'cost_amt': '''bigint(50) NOT NULL COMMENT '分润金额 单位:分' '''},
                           {'cost_amt_calibrated': '''bigint(20) DEFAULT NULL COMMENT '调整后账单总金额 单位:分' '''}],
        'tbs_his_cost': [{'cost_amt': '''bigint(50) NOT NULL COMMENT '分润金额 单位:分' '''},
                         {'cost_amt_calibrated': '''bigint(20) DEFAULT NULL COMMENT '调整后账单总金额 单位:分' '''}],
        'tbs_final_cost_sub': [{'amt_org': '''bigint(20) DEFAULT NULL COMMENT '原金额 单位:分' '''},
                               {'amt_new': '''bigint(20) DEFAULT NULL COMMENT '手动调账后金额 单位:分' '''},
                               {'amt_recalculate': '''bigint(20) DEFAULT NULL COMMENT '调量后的金额 单位:分' '''}],
        'tbs_his_cost_sub': [{'amt_org': '''bigint(20) DEFAULT NULL COMMENT '原金额 单位:分' '''},
                             {'amt_new': '''bigint(20) DEFAULT NULL COMMENT '手动调账后金额 单位:分' '''},
                             {'amt_recalculate': '''bigint(20) DEFAULT NULL COMMENT '调量后的金额 单位:分' '''}],
        'tbs_final_cost_sub_summary': [{'price': '''bigint(20) DEFAULT NULL COMMENT '单价 单位:分' '''},
                                       {'amt_org': '''bigint(20) DEFAULT NULL COMMENT '原金额 单位:分' '''},
                                       {'amt_new': '''bigint(20) DEFAULT NULL COMMENT '调账后金额 单位:分' '''}],
        'tbs_his_cost_sub_summary': [{'price': '''bigint(20) DEFAULT NULL COMMENT '单价 单位:分' '''},
                                     {'amt_org': '''bigint(20) DEFAULT NULL COMMENT '原金额 单位:分' '''},
                                     {'amt_new': '''bigint(20) DEFAULT NULL COMMENT '调账后金额 单位:分' '''}],
        'tbs_final_voucher_cost': [{'voucher_cost_amt': '''bigint(20) NOT NULL COMMENT '凭证金额' '''}],
        'tbs_final_voucher_income': [{'org_amt': '''bigint(20) DEFAULT NULL COMMENT '原始金额' '''},
                                     {'voucher_amt': '''bigint(20) NOT NULL COMMENT '凭证金额' '''}],
        'tbs_daily_bill': [{'bill_amt': '''bigint(20) NOT NULL COMMENT '预估账单总金额 单位:分' '''},
                           {'pre_day_bill_amt': '''bigint(20) NOT NULL COMMENT '前一天的账单估算金额 单位:分' '''},
                           {'daily_amt': '''bigint(20) NOT NULL COMMENT '今日预估日收入 单位:分' '''}],
        'tbs_daily_bill_sub': [
            {'calculate_amt': '''bigint(20) NOT NULL COMMENT '子账单金额(即当前规则计算金额) 单位:分' '''},
            {'pre_calculate_amt': '''bigint(20) NOT NULL COMMENT '前一日子账单金额(即当前规则计算金额) 单位:分' '''},
            {
                'daily_calculate_amt': '''bigint(20) NOT NULL COMMENT '当日子账单收入金额(calculate_amt-pre_calculate_amt) 单位:分' '''}],
        'tbs_daily_bill_sub_summary': [{'price': '''bigint(20) DEFAULT NULL COMMENT '单价 单位:分' '''},
                                       {'amt_org': '''bigint(20) DEFAULT NULL COMMENT '原金额 单位:分' '''},
                                       {
                                           'pre_amt_org': '''bigint(20) DEFAULT NULL COMMENT '上次估算-原金额 单位:分' '''},
                                       {'daily_amt': '''bigint(20) DEFAULT NULL COMMENT '当日收入金额 单位:分' '''}],
        'tbs_daily_cost': [{'pre_amt': '''bigint(20) NOT NULL COMMENT '上一个成本金额账单总金额 单位:分' '''},
                           {'due_amt': '''bigint(20) NOT NULL COMMENT '截止到当前账单总金额 单位:分' '''},
                           {'cost_amt': '''bigint(20) NOT NULL COMMENT '日账单金额 单位:分' '''}],
        'tbs_daily_cost_sub': [{'amt_org': '''bigint(20) DEFAULT NULL COMMENT '截至到当日的月成本金额 单位:分' '''},
                               {'day_amt': '''bigint(20) DEFAULT NULL COMMENT '当日产生的成本金额 单位:分' '''}],
        'tbs_daily_cost_sub_summary': [{'price': '''bigint(20) DEFAULT NULL COMMENT '单价 单位:分' '''},
                                       {'amt_org': '''bigint(20) DEFAULT NULL COMMENT '原金额 单位:分' '''}]
    }
    print_cleansing_column_comment_remark(table_column_comment_remark_map)

    print('\n')
    print('\n')

    print('# activityFormData清洗')
    print_activity_form_data()

    print('\n')
    print('\n')

    print('# 特殊处理:分润报价阶梯为金额')
    print_quote_ladder_rule_column()

    # 测试数据库字段转驼峰
    print(to_camel_case('str_char_test'))
