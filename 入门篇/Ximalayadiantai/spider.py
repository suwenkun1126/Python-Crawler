import requests
from requests.exceptions import RequestException
from bs4 import BeautifulSoup
import pymongo
from config import *
import time
import json

client=pymongo.MongoClient(MONGO_URL)
db=client[MONGO_DB]

def get_page_index(url):
    headers={'User-Agent':'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'}
    try:
        response=requests.get(url,headers=headers)
        if response.status_code==200:
            print('请求索引页正常')
            return response.text
        return response.status_code
    except RequestException:
        return None

def parse_page_index(html):
    soup=BeautifulSoup(html,'lxml')
    results=soup.select('div.discoverAlbum_item')
    for result in results:
        img_url=result.select('img')[0]['src']
        # print(img_url)
        album_title=result.select('a.discoverAlbum_title')[0].text
        # print(album_title)
        detail_url=result.select('a.discoverAlbum_title')[0]['href']
        # print(detail_url)
        content={
            'img_url':img_url,
            'album_title':album_title,
            'detail_url':detail_url
        }
        print(content)
        save_to_mongodb(MONGO_TABLE_1,content)
        print('存储到MONGO_TABLE_1成功')
        return detail_url

def get_page_detail(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'}
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            print('请求详情页正常')
            return response.text
        return response.status_code
    except RequestException:
        return None

def parse_page_detail(html):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'}
    soup=BeautifulSoup(html,'lxml')
    for result in soup.select('div.personal_body'):
        sound_ids=result['sound_ids'].split(',') #想利用CSS选择器直接提取属性sound_id的值不成功
        for sound_id in sound_ids:
            json_url='http://www.ximalaya.com/tracks/{}.json'.format(sound_id)
            response=requests.get(json_url,headers=headers)
            html=response.text
            data=json.loads(html)
            # print(data)
            save_to_mongodb(MONGO_TABLE_2,data)
            print('存储到MONGO_TABLE_2成功',data.get('play_path'))

def save_to_mongodb(table,result):
    if db[table].insert(result):
        return True
    return False

def main(page):
    url='http://www.ximalaya.com/dq/'+str(page)
    print('正在处理第%s页'%page)
    html=get_page_index(url)
    time.sleep(1)
    detail_url=parse_page_index(html)
    html=get_page_detail(detail_url)
    parse_page_detail(html)

if __name__=='__main__':
    for i in range(1,85):
        main(i)

