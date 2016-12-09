from config import headers
import requests
from bs4 import BeautifulSoup
import time
import os


class ZhihuLogIn(object):
    """
    知乎登录助手
    ~~~~~~~~~~

    Usage:
    z = ZhihuLogIn()
    session = z.login()
    """
    def __init__(self):
        self.homepage = 'https://www.zhihu.com'
        self.login_url = 'https://www.zhihu.com/login/email'
        self.session = requests.session()
        self.soup = self.get_soup()
        self._xsrf = self.get_xsrf()
        print('_xsrf: ' + self._xsrf)

    def get_soup(self):
        # 获取soup的时候不应该访问login_in时 的post url
        # 而是访问主页！！！
        html = self.session.get(self.homepage, headers=headers,).text
        soup = BeautifulSoup(html, 'lxml')
        return soup

    # xsrf 用于防止跨站攻击
    def get_xsrf(self):
        xrsf = self.soup.find('input')['value']
        return xrsf

    def get_captcha(self):
        # 注意后面的参数 int(time.time() * 1000)
        captcha_url = 'https://www.zhihu.com/captcha.gif?r=%s' % int(time.time() * 1000)
        pic = self.session.get(captcha_url, headers=headers).content
        if not os.path.exists('./captcha'):
            os.mkdir('./captcha')
        with open('./captcha/captcha.jpg', 'wb') as f:
            f.write(pic)

    def log_in(self):
        """

        :return: 返回一个已经登录的知乎session
        """
        self.get_captcha()
        email = input('Email: ')
        password = input('Password: ')
        captcha = input('请在captcha目录下寻找captcha.jpg: ')
        data = {
            'email': email,
            'password': password,
            'captcha': captcha,
            '_xsrf': self._xsrf,
            'remember_me': 'true'
        }

        json_res = self.session.post(self.login_url, data=data, headers=headers).json()
        if json_res['msg'] == '登录成功':
            return self.session
        else:
            return None

        # html = self.session.get('https://www.zhihu.com', headers=headers).text
        # soup = BeautifulSoup(html, 'lxml')
        # sr = SoupRefiner(soup, 'https://www.zhihu.com')
        # for link in sr.get_external_links():
        #   print(link)

if __name__ == '__main__':
    z = ZhihuLogIn()
    print(type(z.log_in()))
    # <class 'requests.sessions.Session'>
