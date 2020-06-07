# -*- coding: utf-8 -*-

"""
Created on 2020-03-26 13:55

@author: congyingxu
"""

import sys

sys.path.append('../')  # 新加入的

import json
import time
import selenium
from selenium import webdriver
from selenium.webdriver.firefox.options import Options


# Chorme
# 关闭提示 "Chorme正在收到自动软件的控制"
# option = webdriver.ChromeOptions()
# option.add_argument('disable-infobars')
# 后台显示，前端不显示
# option.add_argument('headless')
# browser = webdriver.Chrome('/Users/congyingxu/Documents/chromedriver', chrome_options=option)


class ChromeBrowser:
    browser = ''
    profile = ''
    options = ''

    def __init__(self):
        # self.setprofile()
        self.setOptions()
        self.creatbrowser()
        self.setTomeout()

    def setprofile(self):
        self.profile = webdriver.FirefoxProfile()
        # proxy = '42.51.13.68:16816'
        # ip, port = proxy.split(":")
        # port = int(port)
        # # 不使用代理的协议，注释掉对应的选项即可
        # settings = {
        #     'network.proxy.type': 0,  # 0: 不使用代理；1: 手动配置代理
        #     'network.proxy.http': ip,
        #     'network.proxy.http_port': port,
        #     'network.proxy.ssl': ip,  # https的网站,
        #     'network.proxy.ssl_port': port,
        # }
        # 更新配置文件
        # for key, value in settings.items():
        #     profile.set_preference(key, value)
        # profile.update_preferences()

        settings = {
            'network.proxy.type': 0  # 0: 不使用代理；1: 手动配置代理
        }
        # 更新配置文件
        for key, value in settings.items():
            self.profile.set_preference(key, value)
        self.profile.update_preferences()

    def setOptions(self):
        # 设定页面加载限制时间
        self.options = webdriver.ChromeOptions()
        self.options.add_argument('disable-infobars')
        # 后台运行，前端不显示
        self.options.add_argument('--headless')
        # 解决证书信任问题
        self.options.add_argument("service_args=[’–ignore-ssl-errors=true’, ‘–ssl-protocol=TLSv1’]")

    def creatbrowser(self):
        self.driver_path = '/Users/congyingxu/Documents/chromedriver'
        self.browser = webdriver.Chrome(executable_path=self.driver_path, chrome_options = self.options)

        # time.sleep(60)
        self.browser.get("https://www.baidu.com")
        # time.sleep(60)

    def setTomeout(self):
        self.browser.set_page_load_timeout(100)
        # 如果10秒内没有加载完成就会报错
        # selenium.common.exceptions.TimeoutException: Message: timeout: Timed out receiving message from renderer: 1.684

        # # 新开一个窗口，通过执行js来新开一个窗口
        # js = 'window.open("https://www.sogou.com");'
        # browser.execute_script(js)
        pass


browser = ChromeBrowser().browser


def getHtmlFromUrl(url):
    global browser

    try:
        browser.get(url)
        pageSource = browser.page_source
        html = pageSource.encode("utf-8", "ignore")
        title = browser.title
    except selenium.common.exceptions.TimeoutException:
        print("TimeoutException")
        time.sleep(10)

        restart()

        browser.get(url)
        pageSource = browser.page_source
        html = pageSource.encode("utf-8", "ignore")
        title = browser.title

    return html, title


def getHttpStatus(browser):
    for responseReceived in browser.get_log('performance'):
        try:
            response = json.loads(responseReceived[u'message'])[u'message'][u'params'][u'response']
            if response[u'url'] == browser.current_url:
                return (response[u'status'], response[u'statusText'])
        except:
            pass
    return None


def quitCrawler():
    global browser
    browser.quit()


def restart():
    global browser
    print("restart")
    quitCrawler()
    browser = ChromeBrowser().browser