ALTER TABLE `tbs_product_price_segment_info` 
MODIFY COLUMN `unit_price` bigint(20) DEFAULT NULL COMMENT '区间基准价格 单位:毫（小数点后4位）' ; 
ALTER TABLE `tbs_final_segment_price` 
MODIFY COLUMN `unit_price` bigint(20) DEFAULT NULL COMMENT '区间基准价格 单位:毫（小数点后4位）' ; 
ALTER TABLE `tbs_his_segment_price` 
MODIFY COLUMN `unit_price` bigint(20) DEFAULT NULL COMMENT '区间基准价格 单位:毫（小数点后4位）' ; 
ALTER TABLE `tbs_final_quote_sub` 
MODIFY COLUMN `basic_price` bigint(20) DEFAULT NULL COMMENT '基准价格 单位:毫（小数点后4位）' , 
MODIFY COLUMN `channel_price` bigint(20) DEFAULT NULL COMMENT '渠道原最高单价 单位:毫（小数点后4位）' , 
MODIFY COLUMN `total_price` bigint(20) DEFAULT NULL COMMENT '总价 单位:毫（小数点后4位）' , 
MODIFY COLUMN `unit_price` bigint(20) DEFAULT NULL COMMENT '单价 单位:毫（小数点后4位）' , 
MODIFY COLUMN `advance_amt` bigint(20) DEFAULT NULL COMMENT '预付费 单位:毫（小数点后4位）' , 
MODIFY COLUMN `contract_amt` bigint(20) DEFAULT NULL COMMENT '合同金额 单位:毫（小数点后4位）' ; 
ALTER TABLE `tbs_his_quote_sub` 
MODIFY COLUMN `basic_price` bigint(20) DEFAULT NULL COMMENT '基准价格 单位:毫（小数点后4位）' , 
MODIFY COLUMN `channel_price` bigint(20) DEFAULT NULL COMMENT '渠道原最高单价 单位:毫（小数点后4位）' , 
MODIFY COLUMN `total_price` bigint(20) DEFAULT NULL COMMENT '总价 单位:毫（小数点后4位）' , 
MODIFY COLUMN `unit_price` bigint(20) DEFAULT NULL COMMENT '单价 单位:毫（小数点后4位）' , 
MODIFY COLUMN `advance_amt` bigint(20) DEFAULT NULL COMMENT '预付费 单位:毫（小数点后4位）' , 
MODIFY COLUMN `contract_amt` bigint(20) DEFAULT NULL COMMENT '合同金额 单位:毫（小数点后4位）' ; 
ALTER TABLE `tbs_quote_ladder_rule_info` 
MODIFY COLUMN `unit_price` bigint(20) DEFAULT '0' COMMENT '价格 单位:毫（小数点后4位）' ; 
ALTER TABLE `tbs_final_data_extract` 
MODIFY COLUMN `unit_price` bigint(20) DEFAULT NULL COMMENT '单价 单位:毫（小数点后4位）' , 
MODIFY COLUMN `amt` bigint(20) DEFAULT NULL COMMENT '金额 单位:毫（小数点后4位）' ; 
ALTER TABLE `tbs_his_data_extract` 
MODIFY COLUMN `unit_price` bigint(20) DEFAULT NULL COMMENT '单价 单位:毫（小数点后4位）' , 
MODIFY COLUMN `amt` bigint(20) DEFAULT NULL COMMENT '金额 单位:毫（小数点后4位）' ; 
ALTER TABLE `tbs_final_invoice` 
MODIFY COLUMN `invoice_amount` bigint(20) NOT NULL COMMENT '开票金额 单位:毫（小数点后4位）' , 
MODIFY COLUMN `prepaid_amount` bigint(20) DEFAULT NULL COMMENT '预售款总额 单位:毫（小数点后4位）' , 
MODIFY COLUMN `prepaid_used_amount` bigint(20) DEFAULT NULL COMMENT '预付款使用金额 单位:毫（小数点后4位）' , 
MODIFY COLUMN `prepaid_left_amount` bigint(20) DEFAULT NULL COMMENT '预付款剩余金额 单位:毫（小数点后4位）' ; 
ALTER TABLE `tbs_his_invoice` 
MODIFY COLUMN `invoice_amount` bigint(20) NOT NULL COMMENT '开票金额 单位:毫（小数点后4位）' , 
MODIFY COLUMN `prepaid_amount` bigint(20) DEFAULT NULL COMMENT '预售款总额 单位:毫（小数点后4位）' , 
MODIFY COLUMN `prepaid_used_amount` bigint(20) DEFAULT NULL COMMENT '预付款使用金额 单位:毫（小数点后4位）' , 
MODIFY COLUMN `prepaid_left_amount` bigint(20) DEFAULT NULL COMMENT '预付款剩余金额 单位:毫（小数点后4位）' ; 
ALTER TABLE `tbs_final_bill` 
MODIFY COLUMN `bill_amt` bigint(20) NOT NULL COMMENT '账单总金额 单位:毫（小数点后4位）' , 
MODIFY COLUMN `commission_total` bigint(20) DEFAULT '0' COMMENT '累进分润池，含本次 单位:毫（小数点后4位）' , 
MODIFY COLUMN `bill_amt_calibrate` bigint(20) DEFAULT NULL COMMENT '调整后账单总金额 单位:毫（小数点后4位）' , 
MODIFY COLUMN `bill_amt_commissioned` bigint(20) DEFAULT NULL COMMENT '分润后的账单总金额 单位:毫（小数点后4位）' , 
MODIFY COLUMN `total_amt` bigint(20) NOT NULL COMMENT '报价累计总金额（含本次） 单位:毫（小数点后4位）' ; 
ALTER TABLE `tbs_his_bill` 
MODIFY COLUMN `bill_amt` bigint(20) NOT NULL COMMENT '账单总金额 单位:毫（小数点后4位）' , 
MODIFY COLUMN `commission_total` bigint(20) DEFAULT '0' COMMENT '累进分润池，含本次 单位:毫（小数点后4位）' , 
MODIFY COLUMN `bill_amt_calibrate` bigint(20) DEFAULT NULL COMMENT '调整后账单总金额 单位:毫（小数点后4位）' , 
MODIFY COLUMN `bill_amt_commissioned` bigint(20) DEFAULT NULL COMMENT '分润后的账单总金额 单位:毫（小数点后4位）' , 
MODIFY COLUMN `total_amt` bigint(20) NOT NULL COMMENT '报价累计总金额（含本次） 单位:毫（小数点后4位）' ; 
ALTER TABLE `tbs_final_bill_sub` 
MODIFY COLUMN `commission_amt` bigint(20) DEFAULT NULL COMMENT '分润金额' , 
MODIFY COLUMN `calculate_amt` bigint(20) NOT NULL COMMENT '子账单金额(即当前规则计算金额) 单位:毫（小数点后4位）' , 
MODIFY COLUMN `calculate_amt_calibrate` bigint(20) DEFAULT NULL COMMENT '调整后计算金额 单位:毫（小数点后4位）' , 
MODIFY COLUMN `sub_amt_final` bigint(20) DEFAULT NULL COMMENT '最终调整金额 单位:毫（小数点后4位）' , 
MODIFY COLUMN `his_total_amt` bigint(20) NOT NULL COMMENT '历史金额汇总(计费规则内，不含本次) 单位:毫（小数点后4位）' ; 
ALTER TABLE `tbs_his_bill_sub` 
MODIFY COLUMN `commission_amt` bigint(20) DEFAULT NULL COMMENT '分润金额' , 
MODIFY COLUMN `calculate_amt` bigint(20) NOT NULL COMMENT '子账单金额(即当前规则计算金额) 单位:毫（小数点后4位）' , 
MODIFY COLUMN `calculate_amt_calibrate` bigint(20) DEFAULT NULL COMMENT '调整后计算金额 单位:毫（小数点后4位）' , 
MODIFY COLUMN `sub_amt_final` bigint(20) DEFAULT NULL COMMENT '最终调整金额 单位:毫（小数点后4位）' , 
MODIFY COLUMN `his_total_amt` bigint(20) DEFAULT NULL COMMENT '历史金额汇总(计费规则内，不含本次) 单位:毫（小数点后4位）' ; 
ALTER TABLE `tbs_final_bill_commission_summary` 
MODIFY COLUMN `commission_amt` bigint(50) NOT NULL COMMENT '分润金额 单位:毫（小数点后4位）' , 
MODIFY COLUMN `commission_pool_amt` bigint(20) DEFAULT '0' COMMENT '累进池 单位:毫（小数点后4位）' ; 
ALTER TABLE `tbs_his_bill_commission_summary` 
MODIFY COLUMN `commission_amt` bigint(50) NOT NULL COMMENT '分润金额 单位:毫（小数点后4位）' , 
MODIFY COLUMN `commission_pool_amt` bigint(20) DEFAULT '0' COMMENT '累进池 单位:毫（小数点后4位）' ; 
ALTER TABLE `tbs_final_bill_sub_summary_details` 
MODIFY COLUMN `price` bigint(20) DEFAULT NULL COMMENT '单价 单位:毫（小数点后4位）' , 
MODIFY COLUMN `amt_org` bigint(20) DEFAULT NULL COMMENT '原金额 单位:毫（小数点后4位）' , 
MODIFY COLUMN `amt_new` bigint(20) DEFAULT NULL COMMENT '金额 单位:毫（小数点后4位）' , 
MODIFY COLUMN `bill_progress_amt` bigint(20) DEFAULT NULL COMMENT '账单进度金额 单位:毫（小数点后4位）' ; 
ALTER TABLE `tbs_his_bill_sub_summary_details` 
MODIFY COLUMN `price` bigint(20) DEFAULT NULL COMMENT '单价 单位:毫（小数点后4位）' , 
MODIFY COLUMN `amt_org` bigint(20) DEFAULT NULL COMMENT '原金额 单位:毫（小数点后4位）' , 
MODIFY COLUMN `amt_new` bigint(20) DEFAULT NULL COMMENT '金额 单位:毫（小数点后4位）' , 
MODIFY COLUMN `bill_progress_amt` bigint(20) DEFAULT NULL COMMENT '账单进度金额 单位:毫（小数点后4位）' , 
MODIFY COLUMN `diff_amt` bigint(20) NOT NULL COMMENT '差额,单位:毫（小数点后4位）' ; 
ALTER TABLE `tbs_final_cost` 
MODIFY COLUMN `cost_amt` bigint(50) NOT NULL COMMENT '分润金额 单位:毫（小数点后4位）' , 
MODIFY COLUMN `cost_amt_calibrated` bigint(20) DEFAULT NULL COMMENT '调整后账单总金额 单位:毫（小数点后4位）' ; 
ALTER TABLE `tbs_his_cost` 
MODIFY COLUMN `cost_amt` bigint(50) NOT NULL COMMENT '分润金额 单位:毫（小数点后4位）' , 
MODIFY COLUMN `cost_amt_calibrated` bigint(20) DEFAULT NULL COMMENT '调整后账单总金额 单位:毫（小数点后4位）' ; 
ALTER TABLE `tbs_final_cost_sub` 
MODIFY COLUMN `amt_org` bigint(20) DEFAULT NULL COMMENT '原金额 单位:毫（小数点后4位）' , 
MODIFY COLUMN `amt_new` bigint(20) DEFAULT NULL COMMENT '手动调账后金额 单位:毫（小数点后4位）' , 
MODIFY COLUMN `amt_recalculate` bigint(20) DEFAULT NULL COMMENT '调量后的金额 单位:毫（小数点后4位）' ; 
ALTER TABLE `tbs_his_cost_sub` 
MODIFY COLUMN `amt_org` bigint(20) DEFAULT NULL COMMENT '原金额 单位:毫（小数点后4位）' , 
MODIFY COLUMN `amt_new` bigint(20) DEFAULT NULL COMMENT '手动调账后金额 单位:毫（小数点后4位）' , 
MODIFY COLUMN `amt_recalculate` bigint(20) DEFAULT NULL COMMENT '调量后的金额 单位:毫（小数点后4位）' ; 
ALTER TABLE `tbs_final_cost_sub_summary` 
MODIFY COLUMN `price` bigint(20) DEFAULT NULL COMMENT '单价 单位:毫（小数点后4位）' , 
MODIFY COLUMN `amt_org` bigint(20) DEFAULT NULL COMMENT '原金额 单位:毫（小数点后4位）' , 
MODIFY COLUMN `amt_new` bigint(20) DEFAULT NULL COMMENT '调账后金额 单位:毫（小数点后4位）' ; 
ALTER TABLE `tbs_his_cost_sub_summary` 
MODIFY COLUMN `price` bigint(20) DEFAULT NULL COMMENT '单价 单位:毫（小数点后4位）' , 
MODIFY COLUMN `amt_org` bigint(20) DEFAULT NULL COMMENT '原金额 单位:毫（小数点后4位）' , 
MODIFY COLUMN `amt_new` bigint(20) DEFAULT NULL COMMENT '调账后金额 单位:毫（小数点后4位）' ; 
ALTER TABLE `tbs_final_voucher_cost` 
MODIFY COLUMN `voucher_cost_amt` bigint(20) NOT NULL COMMENT '凭证金额 单位:毫（小数点后4位）' ; 
ALTER TABLE `tbs_final_voucher_income` 
MODIFY COLUMN `org_amt` bigint(20) DEFAULT NULL COMMENT '原始金额 单位:毫（小数点后4位）' , 
MODIFY COLUMN `voucher_amt` bigint(20) NOT NULL COMMENT '凭证金额 单位:毫（小数点后4位）' ; 
ALTER TABLE `tbs_daily_bill` 
MODIFY COLUMN `bill_amt` bigint(20) NOT NULL COMMENT '预估账单总金额 单位:毫（小数点后4位）' , 
MODIFY COLUMN `pre_day_bill_amt` bigint(20) NOT NULL COMMENT '前一天的账单估算金额 单位:毫（小数点后4位）' , 
MODIFY COLUMN `daily_amt` bigint(20) NOT NULL COMMENT '今日预估日收入 单位:毫（小数点后4位）' ; 
ALTER TABLE `tbs_daily_bill_sub` 
MODIFY COLUMN `calculate_amt` bigint(20) NOT NULL COMMENT '子账单金额(即当前规则计算金额) 单位:毫（小数点后4位）' , 
MODIFY COLUMN `pre_calculate_amt` bigint(20) NOT NULL COMMENT '前一日子账单金额(即当前规则计算金额) 单位:毫（小数点后4位）' , 
MODIFY COLUMN `daily_calculate_amt` bigint(20) NOT NULL COMMENT '当日子账单收入金额(calculate_amt-pre_calculate_amt) 单位:毫（小数点后4位）' ; 
ALTER TABLE `tbs_daily_bill_sub_summary` 
MODIFY COLUMN `price` bigint(20) DEFAULT NULL COMMENT '单价 单位:毫（小数点后4位）' , 
MODIFY COLUMN `amt_org` bigint(20) DEFAULT NULL COMMENT '原金额 单位:毫（小数点后4位）' , 
MODIFY COLUMN `pre_amt_org` bigint(20) DEFAULT NULL COMMENT '上次估算-原金额 单位:毫（小数点后4位）' , 
MODIFY COLUMN `daily_amt` bigint(20) DEFAULT NULL COMMENT '当日收入金额 单位:毫（小数点后4位）' ; 
ALTER TABLE `tbs_daily_cost` 
MODIFY COLUMN `pre_amt` bigint(20) NOT NULL COMMENT '上一个成本金额账单总金额 单位:毫（小数点后4位）' , 
MODIFY COLUMN `due_amt` bigint(20) NOT NULL COMMENT '截止到当前账单总金额 单位:毫（小数点后4位）' , 
MODIFY COLUMN `cost_amt` bigint(20) NOT NULL COMMENT '日账单金额 单位:毫（小数点后4位）' ; 
ALTER TABLE `tbs_daily_cost_sub` 
MODIFY COLUMN `amt_org` bigint(20) DEFAULT NULL COMMENT '截至到当日的月成本金额 单位:毫（小数点后4位）' , 
MODIFY COLUMN `day_amt` bigint(20) DEFAULT NULL COMMENT '当日产生的成本金额 单位:毫（小数点后4位）' ; 
ALTER TABLE `tbs_daily_cost_sub_summary` 
MODIFY COLUMN `price` bigint(20) DEFAULT NULL COMMENT '单价 单位:毫（小数点后4位）' , 
MODIFY COLUMN `amt_org` bigint(20) DEFAULT NULL COMMENT '原金额 单位:毫（小数点后4位）' ; 
