#!usr/bin/python
# -*- coding:utf-8 -*-
# Author：Bruce Wang
# 文件demo

import os

def file_name(file_dir):
    L=[]
    for root, dirs, files in os.walk(file_dir):
        for file in files:
            if os.path.splitext(file)[1] == '.jpg':
                L.append(os.path.join(root, file))
    return L

def listdir(path, list_name):  #传入存储的list
    for file in os.listdir(path):
        file_path = os.path.join(path, file)
        if os.path.isdir(file_path):
            listdir(file_path, list_name)
        else:
            if file_path.endswith('.jpg') or file_path.endswith('.png'):
                list_name.append(file_path)

def main():
    '''
    主函数入口
    '''
    while True:
        num = input("Enter menu:\n1. file_name示例.\n2. listdir示例.\n3. exit.\n")
        if "1" == num:
            fileList = file_name(r"C:\Users\ubt\Pictures\photo")
            return print(fileList)
        elif "2" == num:
            fileList = []
            listdir(r"C:\Users\ubt\Pictures\photo", fileList)
            print(fileList)
            return 0
        elif "3" ==num:
            return 0
        else:
            continue
        return

if __name__ == '__main__':
    main()