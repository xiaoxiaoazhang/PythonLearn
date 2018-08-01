#!usr/bin/python
# -*- coding:utf-8 -*-
# Author：Bruce Wang
# requests网络库使用demo
"""
requests库请求网络的使用demo
"""

import requests
import json


def get():
    payload = {'key1': 'value1', 'key2': 'value2'}
    r = requests.get('http://httpbin.org/get', params=payload)
    print(r.url)
    print(r.text)
    print(r.encoding)
    r.encoding = 'ISO-8859-1'
    print(r.encoding)

    payload = {'key1': 'value1', 'key2': ['value2', 'value3']}
    r = requests.get('http://httpbin.org/get', params=payload)
    print(r.url)

    print("##########################################")
    url = 'https://api.github.com/some/endpoint'
    headers = {'user-agent': 'my-app/0.0.1'}
    r = requests.get(url, headers=headers)
    print(r.url)
    print(r.text)


def post():
    payload = {'key1': 'value1', 'key2': 'value2'}
    r = requests.post("http://httpbin.org/post", data=payload)
    print(r.text)

    payload = (('key1', 'value1'), ('key1', 'value2'))
    r = requests.post('http://httpbin.org/post', data=payload)
    print(r.text)

    url = 'https://api.github.com/some/endpoint'
    payload = {'some': 'data'}
    r = requests.post(url, data=json.dumps(payload))
    print(r.text)

    url = 'https://api.github.com/some/endpoint'
    payload = {'some': 'data'}
    r = requests.post(url, json=payload)
    print(r.text)

    url = 'https://api.github.com/some/endpoint'
    headers = {'user-agent': 'my-app/0.0.1'}
    r = requests.get(url, headers=headers)
    print(r.url)
    print(r.text)


def post_file():
    url = 'http://httpbin.org/post'
    files = {'file': open('report.xls', 'rb')}
    r = requests.post(url, files=files)
    r.text

    url = 'http://httpbin.org/post'
    files = {'file': ('report.xls', open('report.xls', 'rb'), 'application/vnd.ms-excel', {'Expires': '0'})}
    r = requests.post(url, files=files)
    r.text

    url = 'http://httpbin.org/post'
    files = {'file': ('report.csv', 'some,data,to,send\nanother,row,to,send\n')}
    r = requests.post(url, files=files)
    r.text

    url = 'http://httpbin.org/post'
    multiple_files = [
        ('images', ('foo.png', open('foo.png', 'rb'), 'image/png')),
        ('images', ('bar.png', open('bar.png', 'rb'), 'image/png'))]
    r = requests.post(url, files=multiple_files)
    r.text


def put():
    r = requests.put('http://httpbin.org/put', data={'key': 'value'})
    print(r.text)


def main():
    """
    主函数入口
    """
    while True:
        num = input("Enter menu:\n1. get示例.\n2. post示例.\n3. exit.\n")
        if "1" == num:
            return get()
        elif "2" == num:
            return post()
        elif "3" == num:
            return 0
        else:
            continue
        return


if __name__ == '__main__':
    main()

