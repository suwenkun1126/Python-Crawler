import requests
import json

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

province_list=['江苏省','浙江省','广东省','福建省','山东省','河南省','河北省','四川省','辽宁省','云南省','湖南省',
               '湖北省','江西省','安徽省','山西省','广西壮族自治区','陕西省','黑龙江省','内蒙古自治区','贵州省','吉林省',
               '甘肃省','新疆维吾尔自治区','海南省','宁夏回族自治区','青海省','西藏自治区']
for each in province_list:
    decodejson=getjson(each)
    for eachcity in decodejson.get('results'):
        city=eachcity.get('name')
        num=eachcity.get('num')
        output='\t'.join([city,str(num)])+'\n'
        print(output)
        with open('cities.txt','a+',encoding='UTF-8') as f:
            f.write(output)
            f.close()

