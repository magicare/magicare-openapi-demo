# -*- coding: utf-8 -*-

import hmac
import hashlib
import base64
import uuid
import datetime
import http.client

# 配置
appid = "yDRMOnjqx9mqZVjC"  # 麦麦提供
appsecret = "qm1e5kInsLjJnVu8HW8tTdGlaWxVs3Aj"  # 麦麦提供
content_type = "application/json;charset=utf-8"
host = "open-api.haoyong.me"  # 这是测试环境的 与对接环境相关 固定值


def get_http_headers(path, method, body=""):
    headers = {
        "Host": host,
        "Content-Type": content_type,
        "Content-MD5": "null"
    }
    # Content-MD5(对业务数据进行 md5 计算)
    if method != "GET":
        md5 = hashlib.md5()
        md5.update(body.encode('utf-8'))
        headers["Content-MD5"] = base64.b64encode(
            bytes(md5.digest())).decode('utf-8')

    # Date
    headers["Date"] = datetime.datetime.utcnow().strftime(
        '%a, %d %b %Y %H:%M:%S GMT')

    headers["x-signature-method"] = "HMAC-SHA1"

    headers["x-signature-version"] = "1.0"

    headers["x-signature-nonce"] = str(uuid.uuid1())

    if method == "POST":
        signature_tpl = '''{method}
{content_md5}
{content_type}
{date}
{host}
{signature_method}
{signature_nonce}
{signature_version}
{path}'''
    else:
        signature_tpl = '''{method}
{date}
{host}
{signature_method}
{signature_nonce}
{signature_version}
{path}'''

    signature_str = signature_tpl.format(method=method, content_md5=headers["Content-MD5"], content_type=headers["Content-Type"], date=headers["Date"], host=host,
                                         signature_method=headers["x-signature-method"], signature_nonce=headers["x-signature-nonce"], signature_version=headers["x-signature-version"], path=path)

    # 生成签名认证
    digest = hmac.new(appsecret.encode(
        'utf-8'), msg=signature_str.encode('utf-8'), digestmod=hashlib.sha1).digest()
    signature = base64.b64encode(bytes(digest)).decode('utf-8')
    headers["Authorization"] = appid + ":" + signature

    return headers


def test_api(path, method, body=""):
    headers = get_http_headers(path, method, body)
    # 生成 curl
    test_curl = '''
curl "http://{host}{path}" \\
    -X {method} \\
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
'''.format(path=path, method=method, host=host, contentType=headers["Content-Type"], contentMD5=headers["Content-MD5"], authorization=headers["Authorization"], date=headers["Date"], signMethod=headers["x-signature-method"], signNonce=headers["x-signature-nonce"], signVersion=headers["x-signature-version"], data=body)

    print("\n========================================")

    print("\nFYI, this is the `curl` command below...")
    print(test_curl)

    print("\n And then, send the request using http.client...\n")
    conn = http.client.HTTPConnection(host)
    conn.request(method=method, url=path, body=body, headers=headers)
    res = conn.getresponse()
    res_j = res.read().decode()
    print(res_j)

    print("\n========================================")


if __name__ == "__main__":
    # GET Request
    path_get = "/v1/echo?str=hello"
    test_api(path_get, "GET")

    # POST Request
    path_post = "/v1/communities/688/accountLogs"
    body_post = '{"nfc_uid":"043ccc8d","type":"pay","amount":1000}'
    test_api(path_post, "POST", body_post)
