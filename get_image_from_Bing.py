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
import os
import time
import requests
from bs4 import BeautifulSoup
import sys
import certifi


def makedir(localPath, keyword):
    localPath = os.path.join(localPath, keyword)
    if not os.path.exists(localPath):
        os.mkdir(localPath)
        
#     localPath = os.path.join(localPath, time.strftime("BING:%Y-%m-%d %H:%M", time.localtime(time.time())))
#     if not os.path.exists(localPath):
#         os.mkdir(localPath)
    if os.path.exists(localPath + '/URLlist.txt'):
        os.remove(localPath + '/URLlist.txt') 
        
    return localPath

def getImgUrl(keyword, page):
    
    links = []
    keyword = urllib.pathname2url(keyword)

    pn = page * 35
    url = 'http://cn.bing.com/images/async?q=%s&first=%s&count=35&relp=35&lostate=r&mmasync=1&dgState=x*152_y*1187_h*190_c*1_i*141_r*27&IG=F7F9D77717C14FBBB80ACC9F0099C872&SFX=5&iid=images.5651' % (
    keyword, pn)
    html = urllib.urlopen(url).read()
    soup = BeautifulSoup(html, 'lxml')
    allmimgImages = soup.findAll(attrs={'class':"iusc"})
    imgurl = soup.select(".iusc")
    for i, image in enumerate(imgurl):
        link = eval(image.attrs['m'])['murl']
        links.append(link)
    return(links)

def downImg(imgURL, dirPath, name):

    with open(dirPath + '/URLlist.txt', 'a') as f:
        f.write(imgURL + '\n')
    try:
        ir = requests.get(imgURL, verify=certifi.old_where(), timeout=15)
#         if str(ir.status_code)[0] == '4':
#             print("\n%s:%s" % (str(ir.status_code), imgURL))
#             return False
    except Exception as e:
        print("\nERROR:%s" % imgURL)
        print(e)
        return False
    imgtype = imgURL.split('.')[-1]
    if imgtype.find('/'):
        imgtype = 'jpg'
    with open((dirPath + '/%d.' + imgtype) % name, 'wb') as f:
        f.write(ir.content)
        return True

def getKeyword(keywordsPath):
    keywordlist = []
    with open(keywordsPath, 'r') as f:
        lines = f.readlines()
        for line in lines:
            keywordlist.append(line.split('\n')[0])
        return(keywordlist)    
    
def main(keyword):

    localPath = '/image_dir/' # 下载图片保存的位置
    pages = 500
    x = 1
    allofurl = 0
    
    savePath = makedir(localPath, keyword)
    print(savePath)
    for i in range(pages):
        dataList = getImgUrl(keyword, i)
        for imgURL in dataList:
            allofurl += 1
            if downImg(imgURL, savePath, x):
                sys.stdout.write('\r成功下载\t%s/%s张' % (x, allofurl))
                sys.stdout.flush()
                x += 1
            if x > 200:
                break
        if x > 200:
            break

    print(u'\n下载结束,成功 %s 个, 失败 %s 个' % (x-1, pages*35-x+1))    

if __name__ == '__main__':
    keywords_path = '/state_leaders_temp_bing.txt' # 包含搜索关键词的文本文件
    keywordslist = getKeyword(keywords_path)
    for keyword in  keywordslist:
        main(keyword)
