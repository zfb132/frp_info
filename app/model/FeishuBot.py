#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author: 'zfb'
# time: 2023-09-02 11:47

import base64
import hashlib
import hmac
import json
import requests
import time
import urllib.parse

import app.config as config

webhook_url = config.FEISHU_WEBHOOK
token = config.FEISHU_SECRET_KEY

headers = {
    'Content-Type': 'application/json;charset=utf-8'
}

# 获取时间戳和签名
def get_params(secret):
    timestamp = str(round(time.time()))
    string_to_sign = '{}\n{}'.format(timestamp, secret)
    hmac_code = hmac.new(string_to_sign.encode("utf-8"), digestmod=hashlib.sha256).digest()
    # 对结果进行base64处理
    sign = base64.b64encode(hmac_code).decode('utf-8')
    return timestamp, sign

# 发送消息并@指定成员
def send_text(txt):
    # 判断是否有钉钉机器人的秘钥
    if not webhook_url or not token:
        return
    timestamp, sign = get_params(token)
    request_dict = {
        "timestamp": timestamp,
        "sign": sign,
        "msg_type": "text",
        "content": {
            "text": txt
        }
    }
    # 保证中文可以正常发送
    data = json.dumps(request_dict, ensure_ascii=False).encode('utf-8')
    response = requests.post(webhook_url, data, headers=headers).content
    print(response.decode('utf-8'))

if __name__ == "__main__":
    send_text("我在测试")