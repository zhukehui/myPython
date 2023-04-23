import json
import logging

import requests

from utils.LoggerUtil import LogUtil


class httpUtils:
    logger = LogUtil(log_level=logging.DEBUG).getLogger()

    def get(self, url, body={}, headers={}):
        res = requests.get(url, data=body, headers=headers)
        self.request(res)
        return res

    def post(self, url, body={}, headers={}):
        res = requests.post(url, data=json.dumps(body), headers=headers)
        self.request(res)
        return res

    def request(self, res):
        self.logger.info("请求路径：" + res.request.url)
        headerStr = ""
        for headerKey in res.request.headers:
            headerStr = headerStr + "\n" + headerKey + ":" + res.request.headers[headerKey]
        self.logger.info("请求头信息：" + headerStr)
        self.logger.info("请求参数：\n" + (res.request.body or ''))
        resHeaderStr = ""
        for resHeaderKey in res.headers:
            resHeaderStr = resHeaderStr + "\n" + resHeaderKey + ":" + res.headers[resHeaderKey]
        self.logger.info("响应头信息：" + resHeaderStr)
        self.logger.info("返回结果：\n" + res.content.decode("utf-8"))
        if not res.ok:
            raise RuntimeError("调用外部系统异常!")
        response = res.json()
        response_code = response["code"]
        if response_code != 200:
            raise RuntimeError("调用外部系统异常!errorMessage=[%s]" % response["errorMessage"])
