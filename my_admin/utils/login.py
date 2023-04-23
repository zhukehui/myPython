import logging

from utils.LoggerUtil import LogUtil
from utils.httpUtil import httpUtils
from utils.rsa_util import rsa_encode

log = LogUtil(log_level=logging.DEBUG).getLogger()

# import ssl

# ssl._create_default_https_context = ssl._create_stdlib_context

# 根据 taskAssignee 进行加密返回 token,taskAssignee 为入参
def get_token(url, user_name, password):
    pub_key = """-----BEGIN PUBLIC KEY-----
    MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAoWMNeiuxQTXaaCOFbBgN18AftmVLOndrzavzf4f9tRb4siOEVgze1AATyiJx65LaPh8zWSX2CrkXRC4+TM82M6BeTXdrZXabzEKde2SvnW8qjGmug0RiwQCLiM5AlNN9zbK/rahFucKFgsxdzoCSwEoXRBuNwtMGO/a5fDFMA3LF1g0IuZVzJdhXewf/94cbHd50SJ5XU7iRA5lRF8z9CZJPmZmQcUzfuHpDDIz5DSqsSdSLqusaMkliIeFRv9OE700Xfj1RfP01x3ZK6Jyn8+pxSH+CjTV+7vwm1WB/9d1lblrwjVpDQFoK++D3oDoWV/NwnKyT3iDVj5K9SMDmAQIDAQAB
    -----END PUBLIC KEY-----"""
    username = rsa_encode(user_name, pub_key)
    password = rsa_encode(password, pub_key)
    post_body = {
        "username": username,
        "password": password,
        "verificationCode": "1",
        "verificationCodeKey": "",
    }
    headers = {"Content-Type": "application/json;charset=UTF-8"}
    resp = httpUtils().post(url=url, body=post_body, headers=headers)
    # user_token = json.loads(resp.text)["data"]["token"]

    response = resp.json()
    user_token = response["data"]["token"]
    log.critical("登录成功，token={%s}" % user_token)
    return user_token


if __name__ == '__main__':
    token = get_token("http://localhost:8086/api/auth/login", "shouzhen.qu", "upa.123")
    print(token)
