#!/usr/bin/env python3
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
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36'}
    r = requests.get(url, headers=headers)
    sel = etree.HTML(r.text)
    page = sel.xpath('//ul[@class="pagination"]/li[8]/a/attribute::href')[0]
    for li in sel.xpath('//tbody//tr'):
        if  li.xpath('./td[6]/text()')[0] == "支持":
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
        proxies = {'http': proxy_url, 'https': proxy_url, }
        print("[*] 正在检测第" + str(i) + "个IP......",end="")
        try:
            r = requests.get("http://ip111.cn/", proxies=proxies, timeout=3)
        except requests.exceptions.RequestException as e:
            i += 1
            print("超时")
            continue
        if r.status_code == 200:
            checked_list.append(proxy)
            print("可用")
        else:
            print("Response Code:", r.status_code)
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
    print("[!] 本脚本基于小幻HTTP代理，请勿大量抓取代理^-^")
    print("[*] 正在执行获取代理脚本，您可以随时通过ctrl+c终止选取过程并进入后续步骤")
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
                proxy_list, page = getproxy(page)
                checked_list += checkproxy(proxy_list)
                if len(checked_list) < 3:
                    print("[!] 由于可用IP少于3个，鉴于免费代理的不稳定性， 将自动获取更多代理")
                    continue
                else:
                    break
        else:
            print("[*] 检测到本地代理文件，正在测试可用性...")
            checked_list += checkproxy(proxy_list)
            if len(checked_list) < 3:
                print("[!] 由于可用IP少于3个，鉴于免费代理的不稳定性， 将自动获取更多代理")
                while True:
                    proxy_list, page = getproxy(page)
                    checked_list += checkproxy(proxy_list)
                    if len(checked_list) < 3:
                        continue
                    else:
                        break
        print(checked_list)
    except IOError:
        print('Permisson deny,check that you have permission to read and write %s', path)
    except KeyboardInterrupt:
        pass
    except IndexError:
        print("出现异常，请稍后重试")
    finally:
        for proxy in checked_list:
            f.write(proxy + "\n")
        f.close()


if __name__ == '__main__':
    main()

