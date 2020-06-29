#!/usr/bin/env python
#-*- coding:UTF-8 -*-

import requests
import os

'''
功能：拥有url的连接，批量下载文件
提供参数：url和预定义的文件名  url filename
file:含有url和filename的文件列表
path:要保存的地址
'''


class downFiles(object):
    def __init__(self,file,path):
        self.file=file  #传入的是全限定文件路径
        self.path=path  #传入的是个路径

    def start(self,url,filename):
        file = requests.get(url)
        resultPath = os.path.join(self.path,filename)
        with open(resultPath, "wb") as code:
            code.write(file.content)

    def takeByTurns(self):
        print("开始下载......")
        with open(self.file,encoding="utf-8") as files:
            for item in files:
                filename,url = item.strip().split("\t")
                print("正在下载："+filename)
                self.start(url,filename+'.pdf')
        print("下载完成！")


if __name__=="__main__":
    file="E:\\download\\files\\urls.txt"
    resultpath="E:\\download\\files\\"
    doDownLoad = downFiles(file,resultpath)
    doDownLoad.takeByTurns()
