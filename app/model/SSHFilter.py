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
        # 允许的IP列表
        allow_list = []
        # 如果允许名单为空，表示全部禁止
        if len(SSH_IP_ALLOW) == 0:
            return False
        # 判断允许名单是文件还是列表
        if not isinstance(SSH_IP_ALLOW, list):
            with open(SSH_IP_ALLOW, "r") as file:
                allow_list = file.read().splitlines()
        else:
            allow_list = SSH_IP_ALLOW
        # 开始判断该IP是否在名单
        try:
            ips = list(map(IPv4Network, allow_list))
        except Exception as e:
            # 可能会有子网掩码表示出错，则只保留单个ip
            print(repr(e))
            logging.error(e)
            ips = [IPv4Network(x) for x in allow_list if '/' not in x]
        # 判断IP是否在范围内
        for ip_range in ips:
            if ip in ip_range:
                return True
        else:
            return False
    elif SSH_IP_MODE == 'block':
        # 禁止的IP列表
        deny_list = []
        # 如果阻止名单为空，表示全部允许
        if len(SSH_IP_BLOCK) == 0:
            return True
        # 判断禁止名单是文件还是列表
        if not isinstance(SSH_IP_BLOCK, list):
            with open(SSH_IP_BLOCK, "r") as file:
                deny_list = file.read().splitlines()
        else:
            deny_list = SSH_IP_BLOCK
        # 开始判断该IP是否在名单
        try:
            ips = list(map(IPv4Network, deny_list))
        except Exception as e:
            # 可能会有子网掩码表示出错，则只保留单个ip
            print(repr(e))
            logging.error(e)
            ips = [x for x in deny_list if '/' not in x]
        # 判断IP是否在范围内
        for ip_range in ips:
            if ip in ip_range:
                return False
        else:
            return True