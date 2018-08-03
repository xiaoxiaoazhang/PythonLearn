# coding: utf-8
import itchat
import time
import re
import os
import math
import PIL.Image as Image
import base64
from aip import AipFace

import jieba
import matplotlib.pyplot as plt
from wordcloud import WordCloud, ImageColorGenerator
import numpy as np

# 百度云 人脸检测 申请信息
# 唯一必须填的信息就这三行
APP_ID = "11523614"
API_KEY = "5ZlfEA3FXeorXqegIX6fsSwN"
SECRET_KEY = "lblBMiavAKKuBX14m9sEnEzj1T63ztKK"
# 过滤颜值阈值，存储空间大的请随意
BEAUTY_THRESHOLD = 10
DIR = "headImg"
SCORE_DIR = "scoreHeadImg"


def init_face_detective(app_id, api_key, secret_key):
    client = AipFace(app_id, api_key, secret_key)
    # 人脸检测中，在响应中附带额外的字段。年龄 / 性别 / 颜值 / 质量
    options = {
        'max_face_num': 1,
        'face_field': 'age,beauty,expression,face_shape,gender,glasses,landmark,race,quality,face_type'
    }

    def detective(image):
        response = client.detect(image, "BASE64", options)
        # 如果没有检测到人脸
        result = response["result"]
        if response["error_code"] != 0 or result["face_num"] == 0:
            return []

        valid_faces = []
        for face in result["face_list"]:
            # 人脸置信度太低
            if face["face_probability"] < 0.6:
                continue
            # 人脸质量信息
            if face["quality"]["completeness"] != 1:
                continue
            # 颜值低于阈值
            if face["beauty"] < BEAUTY_THRESHOLD:
                continue
            valid_faces.append(face)

        return valid_faces

    return detective


def signature_analyze(friends):
    signature_list = []
    for friend in friends:
        signature = friend["Signature"].replace(" ", "").replace("span", "").replace("class", "").replace("emoji", "")
        rep = re.compile("1f\d.+")
        signature = rep.sub("", signature)
        signature_list.append(signature)

    # 拼接字符串
    text = "".join(signature_list)
    wordlist_jieba = jieba.cut(text, cut_all=True)
    wl_space_split = " ".join(wordlist_jieba)

    current_path = os.path.dirname(__file__)
    alice_coloring = np.array(Image.open(os.path.join(current_path, "xiaohuangren.jpg")))
    font_path = "./fonts/arial.ttf"
    my_word_cloud = WordCloud(background_color="white", max_words=2000, mask=alice_coloring, max_font_size=40, random_state=42,  font_path=font_path).generate(wl_space_split)

    image_colors = ImageColorGenerator(alice_coloring)
    plt.imshow(my_word_cloud.recolor(color_func=image_colors))
    plt.imshow(my_word_cloud)
    plt.axis("off")
    plt.show()

def friends_classify(friends):
    # 初始化计数器，有男有女，当然，有些人是不填的
    male = female = other = 0
    # 遍历这个列表，列表里第一位是自己，所以从"自己"之后开始计算
    # 1表示男性，2女性
    for friend in friends[1:]:
        sex = friend["Sex"]
        if sex == 1:
            male += 1
        elif sex == 2:
            female += 1
        else:
            other += 1
    # 总数算上，好计算比例啊～
    total = len(friends[1:])
    # 好了，打印结果
    print(u"总计%d好友 男%d人 女%d人 未知%d人" % (total, male, female, other))
    print(u"男性好友：%.2f%%" % (float(male) / total * 100))
    print(u"女性好友：%.2f%%" % (float(female) / total * 100))
    print(u"未填性别：%.2f%%" % (float(other) / total * 100))


def get_file_list(file_dir):
    file_list = []
    for root, dirs, files in os.walk(file_dir):
        for file in files:
            if os.path.splitext(file)[1] == '.jpg':
                file_list.append(os.path.join(root, file))
    return file_list


def friends_image(friends):
    index = 1
    for friend in friends:
        print("is saving number %d image %s" % (index, friend["NickName"]))
        index += 1
        image = itchat.get_head_img(friend["UserName"])
        with open('./headImg/' + friend["NickName"] + ".jpg", 'wb') as f:
            f.write(image)
            f.close()


def rename_friends_image(face_detective):
    file_list = get_file_list(DIR)
    index = 0
    for filepath in file_list:
        print("is score number %d image %s" % (index, os.path.basename(filepath)))
        index += 1
        with open(filepath, "rb") as file:
            image = file.read()
            image_bytes = base64.b64encode(image)
            image_str = image_bytes.decode('utf-8')
            # 请求人脸检测服务
            valid_faces = face_detective(image_str)
            for face in valid_faces:
                filename = ("%d--%s--" % (face["beauty"], face["gender"]["type"])) + os.path.basename(filepath)
                filename = re.sub(r'(?u)[^-\w.]', '_', filename)
                with open(os.path.join(SCORE_DIR, filename), 'wb') as f:
                    f.write(image)
                    f.close()
        # 人脸检测 免费，但有 QPS 限制
        time.sleep(2)


def show_image():
    # 获取文件夹内的文件个数
    length = len(os.listdir(SCORE_DIR))
    if length <= 0:
        print("this folder is not exist image!")
        return
    # 根据总面积求每一个的大小
    each_size = int(math.sqrt(float(810 * 810) / length))
    # 每一行可以放多少个
    lines = int(810 / each_size)
    # 生成白色背景新图片
    image = Image.new('RGB', (810, 810), 'white')
    x = 0
    y = 0
    for file in os.listdir(SCORE_DIR):
        try:
            img = Image.open(os.path.join(SCORE_DIR, file))
        except IOError:
            print(os.path.join(SCORE_DIR, file))
            print("Error")
        else:
            img = img.resize((each_size, each_size), Image.ANTIALIAS)  # resize image with high-quality
            image.paste(img, (x * each_size, y * each_size))
            x += 1
            if x == lines:
                x = 0
                y += 1
    image.save(os.path.join(SCORE_DIR, "all.jpg"))
    # 通过文件传输助手发送到自己微信中
    image.show()


def init_env():
    if not os.path.exists(DIR):
        os.makedirs(DIR)
    if not os.path.exists(SCORE_DIR):
        os.makedirs(SCORE_DIR)


def login_callback():
    print("Finish Login!")


def exit_ccllback():
    print("exit")


if __name__ == '__main__':
    init_env()
    face_detective = init_face_detective(APP_ID, API_KEY, SECRET_KEY)
    # 先登录
    # itchat.login()
    itchat.auto_login(loginCallback=login_callback(), exitCallback=exit_ccllback(), hotReload=False)
    # 获取好友列表
    friends = itchat.get_friends(update=True)
    friends_classify(friends)
    signature_analyze(friends)
    friends_image(friends)
    rename_friends_image(face_detective)
    show_image()
    # 退出微信
    itchat.logout()

