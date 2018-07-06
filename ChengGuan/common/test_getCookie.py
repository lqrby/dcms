# -*- coding: utf-8 -*-
from selenium import webdriver
def test_getCookie(driver):
    #driver = webdriver.Chrome("D:/python/chromeDriverSever/chromedriver.exe")
    cookie = [item["name"] + "=" + item["value"] for item in driver.get_cookies()]  
    cookiestr = ';'.join(item for item in cookie) 
    print("============================cookie:",cookiestr)
    return cookiestr