from selenium import webdriver
# import json
import MySQLdb

conn=MySQLdb.connect(host='localhost',user='root',password='root',db='airbnb',charset='utf8')
cur=conn.cursor()

def parse_page(url):
    browser=webdriver.PhantomJS()
    browser.get(url)
    # print(browser.page_source)
    try:
        results=browser.find_elements_by_class_name('_1uyh6pwn')
        for result in results:
            price=result.find_element_by_css_selector('div._ij17et').text
            comment_count=result.find_element_by_css_selector('span._2a3fke5')
            if comment_count:
                comment_count=comment_count.text
            else:
                comment_count=None
            title=result.find_element_by_css_selector('span._1jhetorm').text
            detail=result.find_element_by_css_selector('span._j1kt73').text
            house_type=detail.split('·')[0]
            house_num=detail.split('·')[1]
            print(price,comment_count,title,house_type,house_num)
            sql="""INSERT INTO airbnb.taiguo_renting (price,title,comment_count,house_num,house_type)
VALUES (%s,%s,%s,%s,%s);"""
            cur.execute(sql,(price,title,comment_count,house_num,house_type))
            conn.commit()
            print('插入MySQL成功:'+title)
    finally:
        browser.close()

# def save_result(content):
#     with open('result.txt','a+',encoding='utf-8') as f:
#         f.write(json.dumps(content,ensure_ascii=False)+'\n')
#         f.close()

def main():
    for page in range(51):
        url = 'https://zh.airbnb.com/s/%E6%9B%BC%E8%B0%B7--%E6%B3%B0%E5%9B%BD/homes?place_id=ChIJ82ENKDJgHTERIEjiXbIAAQE&s_tag=jWgXRoL_&section_offset={}&allow_override%5B%5D='.format(page)
        parse_page(url)
    cur.close()
    conn.close()

if __name__=='__main__':
    main()