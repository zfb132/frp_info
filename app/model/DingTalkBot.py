#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author: 'zfb'
# time: 2020-07-09 00:03

import base64
import hashlib
import hmac
import json
import requests
import time
import urllib.parse

import app.config as config

secret_key = config.DINGTALK_SECRET_KEY
token = config.DINGTALK_ACCESS_TOKEN

headers = {
    'Content-Type': 'application/json;charset=utf-8'
}

# 获取时间戳和签名
def get_params(secret):
    timestamp = str(round(time.time()*1000))
    secret_enc = secret.encode('utf-8')
    string_to_sign = '{}\n{}'.format(timestamp, secret)
    string_to_sign_enc = string_to_sign.encode('utf-8')
    hmac_code = hmac.new(secret_enc, string_to_sign_enc, digestmod=hashlib.sha256).digest()
    sign = urllib.parse.quote_plus(base64.b64encode(hmac_code))
    return timestamp, sign

# 发送消息并@指定成员
def send_text(txt, number=""):
    request_dict = {
        "msgtype": "text", 
        "text": {
            "content": txt
        }, 
        "at": {
            "atMobiles": ["{}".format(number)],
            "isAtAll": False
        }
    }
    # 保证中文可以正常发送
    data = json.dumps(request_dict, ensure_ascii=False).encode('utf-8')
    timestamp, sign = get_params(secret_key)
    url_base = "https://oapi.dingtalk.com/robot/send?access_token={}&timestamp={}&sign={}"
    url = url_base.format(token, timestamp, sign)
    response = requests.post(url, data, headers=headers).content
    print(response.decode('utf-8'))

if __name__ == "__main__":
    send_text("我在测试")