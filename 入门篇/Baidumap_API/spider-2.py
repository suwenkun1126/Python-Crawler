import requests
import json
import MySQLdb
from datetime import datetime

city_list=[]
with open('cities.txt','r',encoding='utf-8') as f:
    for eachline in f:
        if eachline !='' and eachline !='\n':
            city=eachline.split('\t')[0]
            city_list.append(city)
    f.close()

def getjson(palace,page_num=0):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
    }
    url='http://api.map.baidu.com/place/v2/search'
    params={
        'q':'公园',
        'region':palace,
        'scope':'2',
        'page_size':'20',
        'page_num':page_num,
        'output':'json',
        'ak':'XM53LMurtNQaAPFuKVy1WzSyZCNmNA9H',
    }
    response=requests.get(url=url,params=params,headers=headers)
    html=response.text
    decodejson=json.loads(html)
    return decodejson

conn=MySQLdb.connect(host='localhost',user='root',password='root',db='baidumap',charset='utf8')
cur=conn.cursor()
for city in city_list:
    not_last_page=True
    page_num=0
    while not_last_page:
        decodejson=getjson(city,page_num)
        print(city,page_num)
        if decodejson.get('results'):
            for result in decodejson.get('results'):
                park=result.get('name')
                lat=result.get('location').get('lat')
                lng=result.get('location').get('lng')
                address=result.get('address')
                street_id=result.get('street_id')
                uid=result.get('uid')
                sql="""INSERT INTO baidumap.city 
(city,park,location_lat,location_lng,address,street_id,uid,time)
VALUES (%s,%s,%s,%s,%s,%s,%s,%s);"""
                cur.execute(sql,(city,park,lat,lng,address,street_id,uid,datetime.now()))
                conn.commit()
            page_num=page_num+1
        else:
            not_last_page=False
cur.close()
conn.close()

