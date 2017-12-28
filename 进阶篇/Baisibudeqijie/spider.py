import requests
from requests.exceptions import RequestException
import re
import time
from multiprocessing import Pool

headers={
    'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Encoding':'gzip, deflate, sdch',
    'Cookie':'_ga=GA1.2.1244139225.1506604775; _gid=GA1.2.866718336.1506604775; tmc=10.43102518.27828979.1506604774708.1506605159556.1506605184056; tma=43102518.27828979.1506604774708.1506604774708.1506604774708.1; tmd=10.43102518.27828979.1506604774708.; bfd_s=43102518.11037409.1506604774704; bfd_g=82e346abcb0023bc0000087700001dd95978a30a',
    'User-Agent':'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36',
}

def get_page(url):
    response=requests.get(url,headers=headers)
    try:
        if response.status_code==200:
            return response.text
        return None
    except RequestException as e:
        print(e)
        return None

def parse_page(html):
    pattern=re.compile('class="j-video-c".*?data-title="(.*?)".*?data-mp4="(.*?)"',re.S)
    items=re.findall(pattern,html)
    for item in items:
        yield {
            'title':item[0].replace('...',''),
            'url':item[1]
        }

def save_video(url):
    try:
        response=requests.get(url)
        if response.status_code==200:
            return response.content
        return None
    except RequestException:
        return None

def main(page):
    Num=1
    url = 'http://www.budejie.com/video/'+str(page)
    print('正在开始处理第%r页'%page)
    html=get_page(url)
    if html:
        for item in parse_page(html):
            content=save_video(item['url'])
            if content:
                with open(item['title'].replace('，','')+'.mp4','wb')as f:
                    f.write(content)
                    f.close()
                    print('===============下载成功#{0}:{1}==============='.format(Num,item['title'].replace('，','')))
                    Num=Num+1
                    time.sleep(1)

if __name__=='__main__':
    try:
        for page in range(1,22):
            main(page)

        # pool=Pool()
        # pool.map(main,[i*1 for i in range(1,22)])
    except:
        pass
