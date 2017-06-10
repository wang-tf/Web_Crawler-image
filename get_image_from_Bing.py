#!/usr/bin/env python
#_*_ coding:utf-8 _*_
################################################
#
# file: get_image_from_Bing.py
# authou: wang-tf
# date: 2017-06-09 09:31
#
################################################

import urllib
import urllib2
import re
import datetime
import os
import time
import requests
from bs4 import BeautifulSoup
import gzip
import StringIO


def getManyPages(keyword, page):
    links = []
    keyword = urllib.pathname2url(keyword)

    for i in range(page):
        pn = i * 35
        print("i=%s pn=%s" % (i, pn))
        url = 'http://cn.bing.com/images/async?q=%s&first=%s&count=35&relp=35&lostate=r&mmasync=1&dgState=x*152_y*1187_h*190_c*1_i*141_r*27&IG=F7F9D77717C14FBBB80ACC9F0099C872&SFX=5&iid=images.5651' % (
        keyword, pn)
        print(url)
        page = urllib.urlopen(url)
        html = page.read()
        soup = BeautifulSoup(html, 'lxml')
        allmimgImages = soup.findAll(attrs={'class':"iusc"})
        imgurl = soup.select(".iusc")
        for i, image in enumerate(imgurl):
            link = eval(image.attrs['m'])['murl']
            links.append(link)
    return(links)

def getImg(dataList, localPath):
    localPaht = os.path.join(localPath, time.strftime("%Y-%m-%d %H:%M", time.localtime(time.time())))
    if not os.path.exists(localPath):
        os.mkdir(localPath)
    if os.path.exists(localPath + '/URLlist.txt'):
        os.remove(localPath + '/URLlist.txt')
    
    x = 0
    for imgURL in dataList:
        print("正在下载imgURL:%s" % imgURL)
        open(localPath + '/URLlist.txt', 'a').write(imgURL + '\n')
        try:
            ir = requests.get(imgURL, verify = False)
        except :
            print("ERROR")
        open(localPath + '/bing-%d.jpg' % x, 'wb').write(ir.content)
        x += 1
    print(u'下载结束')

if __name__ == '__main__':
    dataList = getManyPages('动漫', 4)
    getImg(dataList, 'data0/users/wangtengfei/pictures/')
