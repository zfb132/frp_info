#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author: 'zfb'
# time: 2020-07-08 19:55

from datetime import datetime
import logging
import time

from app.config import SSH_IP_MODE, subdomain_host, RECEIVERS
from app.model.DingTalkBot import send_text as send_text_dingtalk
from app.model.FeishuBot import send_text as send_text_feishu
from app.model.SSHFilter import ip_check, ip2geo

logging = logging.getLogger('runserver.handlefrpmsg')

# 格式化时间戳
def timestamp_to_str(timestamp):
    return datetime.fromtimestamp(timestamp).strftime("%Y-%m-%d %H:%M:%S")

# 处理Login操作：frpc登录frps
def login_operation(data):
    str_fmt = "frp-client登录\nfrp版本：{}\n系统类型：{}\n系统架构：{}\n登录时间：{}\n连接池大小：{}"
    txt = str_fmt.format(
        data['version'], data['os'],
        data['arch'], timestamp_to_str(data['timestamp']), data['pool_count']
    )
    return txt

# 处理NewProxy操作：frpc与frps之间建立通道用于内网穿透
# proxy_name是frpc与frps之间建立的连接的名称
def newproxy_operation(data):
    run_id = data['user']['run_id']
    proxy_type = data['proxy_type']
    txt = "frp-client建立穿透代理\n主机ID：{}\n代理名称：{}\n代理类型：{}\n".format(
        run_id, data['proxy_name'], proxy_type
    )
    if proxy_type in ["tcp", "udp"]:
        txt += "远程端口：{}\n".format(data['remote_port'])
    elif proxy_type in ["http", "https"]:
        txt += "子域名：{}.{}\n".format(data['subdomain'], subdomain_host)
    return txt

# 处理NewUserConn操作：用户连接内网机器；用户（ssh）-->云服务器（frps）-->内网主机（frpc）
def newuserconn_operation(data):
    run_id = data['user']['run_id']
    ip = data['remote_addr'].split(':')[0]
    # 是否允许连接
    if SSH_IP_MODE == 'no':
        is_allow = True
    else:
        is_allow = ip_check(ip)
    # 用户地理位置
    position = ip2geo(ip)
    str_fmt = "用户连接内网机器\n内网主机ID：{}\n代理名称：{}\n代理类型：{}\n登录时间：{}\n用户IP和端口：{}\n用户位置：{}\n允许用户连接：{}"
    txt = str_fmt.format(
        run_id, data['proxy_name'], data['proxy_type'], timestamp_to_str(data['timestamp']), 
        data['remote_addr'], position, is_allow
    )
    return txt, is_allow

# 处理NewWorkConn操作
def newworkconn_operation(data):
    pass

# 处理frps的各种信息，包括以下几种
# Login、NewProxy、Ping、NewUserConn、NewWorkConn
def handlemsg(data):
    # 当前建立frp的类型
    operation = data['op']
    # frp请求的具体信息
    content = data['content']
    logging.debug(content)
    # 发送给管理员用户的提示
    txt = ""
    # 是否允许用户ssh连接
    is_allow_ssh = True
    # Ping操作每隔30s发送一次，不记录
    if operation == 'Ping':
        return True
    elif operation == 'Login':
        txt = login_operation(content)
    elif operation == 'NewProxy':
        txt = newproxy_operation(content)
    elif operation == 'NewUserConn':
        content['timestamp'] = int(time.time())
        txt, is_allow_ssh = newuserconn_operation(content)
    elif operation == 'NewWorkConn':
        return True
    else:
        # 基本不会出现此情况
        return True
    # 钉钉发送给管理员
    for receiver in RECEIVERS:
        if receiver == "dingtalk":
            send_text_dingtalk(txt)
        elif receiver == "feishu":
            send_text_feishu(txt)
    return is_allow_ssh
