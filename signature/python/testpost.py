# -*- coding: utf-8 -*-

import hmac
import hashlib
import base64
import uuid
import datetime

# 测试环境固定参数
strAppid = "yDRMOnjqx9mqZVjC"
strAppSecret = "qm1e5kInsLjJnVu8HW8tTdGlaWxVs3Aj"

strTestMode = "POST"
strPath = "/v1/communities/688/accountLogs"

# 接口测试业务参数
testBody = '{"nfc_uid":"043ccc8d","type":"pay","amount":1000}'

# 生成content-md5(将业务参数加密)
m5 = hashlib.md5()
m5.update(testBody.encode('utf-8'))
strContent_MD5 = base64.b64encode(bytes(m5.digest())).decode('utf-8')

# 其他header参数
host = "open-api.haoyong.me"

strContent_Type = "application/json;charset=utf-8"

strDate = datetime.datetime.utcnow().strftime('%a, %d %b %Y %H:%M:%S GMT')

strX_signature_method = "HMAC-SHA1"

name = '接口测试'
namespace = uuid.NAMESPACE_URL
strX_signature_nonce = uuid.uuid1()

strX_signature_version = "1.0"

Signature = """%(test_mode)s
%(content_md5)s
%(content_type)s
%(date)s
%(hosts)s
%(signature_method)s
%(signature_nonce)s
%(signature_version)s
%(path)s"""
Signature = Signature % dict(test_mode=strTestMode, content_md5=strContent_MD5, content_type=strContent_Type, date=strDate, hosts=host,
                             signature_method=strX_signature_method, signature_nonce=strX_signature_nonce, signature_version=strX_signature_version, path=strPath)
# 生成签名认证(strAppid:strSignature)
digest = hmac.new(strAppSecret.encode(
    'utf-8'), msg=Signature.encode('utf-8'), digestmod=hashlib.sha1).digest()
strSignature = base64.b64encode(bytes(digest)).decode('utf-8')
strAuthorization = strAppid + ":" + strSignature

# 生成 curl
testCurlStr = '''
curl "http://{host}{path}" \\
  -X POST \\
  -H "Host: {host}" \\
  -H "Content-Type: {contentType}" \\
  -H "Content-MD5: {contentMD5}" \\
  -H "Authorization: {authorization}" \\
  -H "Date: {date}" \\
  -H "x-signature-method: {signMethod}" \\
  -H "x-signature-nonce: {signNonce}" \\
  -H "x-signature-version: {signVersion}" \\
  --compressed \\
  --insecure \\
  -d '{data}'
'''.format(path=strPath, host=host, contentType=strContent_Type, contentMD5=strContent_MD5, authorization=strAuthorization, date=strDate, signMethod=strX_signature_method, signNonce=strX_signature_nonce, signVersion=strX_signature_version, data=testBody)

print("\ncopy and execute the `curl` command below to test in your terminal...")
print(testCurlStr)
