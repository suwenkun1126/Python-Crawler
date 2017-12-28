import requests
from bs4 import BeautifulSoup
import random
from requests.exceptions import RequestException
import time
import pymongo
from config import *
from multiprocessing import Pool

client=pymongo.MongoClient(MONGO_URL)
db=client[MONGO_DB]

UA=['Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36',
    'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.11 (KHTML like Gecko) Chrome/23.0.1271.95 Safari/537.11',
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML like Gecko) Chrome/31.0.1650.63 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML like Gecko) Chrome/35.0.1916.153 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML like Gecko) Chrome/37.0.2062.120 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.11 (KHTML like Gecko) Chrome/23.0.1271.95 Safari/537.11',
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.31 (KHTML like Gecko) Chrome/26.0.1410.64 Safari/537.31',
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML like Gecko) Chrome/36.0.1985.125 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML like Gecko) Chrome/36.0.1985.143 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML like Gecko) Chrome/27.0.1453.110 Safari/537.36']
headers={
'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
'Accept-Encoding':'gzip, deflate, sdch',
'Accept-Language':'zh-CN,zh;q=0.8',
'Cache-Control':'max-age=0',
'Connection':'keep-alive',
'Host':'www.wandoujia.com',
'User-Agent': random.choice(UA)
}

def get_page(url):
    responses=requests.get(url,headers=headers)
    try:
        if responses.status_code==200:
            return responses.text
        return responses.status_code
    except RequestException:
        print('请求出现错误')
        return None

def parse_page(html):
    soup=BeautifulSoup(html,'lxml')
    for result in soup.select('div.list-wrap ul li'):
        issue=result.select('div.issue span')[0].text
        #print(issue)
        app_title=result.select('div.app-title')[0].text
        #print(app_title)
        img_url=result.select('img.icon ')[0]['data-original']
        #print(img_url)
        title=result.select('div.title')[0].text
        #print(title)
        content={
            'issue':issue,
            'app_title':app_title,
            'img_url':img_url,
            'title':title
        }
        print(content)
        save_to_mongodb(content)

def save_to_mongodb(result):
    if db[MONGO_TABLE_2].insert(result):
        print('存储至MONGODB成功')
    else:
        print('存储至MONGODB失败')

def main(i):
    print('正在处理第%r页'%i)
    url='http://www.wandoujia.com/award?page='+str(i)
    html=get_page(url)
    parse_page(html)

if __name__=='__main__':
    pool=Pool()
    start=time.time()
    pool.map(main,[i*1 for i in range(1,51)])
    end=time.time()
    print('所用时间：'+str(end-start))

