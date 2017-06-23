#!/usr/bin/env python
#_*_ coding:utf-8 _*_
################################################
#
# file: get_image_from_baidu.py
# authou: wang-tf
# date: 2017-06-07 09:31
#
################################################

import requests
import os
import time
import sys
import certifi
import re

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
str_maplist = {
    '_z2C$q': ':',
    '_z&e3B': '.',
    'AzdH3F': '/'
}

char_table = {ord(key): ord(value) for key, value in maplist.items()}

def makedir(local_path, keyword):
    
    local_path = os.path.join(local_path, keyword)
    if not os.path.exists(local_path):
        os.mkdir(local_path)
    # 增加日期文件夹
#     local_path = os.path.join(local_path, time.strftime("BAIDU:%Y-%m-%d %H:%M", time.localtime(time.time())))
#     if not os.path.exists(local_path):
#         os.mkdir(local_path)
    # 创建链接保存文件
    if os.path.exists(local_path + '/URLlist.txt'):
        os.remove(local_path + '/URLlist.txt')     
    
    return local_path

def uncompile(url):

    for key, value in str_maplist.items():
        url = url.replace(key, value)
    return url.translate(char_table)             
                
def getKeyword(keywordsPath):
    keywordlist = []
    with open(keywordsPath, 'r') as f:
        lines = f.readlines()
        for line in lines:
            keywordlist.append(line.replace('\n','').strip())
        return(keywordlist)
    
re_url = re.compile(r'"objURL":"(.*?)"')
def getUrlFromPage(keyword, page_number):
    
    params = {
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
                      'pn': page_number * 30,
                      'rn': 30,
                      'gsm': '1e',
                      '1488942260214': ''
                  }
    url = 'https://image.baidu.com/search/acjson'
    urlcontent = requests.get(url, params=params, verify=certifi.old_where()).content.decode('utf-8')    
    urls = [uncompile(x) for x in re_url.findall(urlcontent)]
    return urls

def downloadUrl(img_url,save_path, save_name):
    try:
        ir = requests.get(img_url, timeout=15)
#         if str(ir.status_code)[0] == '4':
#             print("\n%s:%s" % (str(ir.status_code), imgURL))
#             return False
    except Exception as e:
        print("\nERRORURL:%s" % img_url)
        print(e)
        return False
    
    img_type = img_url.split('.')[-1]
    if img_type.find('/'):
        img_type = 'jpg'
    
    with open((save_path + '/%s.' + img_type) % str(save_name), 'wb') as f:
        f.write(ir.content)
        return True    

def main(keyword, local_path):
    # pages为要下载的网页数，每页30张图片
    pages = 500
    # 按序命名下载的图片，并统计
    img_number = 1
    url_number = 0
    # 创建对应的文件夹
    save_path = makedir(local_path, keyword)
    print(save_path)
    # 抓取url并下载图片
    for page_number in range(pages):
        url_list = getUrlFromPage(keyword, page_number)
        for url in url_list:
            url_number += 1
            if downloadUrl(url, save_path, img_number):
                sys.stdout.write('\r成功下载\t%s/%s张' % (img_number, url_number))
                sys.stdout.flush()
                img_number += 1              

    print(u'\n下载结束,成功 %s 个,失败 %s 个' % (img_number-1, url_number-img_number+1))    

def parse_arguments(argv):
    parser = argparse.ArgumentParser()
    parser.add_argument('--keywords_list', help='a text file include keywords.')
    parser.add_argument('--output_dir', help='Directory with download images')
    return parser.parse_args(argv)

if __name__ == '__main__':
    args = parse_arguments(sys.argv[1:])
    keywords_path = args.keywords_list
    local_path = args.output_dir
    keywordslist = getKeyword(keywords_path)
    for keyword in  keywordslist:
        main(keyword, local_path)
