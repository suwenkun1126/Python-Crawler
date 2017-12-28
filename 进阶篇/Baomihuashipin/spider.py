import requests
from requests.exceptions import RequestException
import re
import os
from hashlib import md5

headers={
        'User-Agent':'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36',
        'Accept-Encoding':'gzip, deflate, sdch',
        'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language':'zh-CN,zh;q=0.8',
    }

def get_part(url):
    try:
        response=requests.get(url,headers=headers)
        if response.status_code==200:
            return response.text
        return None
    except RequestException as e:
        print(e)
        return None

def parse_part_1(html):
    try:
        pattern=re.compile('.*?var flvid = (.*?);.*?',re.S)
        result_1=re.search(pattern,html).group(1)
        print('flvid为:'+result_1)
        return result_1
    except Exception:
        print('flvid解析失败')

def parse_part_2(html):
    try:
        pattern=re.compile('.*?&host_480=(.*?)&.*?&dir=(.*?)&.*?',re.S)
        result_2=re.search(pattern,html).group(1)
        result_3=re.search(pattern,html).group(2)
        result=result_2+'/'+result_3
        print('第一部分URL:'+result)
        return result
    except Exception:
        print('解析第一部分URL失败')

def parse_part_3(html):
    try:
        pattern=re.compile('.*?&stream_name=(.*?)&.*?',re.S)
        result_4=re.search(pattern,html).group(1)
        print('第二部分URL:'+'/'+result_4+'.mp4')
        return result_4
    except Exception:
        print('解析第二部分URL失败')

def download_video(url):
    try:
        print('准备下载视频:'+url)
        response=requests.get(url,headers=headers)
        data=response.content
        if data:
            file_path='{}/{}.{}'.format(os.getcwd(),md5(data).hexdigest(),'mp4')
            print('文件为:'+file_path)
            if not os.path.exists(file_path):
                with open(file_path,'wb')as f:
                    f.write(data)
                    f.close()
                    print('视频下载成功:'+url)
    except Exception:
        print('视频下载失败')

def main(url):
    try:
        print('视频初始URL:'+url)
        html=get_part(url)
        if html:
            flvid=parse_part_1(html)
            if flvid:
                url='http://play.baomihua.com/getvideourl.aspx?qudaoid=42&devicetype=pc%5Fplayer&flvid={}&Resolution=1'.format(flvid)
                html=get_part(url)
                if html:
                    base_url_1=parse_part_2(html)
                    url='http://play.baomihua.com/getvideourl.aspx?flvid={}&devicetype=phone_app_Android'.format(flvid)
                    html=get_part(url)
                    if html:
                        base_url_2=parse_part_3(html)
                        url='http://'+base_url_1+'/'+base_url_2+'.mp4'
                        print('视频下载URL:'+url)
                        download_video(url)
    except Exception:
        print('解析视频地址失败')

if __name__=='__main__':
    print('温馨提醒：e.g. http://www.baomihua.com/xxx/xxx'+'、'+'http://video.baomihua.com/v/xxx'+'...')
    url=input('请输入爆米花视频网址:')
    main(url)