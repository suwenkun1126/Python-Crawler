import requests
from requests.exceptions import RequestException
from urllib.parse import urlencode
from bs4 import BeautifulSoup
import pymongo
from config import *
# from multiprocessing import Pool
import time

client=pymongo.MongoClient()
db=client[MONGO_DB]

def get_page(page):
    data={
        'jl':PALACE,
        'kw':KEYWORD,
        'sm':'0',
        'isfilter':'0',
        'fl':'489',
        'isadv':'0',
        'sg':'528fa12f8c1c47078a62f8c1db4a8e82',
        'p':page
    }
    headers={'User-Agent':'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'}
    url='http://sou.zhaopin.com/jobs/searchresult.ashx?'+urlencode(data)
    try:
        response=requests.get(url,headers=headers)
        if response.status_code==200:
            return response.text
        return response.status_code
    except RequestException:
        return None

def parse_page(html):
    soup=BeautifulSoup(html,'lxml')
    for result in soup.select('table.newlist'):
        position=result.select('td.zwmc div a')
        company=result.select('td.gsmc a')
        salary=result.select('td.zwyx')
        palace=result.select('td.gzdd')
        release_time=result.select('td.gxsj')
        if position and company and palace and release_time:
            data={
                'position':position[0].text,
                'company':company[0].text,
                'salary':salary[0].text,
                'palace':palace[0].text,
                'release_time':release_time[0].text
            }
            print(data)
            save_to_mongodb(data)

def save_to_mongodb(result):
    if db[MONGO_TABLE].insert(result):
        print('存储至MONGODB成功')
        return True
    else:
        print('存储至MONGODB失败')
        return False

def main(page):
    html=get_page(page)
    if html:
        print('正在处理第%s页'%page)
        parse_page(html)

if __name__=='__main__':
    start=time.time()
    for page in range(START_PAGE,END_PAGE):
        main(page)
    end=time.time()
    print('task run %s seconds'%(end-start))
    #使用多进程出现有些页面抓取不到的情况
    # pool=Pool()
    # pool.map(main,[i*1 for i in range(START_PAGE,END_PAGE)])
