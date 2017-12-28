import requests
from requests.exceptions import RequestException
from bs4 import BeautifulSoup
from config import *
import os
from hashlib import md5

def get_page_index(url):
    try:
        response=requests.get(url)
        if response.status_code==200:
            return response.text
        return response.status_code
    except RequestException:
        return None

def parser_page_index(html):
    soup=BeautifulSoup(html,'lxml')
    results=soup.select('a.list-group-item.random_list')
    for result in results:
        title=result.select('div.random_title')[0].text[:-10]
        print(title)
        date=result.select('div.date')[0].text
        print(date)
        for url in result.select('img.lazy.image_dtb.img-responsive'):
            url=url.attrs['data-original']
            print(url)
            save_images(download_images(url))

def download_images(url):
    try:
        print('正在下载',url)
        response=requests.get(url)
        if response.status_code==200:
            return response.content
        return response.status_code
    except RequestException:
        return None

def save_images(content):
    try:
        path_name='{0}/{1}.{2}'.format(os.getcwd(),md5(content).hexdigest(),'jpg')
        if not os.path.exists(path_name):
            with open(path_name,'wb') as f:
                f.write(content)
                f.close()
    except Exception:
        pass

def main(page):
    url='https://www.doutula.com/article/list/?page='+str(page)
    print('正在处理第%s页'%page)
    html=get_page_index(url)
    parser_page_index(html)


if __name__=='__main__':
    for i in range(START,STOP):
        main(i)

