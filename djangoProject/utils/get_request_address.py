#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import requests


def get_req_info(ip):
    r = requests.get(f'http://whois.pconline.com.cn/ipJson.jsp?ip={ip}&json=true')
    return r.json()['addr']


if __name__ == '__main__':
    get_req_info('127.0.0.1')
