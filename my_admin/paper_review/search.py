import requests
from docx.api import Document
from flask import json
import os
from tencentcloud.common import credential
from tencentcloud.common.profile.client_profile import ClientProfile
from tencentcloud.common.profile.http_profile import HttpProfile
from tencentcloud.common.exception.tencent_cloud_sdk_exception import TencentCloudSDKException
from tencentcloud.sts.v20180813 import sts_client, models

local_path = "../thesis"


def check_similar(text):
    # 使用API接口进行文献检索与查重
    url = 'https://api.bstester.com/api/v1/mmc_graduate_check'
    headers = {'Content-Type': 'application/json'}
    data = {'raw_text': text}

    try:
        response = requests.post(url, headers=headers, json=data)
        result = response.json()
        if result['result_type'] == 'plagiarism':
            print(result)
            return True, result['copy_percent']
        else:
            return False, 0
    except:
        print("论文对比失败")
        return False, 0


def check_similar_to(text):
    # 使用API接口进行文献检索与查重
    try:
        # 实例化一个认证对象，入参需要传入腾讯云账户的secretId和secretKey，为了保护密钥安全，建议结合方案一，将密钥设置在环境变量中
        cred = credential.Credential(
            "AKID4MkDoQyMXVWP4f9XqxuplZN0RdmqwlEY",
            "ITglcKzcEhCZmnheP8lGZfXE1bzBC1dA")
        httpProfile = HttpProfile()
        httpProfile.endpoint = "sts.tencentcloudapi.com"
        clientProfile = ClientProfile()
        clientProfile.httpProfile = httpProfile
        client = sts_client.StsClient(cred, "", clientProfile)
        req = models.GetFederationTokenRequest()
        params = {
            "SentencePairList": [
                {
                    "SourceText": None,
                    "TargetText": None
                }
            ]
        }
        req.from_json_string(json.dumps(params))
        resp = client.GetFederationToken(req)
        print(resp.to_json_string())
    except TencentCloudSDKException as err:
        print(err)


# 获取文件夹内所有文件
def read_files(path):
    """
    遍历指定目录下的所有文件，读取文件内容
    """
    file_map = {}

    # 遍历指定路径下的所有文件和子目录
    for root, dirs, files in os.walk(path):
        for file_name in files:
            # 获取文件的绝对路径
            file_path = os.path.join(root, file_name)
            doc = Document(file_path)
            content = ""
            for para in doc.paragraphs:
                # with open(file_path, "r", encoding='utf-8') as f:
                # 读取文件内容
                content += para.text
            file_map[file_name] = content
    return file_map


# 示例使用
if __name__ == '__main__':
    for key, value in read_files(local_path).items():
        is_similar, sim_percent = check_similar_to(value)

        if is_similar:
            print(key + "与网络上已有的论文重复，重复率为{}%".format(sim_percent * 100))
        else:
            print(key + "未检测到与网络上已有的论文重复")
