from flask import Flask
from flask_cors import CORS

from calculation.calculation import query_calculation_blue, contract_blue
from process.process import login_blue, query_form_all_blue, query_process_node_by_form_no_blue, approval_blue, \
    one_key_approval_blue, view_process_img_blue, query_flow_chart_by_form_no_blue

app = Flask(__name__)
CORS(app, supports_credentials=True, resources={r"/*": {"origins": "*"}})  # 试解决跨域问题

# 登录
app.register_blueprint(blueprint=login_blue)

# 查询历史电费信息列表
app.register_blueprint(blueprint=query_calculation_blue)

# 计算电费
app.register_blueprint(blueprint=contract_blue)

# 根据formNo获取表单信息集合
app.register_blueprint(blueprint=query_form_all_blue)

# 根据formNo获取表单当前节点
app.register_blueprint(blueprint=query_process_node_by_form_no_blue)

# 单节点审批
app.register_blueprint(blueprint=approval_blue)

# 一键审批
app.register_blueprint(blueprint=one_key_approval_blue)

# 查看流程图
app.register_blueprint(blueprint=view_process_img_blue)

# 根据formNo获取表单发起流程图，修改
app.register_blueprint(blueprint=query_flow_chart_by_form_no_blue)

app.run(debug=True,port=6688)
app.config['JSON_AS_ASCII'] = False
