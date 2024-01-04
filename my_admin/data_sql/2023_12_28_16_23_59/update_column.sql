UPDATE tbs_product_price_segment_info 
 SET unit_price = unit_price * 100;
UPDATE tbs_final_segment_price 
 SET unit_price = unit_price * 100;
UPDATE tbs_his_segment_price 
 SET unit_price = unit_price * 100;
UPDATE tbs_final_quote_sub 
 SET basic_price = basic_price * 100, 
channel_price = channel_price * 100, 
total_price = total_price * 100, 
unit_price = unit_price * 100, 
advance_amt = advance_amt * 100, 
contract_amt = contract_amt * 100;
UPDATE tbs_his_quote_sub 
 SET basic_price = basic_price * 100, 
channel_price = channel_price * 100, 
total_price = total_price * 100, 
unit_price = unit_price * 100, 
advance_amt = advance_amt * 100, 
contract_amt = contract_amt * 100;
UPDATE tbs_quote_ladder_rule_info 
 SET unit_price = unit_price * 100;
UPDATE tbs_final_data_extract 
 SET unit_price = unit_price * 100, 
amt = amt * 100;
UPDATE tbs_his_data_extract 
 SET unit_price = unit_price * 100, 
amt = amt * 100;
UPDATE tbs_final_invoice 
 SET invoice_amount = invoice_amount * 100, 
prepaid_amount = prepaid_amount * 100, 
prepaid_used_amount = prepaid_used_amount * 100, 
prepaid_left_amount = prepaid_left_amount * 100;
UPDATE tbs_his_invoice 
 SET invoice_amount = invoice_amount * 100, 
prepaid_amount = prepaid_amount * 100, 
prepaid_used_amount = prepaid_used_amount * 100, 
prepaid_left_amount = prepaid_left_amount * 100;
UPDATE tbs_final_bill 
 SET bill_amt = bill_amt * 100, 
commission_total = commission_total * 100, 
bill_amt_calibrate = bill_amt_calibrate * 100, 
bill_amt_commissioned = bill_amt_commissioned * 100, 
total_amt = total_amt * 100;
UPDATE tbs_his_bill 
 SET bill_amt = bill_amt * 100, 
commission_total = commission_total * 100, 
bill_amt_calibrate = bill_amt_calibrate * 100, 
bill_amt_commissioned = bill_amt_commissioned * 100, 
total_amt = total_amt * 100;
UPDATE tbs_final_bill_sub 
 SET commission_amt = commission_amt * 100, 
calculate_amt = calculate_amt * 100, 
calculate_amt_calibrate = calculate_amt_calibrate * 100, 
sub_amt_final = sub_amt_final * 100, 
his_total_amt = his_total_amt * 100;
UPDATE tbs_his_bill_sub 
 SET commission_amt = commission_amt * 100, 
calculate_amt = calculate_amt * 100, 
calculate_amt_calibrate = calculate_amt_calibrate * 100, 
sub_amt_final = sub_amt_final * 100, 
his_total_amt = his_total_amt * 100;
UPDATE tbs_final_bill_commission_summary 
 SET commission_amt = commission_amt * 100, 
commission_pool_amt = commission_pool_amt * 100;
UPDATE tbs_his_bill_commission_summary 
 SET commission_amt = commission_amt * 100, 
commission_pool_amt = commission_pool_amt * 100;
UPDATE tbs_final_bill_sub_summary_details 
 SET price = price * 100, 
amt_org = amt_org * 100, 
amt_new = amt_new * 100, 
bill_progress_amt = bill_progress_amt * 100;
UPDATE tbs_his_bill_sub_summary_details 
 SET price = price * 100, 
amt_org = amt_org * 100, 
amt_new = amt_new * 100, 
bill_progress_amt = bill_progress_amt * 100, 
diff_amt = diff_amt * 100;
UPDATE tbs_final_cost 
 SET cost_amt = cost_amt * 100, 
cost_amt_calibrated = cost_amt_calibrated * 100;
UPDATE tbs_his_cost 
 SET cost_amt = cost_amt * 100, 
cost_amt_calibrated = cost_amt_calibrated * 100;
UPDATE tbs_final_cost_sub 
 SET amt_org = amt_org * 100, 
amt_new = amt_new * 100, 
amt_recalculate = amt_recalculate * 100;
UPDATE tbs_his_cost_sub 
 SET amt_org = amt_org * 100, 
amt_new = amt_new * 100, 
amt_recalculate = amt_recalculate * 100;
UPDATE tbs_final_cost_sub_summary 
 SET price = price * 100, 
amt_org = amt_org * 100, 
amt_new = amt_new * 100;
UPDATE tbs_his_cost_sub_summary 
 SET price = price * 100, 
amt_org = amt_org * 100, 
amt_new = amt_new * 100;
UPDATE tbs_final_voucher_cost 
 SET voucher_cost_amt = voucher_cost_amt * 100;
UPDATE tbs_final_voucher_income 
 SET org_amt = org_amt * 100, 
voucher_amt = voucher_amt * 100;
UPDATE tbs_daily_bill 
 SET bill_amt = bill_amt * 100, 
pre_day_bill_amt = pre_day_bill_amt * 100, 
daily_amt = daily_amt * 100;
UPDATE tbs_daily_bill_sub 
 SET calculate_amt = calculate_amt * 100, 
pre_calculate_amt = pre_calculate_amt * 100, 
daily_calculate_amt = daily_calculate_amt * 100;
UPDATE tbs_daily_bill_sub_summary 
 SET price = price * 100, 
amt_org = amt_org * 100, 
pre_amt_org = pre_amt_org * 100, 
daily_amt = daily_amt * 100;
UPDATE tbs_daily_cost 
 SET pre_amt = pre_amt * 100, 
due_amt = due_amt * 100, 
cost_amt = cost_amt * 100;
UPDATE tbs_daily_cost_sub 
 SET amt_org = amt_org * 100, 
day_amt = day_amt * 100;
UPDATE tbs_daily_cost_sub_summary 
 SET price = price * 100, 
amt_org = amt_org * 100;
