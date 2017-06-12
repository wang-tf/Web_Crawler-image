#!/usr/bin/env python
#_*_ coding:utf-8 _*_
################################################
#
# file: get_image_1.py
# authou: shixi_tengfei5
# date: 2017-06-07 09:31
#
################################################

import requests
import os
import time
import sys

maplist = {
        'w': 'a',
        'k': 'b',
        'v': 'c',
        '1': 'd',
        'j': 'e',
        'u': 'f',
        '2': 'g',
        'i': 'h',
        't': 'i',
        '3': 'j',
        'h': 'k',
        's': 'l',
        '4': 'm',
        'g': 'n',
        '5': 'o',
        'r': 'p',
        'q': 'q',
        '6': 'r',
        'f': 's',
        'p': 't',
        '7': 'u',
        'e': 'v',
        'o': 'w',
        '8': '1',
        'd': '2',
        'n': '3',
        '9': '4',
        'c': '5',
        'm': '6',
        '0': '7',
        'b': '8',
        'l': '9',
        'a': '0'
}

def uncompile(url):
    start = 0
    end = 1
    outurl = []
    output = url.replace('_z2C$q', ':')
    output = output.replace('_z&e3B', '.')
    output = output.replace('AzdH3F', '/')
    
    url = output
    while end <= len(url):
        change = False
        for key in maplist:
            if url[start:end] == key:
                outurl.append(maplist[key])
                start = end
                end = start + 1
                change = True
                break
        if change == False:
            outurl.append(url[start:end])
            start = end
            end = start + 1
    return(''.join(outurl))

def getManyPages(keyword,pages):
    params=[]
    for i in range(0,30*pages,30):
        params.append({
                      'tn': 'resultjson_com',
                      'ipn': 'rj',
                      'ct': 201326592,
                      'is': '',
                      'fp': 'result',
                      'queryWord': keyword,
                      'cl': 2,
                      'lm': -1,
                      'ie': 'utf-8',
                      'oe': 'utf-8',
                      'adpicid': '',
                      'st': -1,
                      'z': '',
                      'ic': 0,
                      'word': keyword,
                      's': '',
                      'se': '',
                      'tab': '',
                      'width': '',
                      'height': '',
                      'face': 0,
                      'istype': 2,
                      'qc': '',
                      'nc': 1,
                      'fr': '',
                      'pn': i,
                      'rn': 30,
                      'gsm': '1e',
                      '1488942260214': ''
                  })
    url = 'https://image.baidu.com/search/acjson'
    urls = []
    for i in params:
        urls.append(requests.get(url,params=i,verify=False).json().get('data'))

    return urls


def getImg(dataList, localPath):

    localPath = os.path.join(localPath, time.strftime("BAIDU:%Y-%m-%d %H:%M", time.localtime(time.time())))
    if not os.path.exists(localPath):
        os.mkdir(localPath)
    if os.path.exists(localPath + '/URLlist.txt'):
        os.remove(localPath + '/URLlist.txt')            

    x = 1
    error_num = 0
    for list in dataList:
        for i in list:
            if i == {}:
                continue
            if i.get('objURL') != None:
                imgURL = uncompile(i.get('objURL'))
                sys.stdout.write('\r正在下载第\t%s个' % x)
                sys.stdout.flush()
                open(localPath + '/URLlist.txt', 'a').write(imgURL + '\n')
                try:
                    ir = requests.get(imgURL, verify=False)
                except requests.ConnectionError:
                    error_num += 1
                    print("\nERRORURL:%s" % imgURL)
                    print(ir.status_code)
                imgtype = imgURL.split('.')[-1]
                if imgtype.find('/'):
                    imgtype = 'jpg'
                open((localPath + '/%d.' + imgtype) % x, 'wb').write(ir.content)
                
                x += 1
            else:
                print('\n图片链接不存在%s' % str(x))
    print(u'下载结束,成功 %s 个,失败 %s 个' % (x-error_num-1, error_num))

if __name__ == '__main__':
    
    keywords = u'人脸'
    localPath = '/data0/users/wangtengfei/pictures/'
    pages = 100
    
    dataList = getManyPages(keywords, pages)  # 参数1:关键字，参数2:要下载的页数
    getImg(dataList, localPath) # 参数2:指定保存的路径
