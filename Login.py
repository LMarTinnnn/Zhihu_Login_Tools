from config import headers
import config
import requests
from bs4 import BeautifulSoup
import time
from Common_Crawler_helper.SoupRefiner import SoupRefiner

class ZhihuLogIn(object):
    def __init__(self):
        self.homepage = 'https://www.zhihu.com'
        self.login_url = 'https://www.zhihu.com/login/email'
        self.session = requests.session()
        self.soup = self.get_soup()
        self._xsrf = self.get_xsrf()
        print('_xsrf: ' +self._xsrf)

    def get_soup(self):
        # 获取soup的时候不应该访问login_in时 的post url
        # 而是访问主页！！！
        html = self.session.get(self.homepage, headers=headers, proxies=config.proxies).text
        soup = BeautifulSoup(html, 'lxml')
        return soup

    def get_xsrf(self):
        xrsf = self.soup.find('input')['value']
        return xrsf

    def get_captcha(self):
        captcha_url = 'https://www.zhihu.com/captcha.gif?r=%s' % int(time.time() * 1000)
        pic = self.session.get(captcha_url, headers=headers, proxies=config.proxies).content
        with open('captcha.jpg', 'wb') as f:
            f.write(pic)

    def log_in(self):
        self.get_captcha()
        #email = input('Email: ')
        #password = input('Password: ')
        email = '442669793@qq.com'
        password = 'lyb97427'
        captcha = input('请在当前目录下寻找captcha.jpg: ')
        data = {
            'email': email,
            'password': password,
            'captcha': captcha,
            '_xsrf': self._xsrf,
            'remember_me': 'true'
        }

        response = self.session.post(self.login_url, data=data, headers=headers, proxies=config.proxies)
        print(response.json())
        html = self.session.get('https://www.zhihu.com', headers=headers).text
        soup = BeautifulSoup(html, 'lxml')
        sr = SoupRefiner(soup, 'https://www.zhihu.com')
        for link in sr.get_internal_links():
            print(link)

if __name__ == '__main__':
    z = ZhihuLogIn()
    z.log_in()
