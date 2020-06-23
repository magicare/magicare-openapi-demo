# -*- coding: utf-8 -*-

import hmac
import hashlib
import base64
import uuid
import datetime

# 测试环境固定参数
strAppid = "yDRMOnjqx9mqZVjC"
strAppSecret = "qm1e5kInsLjJnVu8HW8tTdGlaWxVs3Aj"

strTestMode = "GET"
strPath = "/v1/echo?str=hello"

# 其他header参数
host = "open-api.haoyong.me"

strContent_Type = "application/json;charset=utf-8"

# 必须在 15 分钟以内使用
strDate = datetime.datetime.utcnow().strftime('%a, %d %b %Y %H:%M:%S GMT')

strX_signature_method = "HMAC-SHA1"

namespace = uuid.NAMESPACE_URL
strX_signature_nonce = uuid.uuid1()

strX_signature_version = "1.0"

Signature = """%(test_mode)s
%(date)s
%(hosts)s
%(signature_method)s
%(signature_nonce)s
%(signature_version)s
%(path)s"""
Signature = Signature % dict(test_mode=strTestMode, date=strDate, hosts=host,
                             signature_method=strX_signature_method, signature_nonce=strX_signature_nonce, signature_version=strX_signature_version, path=strPath)
# 生成签名认证(strAppid:strSignature)
digest = hmac.new(strAppSecret.encode(
    'utf-8'), msg=Signature.encode('utf-8'), digestmod=hashlib.sha1).digest()
strSignature = base64.b64encode(bytes(digest)).decode('utf-8')
strAuthorization = strAppid + ":" + strSignature

# 生成 curl
testCurlStr = '''
curl "http://{host}{path}" \\
  -X GET \\
  -H "Host: {host}" \\
  -H "Authorization: {authorization}" \\
  -H "Date: {date}" \\
  -H "x-signature-method: {signMethod}" \\
  -H "x-signature-nonce: {signNonce}" \\
  -H "x-signature-version: {signVersion}" \\
  --compressed \\
  --insecure
'''.format(path=strPath, host=host, authorization=strAuthorization, date=strDate, signMethod=strX_signature_method, signNonce=strX_signature_nonce, signVersion=strX_signature_version)

print("\ncopy and execute the `curl` command below to test in your terminal...")
print(testCurlStr)
