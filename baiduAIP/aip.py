# -*- coding: UTF-8 -*-
"""
百度人脸检测的demo，请先在百度AI开发平台申请开发者权限
"""
import requests
import base64
import json

# 定义常量
APP_ID = "11523614"
API_KEY = "5ZlfEA3FXeorXqegIX6fsSwN"
SECRET_KEY = "lblBMiavAKKuBX14m9sEnEzj1T63ztKK"


def get_access_token(appid, apikey, secretkey):
    # client_id 为官网获取的AK， client_secret 为官网获取的SK
    host = "https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id=" \
           + apikey + "&client_secret=" + secretkey
    print(host)
    headers = {
        'Content-Type': 'application/json; charset=UTF-8'
    }
    resp = requests.get(host, headers=headers)
    print(resp.status_code)
    body = resp.json()
    print(body)
    return body


def base64_image(filename):
    f = open(filename, 'rb')  # 二进制方式打开图文件
    ls_f = base64.b64encode(f.read())  # 读取文件内容，转换为base64编码
    f.close()
    return ls_f


def detect(access_token, image):
    '''
    人脸检测与属性分析
    '''

    request_url = "https://aip.baidubce.com/rest/2.0/face/v3/detect"
    params = "{\"image\":\"" + image + "\",\"image_type\":\"BASE64\",\"face_field\":\"faceshape,facetype\"}"
    print("params: " + params)
    headers = {
        'Content-Type': 'application/json; charset=UTF-8'
    }
    request_url = request_url + "?access_token=" + access_token
    response = requests.post(url=request_url, data=params, headers=headers)
    content = response.json()
    if content:
        print(content)


def match(access_token, image1, image2):
    '''
    人脸对比
    '''

    request_url = "https://aip.baidubce.com/rest/2.0/face/v3/match"

    params = json.dumps(
        [{"image": image1, "image_type": "BASE64", "face_type": "LIVE", "quality_control": "LOW"},
         {"image": image2, "image_type": "BASE64", "face_type": "LIVE", "quality_control": "LOW"}])
    headers = {
        'Content-Type': 'application/json; charset=UTF-8'
    }
    request_url = request_url + "?access_token=" + access_token
    response = requests.post(url=request_url, data=params, headers=headers)
    content = response.json()
    if content:
        print(content)


if __name__ == '__main__':
    image = base64_image(r"image\Amber--单看脸的话_哪些女明星有小说女主角的逆天颜值_--2.jpg")
    image_str = image.decode('utf-8')
    print("image: " + image_str)
    image2 = base64_image(r"image\Amber--单看脸的话_哪些女明星有小说女主角的逆天颜值_--3.jpg")
    image_str2 = image2.decode('utf-8')
    print("image2: " + image_str2)
    access_token_response = get_access_token(APP_ID, API_KEY, SECRET_KEY)
    detect(access_token_response['access_token'], image_str)
    match(access_token_response['access_token'], image_str, image_str2)

