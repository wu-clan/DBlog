#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import requests


def get_request_address(ip):
    """
    获取请求IP的地址

    :param ip:
    :return:
    """
    rq = requests.session()
    rq.trust_env = False
    rp = rq.get(f'http://whois.pconline.com.cn/ipJson.jsp?ip={ip}&json=true')
    return rp.json()['addr']
