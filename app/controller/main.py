#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author: 'zfb'
# time: 20-07-08 19:40:23
from app import app
from flask import request
import app.config as config
import logging
import json

from app.model.HandleFrpMsg import handlemsg

# 初始化
logging = logging.getLogger('runserver.main')

@app.route('/handler', methods=["POST", "GET"])
def handler():
    if request.method == "GET":
        logging.debug('GET访问')
        data = [{'提示': "非法访问"}]
        return json.dumps(data, ensure_ascii=False), 403
    try:
        logging.debug('POST访问')
        data = request.json
        # print(data)
        # 处理来自frp的请求数据
        is_allow_ssh = handlemsg(data)
        if is_allow_ssh:
            # 不拒绝连接，保持不变；即不对内容进行任何操作
            response_data = {"reject": False, "unchange": True}
        else:
            # 拒绝连接，非法用户
            response_data = {"reject": True, "reject_reason": "invalid user"}
        logging.debug(response_data)
        return json.dumps(response_data, ensure_ascii=False), 200
    except Exception as e:
        logging.error(repr(e))
        return 404


@app.route('/auth/fHfuglg_RpLHJBcXDZTYTDHG_ydyydYCYFCcxFFcgx_cJnbVBMjhDSweq_ryiutHG', methods=["GET"])
def auth():
    if request.method == "GET":
        logging.debug('GET访问AUTH')
        auth_str = request.args.get("token", type=str, default=None)
        if auth_str == config.AUTH_STR:
            if not isinstance(config.SSH_IP_ALLOW, list):
                ip = request.headers.get('X-Real-Ip', request.remote_addr)
                with open(config.SSH_IP_ALLOW, "r+") as file:
                    exist_ips = file.read().splitlines()
                    if ip in exist_ips:
                        data = [{'警告': "您的IP：{} 已被授权".format(ip)}]
                        return json.dumps(data, ensure_ascii=False), 502
                    else:
                        file.write(ip+"\n")
                        file.flush()
                        data = [{'提示': "您的IP：{} 成功加入允许名单".format(ip)}]
                        return json.dumps(data, ensure_ascii=False), 200
        else:
            data = [{'警告': "非法访问"}]
            return json.dumps(data, ensure_ascii=False), 403