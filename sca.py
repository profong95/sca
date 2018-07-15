#!/usr/bin/python3
import re
import os
import urllib.request
from bs4 import BeautifulSoup
ios_agent = 'Mozilla/5.0 (iPhone; CPU iPhone OS 8_0 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) Version/8.0 Mobile/12A365 Safari/600.1.4'

android_agent = 'Mozilla/5.0 (Linux; Android 4.4.4; HTC D820u Build/KTU84P) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/40.0.2214.89 Mobile Safari/537.36'

pc_agent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.139 Safari/537.36'

class Picture(object):
    def __init__(self, url, name):
        self.__url = url
        self.__name = name

    def set_url(self, url):
        self.__url = url

    def set_name(self, name):
        self.__name = name

    def get_url(self):
        return self.__url

    def get_name(self):
        return self.__name


def checkdir():
    if not os.path.exists('./img'):
        os.mkdir('./img')
    return

def download(name=(), url=()):
    sum = len(name)
    if len(name) != len(url):
        print('名称跟链接数目不符', len(name), len(url))
        return False
    print('开始下载', len(name), '张图片')
    for i in range(sum):
        with open('./img/'+name[i]+'.'+url[i][-3:], 'wb') as f:
            req = urllib.request.Request(url[i])
            req.add_header('User-Agent', ios_agent)

            try:
                look = urllib.request.urlopen(req)

            except urllib.error.HTTPError as e:
                print("错误:e")
            print('down '+name[i])
            f.write(look.read())
    return True

def gettitle(url):

    req = urllib.request.Request(url)
    req.add_header('User-Agent', ios_agent)

    try:
     html = urllib.request.urlopen(req)

    except urllib.error.HTTPError as e:
        print("错误:e")

    
    res = html.read()
     # print("html:\n", res.decode('utf-8'))
    bsobj = BeautifulSoup(res, "html5lib")
    try:
        content = bsobj.title
    except AttributeError as e:
        print("tag not found\n")
        return None
    print("结果如下\n", content)
    name = []
    reg = bsobj.findAll('span', {"class": "dy-name ellipsis fl"})
    for i in reg:
        name.append(i.get_text())
        print(i.get_text())
    pic = []
    reg = bsobj.findAll("img", {"data-original":re.compile("https://.*douyucdn.cn/.*(jpg|png)$")})
    for i in reg:
        pic.append(i['data-original'].lstrip())
        print("warning", i['data-original'].lstrip())
    download(name, pic)
    return True



checkdir()
res = gettitle('https://www.douyu.com/directory/game/DOTA2')
if(res == None):
    print('tag not found , sad\n')

