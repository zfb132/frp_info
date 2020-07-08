#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author: 'zfb'
# time: 2020-07-08 19:55

import logging
import json
from app.model.DingTalkBot import send_text

logging = logging.getLogger('runserver.handlefrpmsg')


# 处理frps的各种信息，包括以下几种
# Login、NewProxy、Ping、NewWorkConn、NewUserConn
def handlemsg(data):
    operation = data['op']
    # Ping操作每隔30s发送一次
    if operation == 'Ping':
        return
    content = data['content']
    send_text(json.dumps(content, ensure_ascii=False))
    logging.debug(content)
