import requests
from requests.exceptions import ConnectionError
from urllib.parse import urlencode
from pyquery import PyQuery as pq
import pymongo
from config import *

headers={
    'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Encoding':'gzip, deflate, sdch',
    'Accept-Language':'zh-CN,zh;q=0.8',
    'Connection':'keep-alive',
    'Cookie':'SUV=00125A02DE4FD3DD594693E2E1BA1824; CXID=99E0C697761AD07EE29B7491F50B42C7; SUID=95D04FDE3120910A0000000059570C5D; GOTO=Af12728; weixinIndexVisited=1; pgv_pvi=7196534784; wuid=AAFPiA7qGgAAAAqLEyJ8zAEAIAY=; usid=WEhVXSB_pJAaNCd_; SNUID=0DF8615F3135687EFFA6B2EF31EEDBE7; ld=Gkllllllll2BqZeNlllllVuMlEDlllllT6@yOyllll9lllll9ylll5@@@@@@@@@@; LSTMV=127%2C26; LCLKINT=4126; ABTEST=4|1505718213|v1; sct=16; IPLOC=CN3505; JSESSIONID=aaa0w6jEwqazT7dYfyr5v',
    'Host':'weixin.sogou.com',
    'Upgrade-Insecure-Requests':'1',
    'User-Agent':'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
}
proxy=None
proxy_pool_url='http://127.0.0.1:5000/get'
max_count=5

client=pymongo.MongoClient(MONGO_URI)
db=client[MONGO_DB]

def get_proxy():
    try:
        response=requests.get(proxy_pool_url)
        if response.status_code==200:
            return response.text
        return None
    except ConnectionError:
        return None

def get_html(url,count=1):
    print('Crawling',url)
    print('Trying count',count)
    global proxy
    if count > max_count:
        print('try too many times')
        return None
    try:
        if proxy:
            proxies={
                'http':'http://'+proxy
            }
            response=requests.get(url,allow_redirects=False,headers=headers,proxies=proxies)
        else:
            response=requests.get(url,allow_redirects=False,headers=headers)
        if response.status_code==200:
            return response.text
        if response.status_code==302:
            print('出现302错误,尝试使用代理')
            proxy=get_proxy()
            if proxy:
                print('Using proxy',proxy)
                return get_html(url)
            else:
                print('Get Proxy Failed')
                return None
    except ConnectionError:
        proxy=get_proxy()
        count=count+1
        return get_html(url,count)

def get_index(keyword,page):
    data={
        'query':keyword,
        'type':'2',
        'page':page
    }
    base_url='http://weixin.sogou.com/weixin?'
    url=base_url+urlencode(data)
    html=get_html(url)
    return html

def parse_index(html):
    doc=pq(html)
    items=doc('.news-box .news-list li .txt-box h3 a').items()
    for item in items:
        yield item.attr('href')

def get_detail(url):
    try:
        response=requests.get(url)
        if response.status_code==200:
            return response.text
        return None
    except ConnectionError:
        return None

def parse_detail(html):
    doc=pq(html)
    title=doc('.rich_media_title').text()
    post_date=doc('.rich_media_meta.rich_media_meta_text').text()
    content=doc('.rich_media_content').text()
    chat=doc('.rich_media_meta.rich_media_meta_link.rich_media_meta_nickname').text()
    return{
        'title':title,
        'post_date':post_date,
        'content':content,
        'chat':chat
    }

def save_mongo(data):
    if db['weixin_articles'].update({'title':data['title']},{'$set':data},True):
        print('Save to mongo',data['title'])
    else:
        print('Save to mongo fail',data['title'])

def main():
    for page in range(1,101):
        print('正在处理第%r页'%page)
        html=get_index('美景',page)
        if html:
            for article_url in parse_index(html):
                article_html=get_detail(article_url)
                if article_html:
                    data=parse_detail(article_html)
                    save_mongo(data)

if __name__=='__main__':
    main()





