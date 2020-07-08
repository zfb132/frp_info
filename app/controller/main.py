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
        handlemsg(data)
        # 始终返回此信息：不拒绝连接，保持不变；即不对内容进行任何操作
        response_data = {"reject": False, "unchange": True}
        return json.dumps(response_data, ensure_ascii=False), 200
    except Exception as e:
        logging.error(repr(e))
        return 404