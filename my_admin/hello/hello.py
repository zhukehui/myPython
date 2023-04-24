# 登录
from flask import Blueprint

hello_blue = Blueprint('hello', __name__)


@hello_blue.route('/', methods=['GET'])
def hello():
    return 'exist'
