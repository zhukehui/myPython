from rest_framework.response import Response


class APIResponse(Response):
    def __init__(self, data_status=200, data_msg=None, results=None, http_status=None, headers=None, exception=False,
                 **kwargs):
        '''
        :param data_status: 状态码
        :param msg: 提示信息
        :param results: 附加信息,如序列化得到的数据
        :param headers:
        :param status: HTTP状态码
        :param kwargs: 其他信息
        '''
        # data的初始状态：状态码与状态信息
        data = {
            'status': data_status,
            'msg': data_msg,
        }
        # data的响应数据体
        # results可能是False、0等数据，这些数据某些情况下也会作为合法数据返回
        if results is not None:
            data['results'] = results
        # data响应的其他内容
        # if kwargs is not None:
        #     for k, v in kwargs.items():
        #         setattr(data, k, v)
        data.update(kwargs)

        super().__init__(data=data, status=http_status, headers=headers, exception=exception)  # 重写父类Response的__init__方法

# 使用：
# APIResponse() 代表就返回 {"status": 200, "msg": "ok"}

# APIResponse(result="结果") 代表返回 {"status": 200, "msg": "ok", "result": "结果"}

# APIResponse(status=1, msg='error', http_status=400, exception=True) 异常返回 {"status": 1, "msg": "error"}