# -*- coding: utf-8 -*-
from selenium import webdriver
import sys
sys.path.append("E:/test/dcms/ChengGuan")
from common.constant_all import getConstant
import ast
class writeAndReadTextFile():
    # 获取cookie并保持
    def test_getCookie(self,driver):
        cookie = [item["name"] + "=" + item["value"] for item in driver.get_cookies()]  
        cookiestr = ';'.join(item for item in cookie) 
        return cookiestr
    # 读取cookie
    def test_readCookies(self):
        with open(getConstant.PROJECT_PATH+"/common/cookie.txt", 'r', encoding='utf8') as f:
            cookie_lines = f.readlines()
        return '\n'.join(cookie_lines)
    # 写入txt
    def test_write_txt(self,path_url,txt):
        f = open(path_url, 'w+', encoding='utf-8')
        f.write(txt)
        f.close()

    # 读取txt：
    def test_read_txt(self,path):
        with open(path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        return '\n'.join(lines)
    # 读取app登录返回值
    def test_read_appLoginResult(self):
        result_path = getConstant.PROJECT_PATH+"/common/appLoginResult.txt"
        login_items = self.test_read_txt(result_path)
        loginitems = ast.literal_eval(login_items)
        return loginitems

    # 读取pc端登录返回值
    def test_read_systemId(self,systemName):
        webresult_path = getConstant.PROJECT_PATH+"/common/webLoginResult.txt"
        weblogin_items = self.test_read_txt(webresult_path)
        webloginitems = ast.literal_eval(weblogin_items)
        for item in webloginitems:
            if item['sysName'] == systemName:
                systemId = item['sysId']
        return systemId

    #读取mark标记
    def test_read_numberMark(self):
        markpath = getConstant.PROJECT_PATH+"/common/numberMark.txt"
        mark_items = self.test_read_txt(markpath)
        mark = ast.literal_eval(mark_items)
        return mark
