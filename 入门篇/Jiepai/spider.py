from hashlib import md5
from urllib.parse import urlencode
import requests
from requests.exceptions import RequestException
import json
from bs4 import BeautifulSoup
import re
import pymongo
from config import *
import os
from multiprocessing import Pool

client=pymongo.MongoClient(MONGO_URL)
db=client[MONGO_DB]

def get_page_index(offset,keyword):
    data={'offset':offset,
        'format':'json',
        'keyword':keyword,
        'autoload':'true',
        'count':'20',
        'cur_tab':'1'}
    url='http://www.toutiao.com/search_content/?'+urlencode(data)
    try:
        response=requests.get(url)
        if response.status_code==200:
            return response.text
        return response.status_code
    except RequestException:
        print('请求索引页出错')
        return None

def parse_page_index(html):
    if html:
        data=json.loads(html)
        if data and 'data' in data.keys():
            for item in data.get('data'):
                yield item.get('article_url')

def get_page_detail(url):
    try:
        response=requests.get(url)
        if response.status_code==200:
            return response.text
        return response.status_code
    except RequestException:
        print('请求详情页出错')
        return None


def parse_page_detail(html,url):
    soup=BeautifulSoup(html,'lxml')
    title=soup.select('title')[0].get_text()
    print(title)
    pattern=re.compile('gallery: (.*?),\n',re.S)
    sub_images=re.search(pattern,html)
    if sub_images and sub_images.group(1):
        # print(sub_images.group(1))
        data=json.loads(sub_images.group(1))
        if data and 'sub_images' in data.keys():
            sub_images=data.get('sub_images')
            images=[item.get('url')for item in sub_images]
            for image in images:
                download_image(image)
            return {
                'title':title,
                'url':url,
                'images':images
            }
def save_to_mongodb(result):
    if db[MONGO_TABLE].insert(result):
        print('保存到MONGODB成功')
        return True
    else:
        print('保存至MONGODB失败')
        return False

def download_image(url):
    print('正在下载',url)
    try:
        response=requests.get(url)
        if response.status_code==200:
            save_image(response.content)
        return response.status_code
    except RequestException:
        print('下载图片出错')
        return None

def save_image(content):
    file_name='{0}/{1}.{2}'.format(os.getcwd(),md5(content).hexdigest(),'jpg')
    if not os.path.exists(file_name):
        with open(file_name,'wb') as f:
            f.write(content)
            f.close()

def main(offset):
    html=get_page_index(offset,KEYWORDS)
    for article_url in parse_page_index(html):
        html=get_page_detail(article_url)
        if html:
            result=parse_page_detail(html,article_url)
            if result:
                save_to_mongodb(result)

if __name__=='__main__':
    pool=Pool()
    pool.map(main,[i*20 for i in range(0,20)])















