#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author: 'zfb'
# time: 20-07-08 19:24:15

# flask秘钥
FLASK_SECRET_KEY = "qrd762^$#&*hgwd$%UTD(*#RYD"
# 验证字符串，用以快速添加IP的允许名单
AUTH_STR = "wqfK3JQ7Re2JngWpqtd2C542890tewkvslGDJVifvjFfindPf6xmdCGwYoJejhKwPfqqo"
# 钉钉群机器人的安全密钥
DINGTALK_SECRET_KEY = "SECff11ffffffffffffffffffffffffffff896c5cb6d21234567898765432123876"
# 钉钉群机器人的接入秘钥
DINGTALK_ACCESS_TOKEN = "896c5cb6d212896c5cb6d212ac9d9dac896c5cb6d2120dd24896c5cb6d2128c4"

# frps.ini，若未设置，则写为""即可
subdomain_host = "example.cn"

# no表示不过滤IP，允许所有的IP，此时忽略SSH_IP_BLOCK、SSH_IP_ALLOW
# allow表示允许名单模式，只有SSH_IP_ALLOW允许访问，此时忽略SSH_IP_BLOCK
# block表示禁止名单模式，只有SSH_IP_BLOCK禁止访问，此时忽略SSH_IP_ALLOW
SSH_IP_MODE = 'no'
# 每个IP都用字符串表示；支持子网掩码格式，如192.168.0.0/28
# SSH_IP_ALLOW可以写成list，也可写成文件的绝对路径
# SSH_IP_ALLOW = ["202.114.12.11", "192.168.0.0/28"]
# allow.txt文件内容示例（每个IP占一行，不需要引号）
# 202.114.12.11
# 192.168.0.0/28
SSH_IP_ALLOW = "/home/zfb/frp-info/allow.txt"
SSH_IP_BLOCK = []
