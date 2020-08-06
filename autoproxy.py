#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Author: Gality
Name：autoproxy.py
Usage: python3 autoproxy.py
require: requests, lxml
Description: Get proxy automatically（China）and config sqlmap use proxy IP
E-mail: gality365@gmail.com
"""


import requests
import os
from lxml import etree


# 获取代理IP列表
def getproxy(page=''):
    print("[*] 正在获取代理IP列表")
    url = "https://ip.ihuan.me/address/5Lit5Zu9.html" + page
    proxy_list = []
    r = requests.get(url)
    sel = etree.HTML(r.text)
    page = sel.xpath('//ul[@class="pagination"]/li[8]/a/attribute::href')[0]
    for li in sel.xpath('//tbody//tr'):
        if li.xpath('./td[5]/text()')[0] == "支持" and li.xpath('./td[6]/text()')[0] == "支持":
            proxy_list.append(li.xpath('./td[1]/a/text()')[0] + ":" + li.xpath('./td[2]/text()')[0])
    if proxy_list == []:
        tmp_list, tmp = getproxy(page)
        proxy_list += tmp_list
    print("[*] 获取到" + str(len(proxy_list)) + "个代理IP")
    return proxy_list, page


# 检测代理可用性
def checkproxy(proxy_list):
    print("[*] 正在检测代理IP可用性,请稍等...")
    checked_list = []
    i = 1
    for proxy in proxy_list:
        proxy_url = "http://" + proxy
        proxies = {'http': proxy_url, 'https': proxy_url}
        print("[*] 正在检测第" + str(i) + "个IP......",end="")
        try:
            r = requests.get("https://www.baidu.com", proxies=proxies, timeout=3)
        except requests.exceptions.RequestException as e:
            i += 1
            print("超时")
            continue
        if r.status_code == 200:
            checked_list.append(proxy)
            print("可用")
        i += 1
    if checked_list == []:
        print("[!] 所有获取到的IP均不可用,将会自动获取新的代理")
    return checked_list


# 主函数
def main():
    path = os.path.dirname(os.path.realpath(__file__)) + '/proxy.txt'
    proxy_list = []
    checked_list = []
    page = ""
    try:
        try:
            f = open(path, 'r')
            for line in f.readlines():
                proxy_list.append(line[:-1])
        except IOError:
            pass

        f = open(path , 'w')
        if proxy_list == []:
            print("[!] 未检测到本地有代理IP列表文件，将自动获取代理IP")
            while True:
                proxy_list, page = getproxy()
                checked_list = checkproxy(proxy_list)
                if checked_list != []:
                    break
        else:
            print("[*] 检测到本地代理文件，正在测试可用性...")
            checked_list = checkproxy(proxy_list)
            if checked_list == []:
                while True:
                    proxy_list, page = getproxy()
                    checked_list = checkproxy(proxy_list)
                    if checked_list != []:
                        break
        for proxy in checked_list:
            f.write(proxy + "\n")
        print(checked_list)
    except IOError:
        print('Permisson deny,check that you have permission to read and write %s', path)
    finally:
        f.close()


if __name__ == '__main__':
    main()

