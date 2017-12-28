import requests
import re
import time

exist_urls=[]
headers={
    'User-Agent':'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.62 Safari/537.36',
}
def scrapypy(url):
    try:
        response=requests.get(url=url,headers=headers)
        response.encoding='UTF-8'
        html=response.text
        link_lists=re.findall('.*?<a target=_blank href="/item/([^:#=<>]*?)".*?</a>',html)
        return link_lists
    except Exception as e:
        print(e)
        print('下载失败:'+url)
        return None
    finally:
        exist_urls.append(url)

def main(start_url,depth=1):
    count=0
    link_lists=scrapypy(start_url)
    if link_lists:
        unique_lists=list(set(link_lists)-set(exist_urls))
        for unique_list in unique_lists:
            unique_list='https://baike.baidu.com/item/'+unique_list
            count=count+1
            output='No.'+str(count)+'\t Depth:'+str(depth)+'\t'+start_url+'======>'+unique_list+'\n'
            print(output)
            with open('title.txt','a+') as f:
                f.write(output)
                f.close()
            if depth<2:
                main(unique_list,depth+1)

if __name__=='__main__':
    t1=time.time()
    start_url='https://baike.baidu.com/item/%E7%99%BE%E5%BA%A6%E7%99%BE%E7%A7%91'
    main(start_url)
    t2=time.time()
    print('总时间',t2-t1)



