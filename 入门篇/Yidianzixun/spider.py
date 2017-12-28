import requests
import time
from bs4 import BeautifulSoup
import csv
from selenium import webdriver

browser=webdriver.Chrome()
browser.get('https://www.yidianzixun.com/')
print('浏览器最大化')
browser.maximize_window()
time.sleep(10)
browser.find_element_by_css_selector('body > div.widget-tool > div.item.refresh.icon.iconfont.icon-refresh.anim').click()
for i in range(1,5):
    print('第%s次下拉'%i)
    browser.execute_script('window.scrollBy(0,1000)')
    time.sleep(15)
soup=BeautifulSoup(browser.page_source,'lxml')
results=soup.select('a.item.doc.style-small-image.style-content-middle')
contents=[]
for result in results:
    link='https://www.yidianzixun.com/'+result['href']
    title=result.select('div.doc-title')[0].text
    source=result.select('span.source')[0].text
    comment=result.select('span.comment-count')[0].text
    date=result.select('span.date')[0].text
    contents.append([link,title,source,comment[:-1],date])
    print(contents)
browser.close()
with open('result.csv','a') as f:
    writer=csv.writer(f)
    # writer.writerow=(['新闻链接','文章标题','信息来源','评论人数','发布时间'])
    for content in contents:
        writer.writerow(content)










