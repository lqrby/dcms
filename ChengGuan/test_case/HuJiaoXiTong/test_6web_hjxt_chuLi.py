# -*- coding: utf-8 -*-

import requests
from selenium import webdriver
import json
import re
import unittest
import urllib, sys, io
sys.path.append("E:/test/dcms/ChengGuan")
import time
from bs4 import BeautifulSoup
# import config
from config.Log import logging
sys.stdout = io.TextIOWrapper(sys.stdout.buffer,encoding='utf-8')
from common.constant_all import getConstant
from chengguan_authCode import test_login_authCode
from common.writeAndReadText import writeAndReadTextFile
# 权属单位登录--任晓华--renxiaohua:111111
def test_cg_login(driver):  #登录的方法
    loginResult = False
    authCode = test_login_authCode(driver) #获取验证码
    while authCode == "" :
        authCode = test_login_authCode(driver) 
    else:
        # time.sleep(1)
        driver.find_element_by_name('logonname').click()
        driver.find_element_by_name('logonname').send_keys(u"renxiaohua")
        time.sleep(1)
        driver.find_element_by_name('logonpassword').click()
        driver.find_element_by_name('logonpassword').send_keys(u"111111")
        time.sleep(1)
        driver.find_element_by_name('code').click()
        driver.find_element_by_name('code').send_keys(authCode)
        time.sleep(1)
        driver.find_element_by_xpath('//*[@id="logonForm"]/p/input').click()
        
        try:
            assert u"智慧化城市管理云平台" in driver.page_source, u"页面源码中不存在该关键字！"
        except AssertionError:
            print("断言验证错误")
            loginResult = test_cg_login(driver)
        else:
            print("登录后断言匹配正确")
            loginResult = BeautifulSoup(driver.page_source,'html.parser')
            cookiestr = writeAndReadTextFile().test_getCookie(driver)
            # print("cookiestr的类型是：",type(cookiestr))
            # 把cookie写入txt文件
            path = "E:/test/dcms/ChengGuan/common/cookie.txt"
            # print("cookiestr的类型是：：",type(cookiestr))
            writeAndReadTextFile().test_write_txt(path,cookiestr)
            # print("登录后的cookie是",cookiestr)
        # finally:
        #     print("断言验证错误，我依然被执行。")
       
    return loginResult

#查询待处理案卷列表    
def test_PendingList():
    # driver = webdriver.Chrome("D:/python/chromeDriverSever/chromedriver.exe")
    # test_cg_login(driver)
    cookies = writeAndReadTextFile().test_readCookies()
    dcl_url = getConstant.IP_WEB_180+"/dcms//cwsCase/Case-deallist.action?casestate=30&menuId=402880822f9490ad012f949be0e80053&keywords=402880eb2f90e905012f9138a5fb00a4"
    header = {
        "Cookie":cookies
    }
    respons = requests.get(url = dcl_url,headers=header).text
    # print("待处理列表",respons)
    return respons

#进入待处理案卷详情并处理
def test_handlingDetailsAndHandling():
    # 获取待处理列表
    res = test_PendingList()
    result = BeautifulSoup(res,'html.parser')
    divObj = result.find('div', attrs={'class':'mainContentTableContainer'})
    dcl_tr = divObj.findAll('table')[1].findAll('tr')[1]
    str_tr = str(dcl_tr)
    # print("res的类型是：",tables)
    number= re.compile('<span id="pagemsg" style="(.*?)"><label>总共(.*?)页,(.*?)条记录</label></span>').search(res).group(3)
    if int(number)>0:
        pattern = re.compile(r'<tr[\s\S]*id="(.*?)"[\s\S]*onclick="casedo[\(](.*?),(.*?),(.*?),(.*?),this[\)]">')
        dclid = pattern.search(str_tr).group(1)
        dcl_menuid = pattern.search(str_tr).group(2).strip("'")
        dcl_taskprocess = pattern.search(str_tr).group(5).strip("'")
        # 待处理详情url
        dclxq_url = getConstant.IP_WEB_180+"/dcms/cwsCase/Case-dealview.action?id="+dclid+"&menuId="+dcl_menuid+"&taskprocess="+dcl_taskprocess
        dclxq_cookies = writeAndReadTextFile().test_readCookies()
        header = {
           "Cookie":dclxq_cookies
        }
        dclxq_res = requests.get(url = dclxq_url,headers=header).text
        # print("待处理详情",dclxq_res)
        # -----------------------------------------------------------------
        cllist = writeAndReadTextFile().test_read_txt('E:/test/dcms/ChengGuan/testFile/chuLi/anjuanchuli.txt')
        cl_list = cllist.split(',')
        cl_taskcasestateid = re.compile('<input type="hidden" id="taskcasestateid" name="taskcasestateid" value="(.*?)"/>').search(dclxq_res).group(1)
        cl_casestate = re.compile('<input type="hidden" id="casestate" name="casestate" value="(.*?)" />').search(dclxq_res).group(1)
        cl_taskDeptID = re.compile('<input type="hidden" id="taskDeptID" name="taskDeptID" value="(.*?)" />').search(dclxq_res).group(1)
        cl_applyreturnlist = re.compile('<input type="hidden" id="applyreturnlist" name="applyreturnlist" value="(.*?)" />').search(dclxq_res).group(1)
        # 处理案卷url
        cl_url = getConstant.IP_WEB_180+"/dcms/cwsCase/Case-deal.action"
        cl_data = {
            "taskcasestateid":cl_taskcasestateid,
            "menuId":dcl_menuid,
            "casestate":cl_casestate,
            "id":dclid,
            "taskprocess":dcl_taskprocess,
            "taskDeptID":cl_taskDeptID,
            "resultprocess":cl_list[0],
            "applyreturnlist":cl_applyreturnlist,
            "operatingComments":cl_list[1],
            "upload":"",
            "dispatchDeptid":"",
            "dispatchDeptname":"",
            "limittime": "",
            "operatingComments_dis": "",
            "sentence": ""
        }
        cl_header = {
            "Cookie":dclxq_cookies
        }
        cl_result = requests.post(cl_url,cl_data,headers = cl_header).text
        print(cl_result)
        return cl_result
    else:
        print("待处理列表暂无数据！！！")







if __name__=="__main__": 
    test_handlingDetailsAndHandling()