#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import requests


def get_req_info(ip):
    """
    获取请求IP的地址

    :param ip:
    :return:
    """
    rq = requests.session()
    rq.trust_env = False
    rp = rq.get(f'http://whois.pconline.com.cn/ipJson.jsp?ip={ip}&json=true')
    return rp.json()['addr']


if __name__ == '__main__':
    get_req_info('127.0.0.1')
