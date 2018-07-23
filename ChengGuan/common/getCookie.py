# -*- coding: utf-8 -*-
from selenium import webdriver
def test_getCookie(driver):
    #driver = webdriver.Chrome("D:/python/chromeDriverSever/chromedriver.exe")
    cookie = [item["name"] + "=" + item["value"] for item in driver.get_cookies()]  
    cookiestr = ';'.join(item for item in cookie) 
    print("============================cookie:",cookiestr)
    # r = open("E:/test/dcms/ChengGuan/common","a",encoding = "utf-8")
    return cookiestr

def test_readCookies():
    # path = "E:/test/dcms/ChengGuan/common/cookie.txt"
    with open("E:/test/dcms/ChengGuan/common/cookie.txt", 'r', encoding='utf8') as f:
        cookie_lines = f.readlines()
    return '\n'.join(cookie_lines)
# 写入txt
def test_write_txt(path_url,txt):
    f = open(path_url, 'w+')
    f.write(txt)
    f.close()

# 读取txt：
def test_read_txt(path):
    with open(path, 'r', encoding='utf8') as f:
        lines = f.readlines()
    return '\n'.join(lines)