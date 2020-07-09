#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author: 'zfb'
# time: 2020-07-09 15:41

from ipaddress import IPv4Network, ip_address
import logging
from app.config import SSH_IP_ALLOW, SSH_IP_BLOCK, SSH_IP_MODE

logging = logging.getLogger('runserver.sshfilter')


# 根据config的规则生成所有IP，因为有子网掩码
def get_ips(ips):
    ip_list = [x for x in ips if '/' not in x]
    ip_subnets = [x for x in ips if '/' in x]
    for i in ip_subnets:
        ip_list = ip_list + [str(ip) for ip in IPv4Network(i)]
    return ip_list

# 根据ip返回地理位置和ISP
def ip2geo(ip):
    import requests
    geo = requests.get("http://whois.pconline.com.cn/ip.jsp?ip={}".format(ip)).text
    return geo.replace('\r','').replace('\n','')

# 根据IP判断是否允许此用户连接
def ip_check(ip):
    ip = ip_address(ip)
    if SSH_IP_MODE == 'allow':
        # 如果允许名单为空，表示全部禁止
        if len(SSH_IP_ALLOW) == 0:
            return False
        try:
            ips = list(map(IPv4Network, SSH_IP_ALLOW))
        except Exception as e:
            # 可能会有子网掩码表示出错，则只保留单个ip
            print(repr(e))
            logging.error(e)
            ips = [IPv4Network(x) for x in SSH_IP_ALLOW if '/' not in x]
        # 判断IP是否在范围内
        for ip_range in ips:
            if ip in ip_range:
                return True
        else:
            return False
    elif SSH_IP_MODE == 'block':
        # 如果阻止名单为空，表示全部允许
        if len(SSH_IP_BLOCK) == 0:
            return True
        try:
            ips = list(map(IPv4Network, SSH_IP_BLOCK))
        except Exception as e:
            # 可能会有子网掩码表示出错，则只保留单个ip
            print(repr(e))
            logging.error(e)
            ips = [x for x in SSH_IP_BLOCK if '/' not in x]
        # 判断IP是否在范围内
        for ip_range in ips:
            if ip in ip_range:
                return False
        else:
            return True