import requests
from http.cookiejar import LWPCookieJar
import re
import time
from PIL import Image
import pytesseract

headers={
        'Referer':'https://www.zhihu.com/',
        'Origin':'https://www.zhihu.com/',
        'User-Agent':'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Mobile Safari/537.36'
    }
session=requests.session()
session.cookies=LWPCookieJar(filename='cookies.txt')
try:
    session.cookies.load(ignore_discard=True)
    print('Cookies已经存在')
except:
    print('Cookies尚未存在')

def get_xsrf():
    url='https://www.zhihu.com/signin?next=/'
    html=session.get(url=url,headers=headers).text
    pattern=re.compile('.*?<input type="hidden" name="_xsrf" value="(.*?)"/>', re.S)
    _xsrf=re.search(pattern,html).group(1)
    if _xsrf:
        print('_xsrf获取成功:'+ _xsrf)
        return _xsrf
    else:
        print('_xsrf获取失败')
#
# def get_captcha():
#     t=int(time.time()*1000)
#     url='https://www.zhihu.com/captcha.gif?r='+str(t)+'&type=login'
#     content=session.get(url=url,headers=headers).content
#     with open('captcha.jpg','wb') as f:
#         f.write(content)
#     im=Image.open('captcha.jpg')
#     im.show()
#     time.sleep(5)
#     im.close()
#     return input('请输入验证码:')


def get_captcha():
    t=int(time.time()*1000)
    url='https://www.zhihu.com/captcha.gif?r='+str(t)+'&type=login'
    content=session.get(url=url,headers=headers).content
    with open('captcha.jpg','wb') as f:
        f.write(content)
    im=Image.open('captcha.jpg')
    gray=im.convert('L')
    gray.show()
    threshold=150
    table=[]
    for i in range(256):
        if i < threshold:
            table.append(0)
        else:
            table.append(1)
    out=gray.point(table,'1')
    out.show()
    out.save('captcha_thresholded.jpg')
    th=Image.open('captcha_thresholded.jpg')
    print(pytesseract.image_to_string(th))
    return pytesseract.image_to_string(th)

def get_phonenum():
    return input('请输入手机号码:')

def get_password():
    return input('请输入密码:')

def isLogin():
    url='https://www.zhihu.com/settings/profile'
    response=session.get(url=url,headers=headers,allow_redirects=False)
    if response.status_code==200:
        print('登入成功')
        return True
    else:
        print('登入失败')
        return False

def login(phone_num,password,_xsrf,captcha):
        postdata={
            'phone_num':phone_num,
            'password':password,
            '_xsrf':_xsrf,
            'captcha':captcha,
        }
        url='https://www.zhihu.com/login/phone_num'
        response=session.post(url=url,data=postdata,headers=headers)
        if response.status_code==200:
            session.cookies.save(ignore_discard=True,ignore_expires=True)
            print('Cookies保存至本地成功')
        else:
            print('Cookies保存至本地失败')

if __name__=='__main__':
    if isLogin():
        print('您已经登入')
    else:
        phone_num=get_phonenum()
        password=get_password()
        _xsrf=get_xsrf()
        captcha=get_captcha()
        login(phone_num,password,_xsrf,captcha)


