import re
import requests
from requests.exceptions import RequestException
import json
from multiprocessing import Pool

def get_page(url):
    # headers={'User-Agent':'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'}
    response=requests.get(url)
    try:
        if response.status_code==200:
            return response.text
        return None
    except RequestException:
        return None

def parse_page(html):
    try:
        pattern=re.compile('<h2>(.*?)</h2>.*?<span>(.*?)</span>.*?number">(\d+)</i>.*?number">(\d+)</i>',re.S)
        results=re.findall(pattern,html)
        if results:
            for item in results:
                yield{
                    'name':item[0].strip(),
                    'content':item[1].strip(),
                    'laughter':item[2],
                    'comment':item[3]
                }
    except:
        pass

def save_result(result):
    if result:
        with open('result.txt','a',encoding='utf-8') as f:
            f.write(json.dumps(result,ensure_ascii=False)+'\n')
            f.close()

def main(page):
    url='https://www.qiushibaike.com/hot/page/'+str(page)
    html=get_page(url)
    for item in parse_page(html):
        print(item)
        save_result(item)

if __name__=='__main__':
    # pool=Pool()
    # pool.map(main,[i*1 for i in range(1,13)])
    for i in range(1,13):
        main(i)