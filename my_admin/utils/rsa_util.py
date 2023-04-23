import base64

from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_v1_5 as Cipher_pkcs1_v1_5
# from Cryptodome.Cipher import PKCS1_v1_5 as Cipher_pkcs1_v1_5
# from Cryptodome.PublicKey import RSA


def rsa_encode(text, public_key):
    key = RSA.importKey(public_key)
    cipher = Cipher_pkcs1_v1_5.new(key)  # 创建用于执行pkcs1_v1_5加密或解密的密码
    cipher_text = base64.b64encode(cipher.encrypt(text.encode('utf-8')))
    return cipher_text.decode('utf-8')


if __name__ == '__main__':
    key = """-----BEGIN PUBLIC KEY-----
    MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAoWMNeiuxQTXaaCOFbBgN18AftmVLOndrzavzf4f9tRb4siOEVgze1AATyiJx65LaPh8zWSX2CrkXRC4+TM82M6BeTXdrZXabzEKde2SvnW8qjGmug0RiwQCLiM5AlNN9zbK/rahFucKFgsxdzoCSwEoXRBuNwtMGO/a5fDFMA3LF1g0IuZVzJdhXewf/94cbHd50SJ5XU7iRA5lRF8z9CZJPmZmQcUzfuHpDDIz5DSqsSdSLqusaMkliIeFRv9OE700Xfj1RfP01x3ZK6Jyn8+pxSH+CjTV+7vwm1WB/9d1lblrwjVpDQFoK++D3oDoWV/NwnKyT3iDVj5K9SMDmAQIDAQAB
    -----END PUBLIC KEY-----"""
    print(rsa_encode("shouzhen.qu", key))
