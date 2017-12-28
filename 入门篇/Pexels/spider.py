import requests
from requests.exceptions import RequestException
from pyquery import PyQuery as pq
import time
import os
from hashlib import md5
from multiprocessing import Pool
from config import *

def get_index(url):
    response=requests.get(url,headers=headers)
    try:
        if response.status_code==200:
            return response.text
        return None
    except RequestException:
        return None

def parse_index(html):
    doc=pq(html)
    links=doc('.photos .photo-item a img')
    for link in links:
        # title=pq(link).attr('alt').replace(',','')
        url=pq(link).attr('data-pin-media').replace('images','static').split('?')[0]
        yield url

def download_img(url):
    response=requests.get(url)
    try:
        if response.status_code==200:
            return response.content
        return None
    except RequestException:
        return None

def save_image(content):
        path_name='{0}/{1}.{2}'.format(os.getcwd(),md5(content).hexdigest(),'jpg')
        if not os.path.exists(path_name):
            with open(path_name,'wb') as f:
                f.write(content)
                f.close()

def main(page):
    url = 'https://www.pexels.com/search/'+keyword+'/?page='+str(page)
    html=get_index(url)
    if html:
        urls=parse_index(html)
        for url in urls:
            print('正在下载:%r'%url)
            content=download_img(url)
            save_image(content)
            print('下载完成:%r'%url)
            time.sleep(3)

if __name__=='__main__':
    pool=Pool()
    pool.map(main,[i*1 for i in range(start_page,stop_page+1)])

