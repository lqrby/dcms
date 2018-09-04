# -*- coding: utf-8 -*-
import re
import unittest
import sys
sys.path.append("E:/test/dcms/ChengGuan")
import time
from config.Log import logging
from selenium import webdriver
from common.constant_all import getConstant
from login import allLogin
from jobEntry import submitOrder
from queRen import confirm
from heShi import verify
from liAn import setUpCase
from paiFa import distribution
from chuLi import fileFandling
from fuHeAndHuiFang import reviewAndReturnVisit
from common.writeAndReadText import writeAndReadTextFile

class MyTest2(unittest.TestCase):     #封装测试环境的初始化和还原的类  
    @classmethod
    def setUpClass(cls): #放对数据可操作的代码，如对mysql、momgodb的初始化等,这里不对数据库进行操作！  
        cls.driver = webdriver.Chrome("D:/python/chromeDriverSever/chromedriver.exe")
        logging.info("***打开浏览器***")
    

    #web端登录
    def test_1webLogin_lc3(self):
        webLogin = allLogin().test_web_login(self.driver)
        while webLogin==False:
            webLogin = allLogin().test_web_login(self.driver)
        logging.info("*****1.web端登录完毕*****")

    #移动端登录
    time.sleep(2)
    def test_2apkLogin_lc3(self):
        appLogin = allLogin().test_app_allLogin()
        while appLogin == False:
            appLogin = allLogin().test_app_allLogin()
        logging.info("*****2.移动端登录完毕*****")

    #移动端执法局上报案卷
    time.sleep(2)
    def test_3gongDan_lc3(self):
        loginItems = writeAndReadTextFile().test_read_appLoginResult()
        loginUser = loginItems['zfj']['user']#核实人
        dataObject = {}
        # dataObject['loginUser'] = loginUser
        dataObject['bgadminId'] = loginUser['id']
        dataObject['eorcId'] = getConstant.EORCID_SJ #案卷类型（事件）
        dataObject['mposl'] = "14090111.334314974"#经纬度
        dataObject['mposb'] = "5437565.851896823" 
        dataObject['description'] = "私搭乱建，违法建筑" #描述
        dataObject['eventtypeoneId'] = getConstant.SJ_SRHJ #大类  市容环境
        dataObject['eventtypetwoId'] = getConstant.SJ_SRHJ_SDLJ #小类 私搭乱建
        dataObject['gridId'] = '22021100200704' #万米网格
        # dataObject['regioncodeId'] = '220211' #丰满区
        # dataObject['bgcodeId'] = '220211002' #江南街道	
        
        dataObject['fieldintro'] = '吉林市 丰满区 江南街道 南山社区 南山社区第四网格 ' #位置描述
        # dataObject['needconfirm'] = getConstant.NEEDCONFIRM_YES #核实
        # dataObject['isFh'] = getConstant.ISFH_NO #回访
        zfj_res = submitOrder().test_app_submitOrder(dataObject)
        if zfj_res:
            logging.info("*****3.执法局上报案卷完毕*****")


    #web端立案   
    time.sleep(2)
    def test_4liAn_lc3(self):
        lian_result = setUpCase().test_detailsAndFiling()
        if lian_result:
            logging.info("*****4.web立案完毕*****")


    #web端派发 
    time.sleep(2)  
    def test_5paiFa_lc3(self):
        loginItemsUser = writeAndReadTextFile().test_read_appLoginResult()
        loginItem_qsdw = loginItemsUser['qsdw']['user']
        item = {}
        item['id'] = loginItem_qsdw['id']
        item["deptname"] = loginItem_qsdw['deptname']
        item["dispatchDeptname"] = loginItem_qsdw['deptname']
        item["deptid"] = loginItem_qsdw['deptid']
        paifa_result = distribution().test_sendDetailsAndSendOut(item)
        if paifa_result:
            logging.info("*****5.web派发完毕*****")

    # 处理 移动端权属单位apk处理
    time.sleep(2)    
    def test_6chuLi_lc3(self):
        loginItemsUser = writeAndReadTextFile().test_read_appLoginResult()
        loginItem_qsdw = loginItemsUser['qsdw']['user']
        qsdw_result = fileFandling().test_app_handlingDetailsAndHandling(loginItem_qsdw)
        if qsdw_result:
            logging.info("*****6.移动端权属单位处理完毕*****")

    # 复核 执法局复核
    time.sleep(2)    
    def test_7fuHe_lc3(self):
        loginItemsUser = writeAndReadTextFile().test_read_appLoginResult()
        fh_loginUser = loginItemsUser['zfj']['user']
        zfjfh_result = reviewAndReturnVisit().test_app_returnDetailsAndVisit(fh_loginUser)
        if zfjfh_result:
            logging.info("*****7.移动端执法局复核完毕*****")

    @classmethod
    def tearDownClass(cls): 
        cls.driver.quit()            #与setUp()相对y  
        logging.info("***关闭浏览器***")

if __name__=="__main__":
    unittest.main()