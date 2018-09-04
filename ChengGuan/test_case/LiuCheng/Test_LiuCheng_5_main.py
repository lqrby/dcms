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


class MyTest(unittest.TestCase):     #封装测试环境的初始化和还原的类  
    @classmethod
    def setUpClass(cls): #放对数据可操作的代码，如对mysql、momgodb的初始化等,这里不对数据库进行操作！  
        cls.driver = webdriver.Chrome("D:/python/chromeDriverSever/chromedriver.exe")
        logging.info("***打开浏览器***")
    

    #web端登录
    def test_1webLogin_lc5(self):
        webLogin = allLogin().test_web_login(self.driver)
        while webLogin==False:
            webLogin = allLogin().test_web_login(self.driver)
        logging.info("*****1.web端登录完毕*****")

    #移动端登录
    time.sleep(2)
    def test_2apkLogin_lc5(self):
        appLogin = allLogin().test_app_allLogin()
        while appLogin == False:
            appLogin = allLogin().test_app_allLogin()
        logging.info("*****2.移动端登录完毕*****")

    #移动端执法局巡检上报案卷
    time.sleep(2)
    def test_3gongDan_lc5(self):
        xjsb_res = submitOrder().test_app_reportInspection()
        if xjsb_res:
            logging.info("*****3.执法局巡检上报案卷完毕*****")

    #web端确认案卷
    time.sleep(2)
    def test_4queRen_lc5(self):
        loginItems = writeAndReadTextFile().test_read_appLoginResult()
        loginUser = loginItems['wggly']['user']#核实人
        dataObject = {}
        dataObject['loginUser'] = loginUser
        dataObject['eorcId'] = getConstant.EORCID_SJ #事件
        dataObject['eventtypeoneId'] = getConstant.SJ_XCGG #大类
        dataObject['eventtypetwoId'] = getConstant.SJ_XCGG_FFXGG #小类
        dataObject['regioncodeId'] = '220206' #高新开发区
        dataObject['bgcodeId'] = '220206001' #高新开发区街道	
        # dataObject['gridId'] = '22020600100706' #万米网格
        # dataObject['fieldintro'] = '吉林市 高新开发区 高新开发区街道 日升社区 日升社区第六网格' #位置描述
        dataObject['needconfirm'] = getConstant.NEEDCONFIRM_YES #核实
        dataObject['isFh'] = getConstant.ISFH_NO #回访
        webqueren_res = confirm().test_web_UnconfirmedDetail(dataObject)
        if webqueren_res:
            logging.info("*****4.web确认案卷完毕*****")


    #移动端网格管理员核实案卷
    time.sleep(2)
    def test_5heShi_lc2(self):
        loginItems = writeAndReadTextFile().test_read_appLoginResult()
        loginItem_hs = loginItems['wggly']['user']
        zfjhs_res = verify().test_app_wggly_daiHeShiDetail(loginItem_hs)
        if zfjhs_res:
            logging.info("*****5.网格管理员核实案卷完毕*****")

    #web端立案   
    time.sleep(2)
    def test_6liAn_lc5(self):
        lian_result = setUpCase().test_detailsAndFiling()
        if lian_result:
            logging.info("*****6.web立案完毕*****")

    #web端派发 
    time.sleep(2)  
    def test_7paiFa_lc5(self):
        loginItemsUser = writeAndReadTextFile().test_read_appLoginResult()
        loginItem_qsdw = loginItemsUser['qsdw']['user']
        item = {}
        item['id'] = loginItem_qsdw['id']
        item["deptname"] = loginItem_qsdw['deptname']
        item["dispatchDeptname"] = loginItem_qsdw['deptname']
        item["deptid"] = loginItem_qsdw['deptid']
        paifa_result = distribution().test_sendDetailsAndSendOut(item)
        if paifa_result:
            logging.info("*****7.web端派发完毕*****")

    # 处理 移动端权属单位apk处理
    time.sleep(2)    
    def test_8chuLi_lc5(self):
        loginItems = writeAndReadTextFile().test_read_appLoginResult()
        qsdwItem = loginItems['qsdw']['user']
        qsdw_result = fileFandling().test_app_handlingDetailsAndHandling(qsdwItem)
        if qsdw_result:
            logging.info("*****8.移动端权属单位处理完毕*****")

    # web回访 
    time.sleep(2)    
    def test_9fuHe_lc5(self):
        zfjfh_result = reviewAndReturnVisit().test_returnDetailsAndVisit()
        if zfjfh_result:
            logging.info("*****9.web端回访完毕*****")

    @classmethod
    def tearDownClass(cls): 
        cls.driver.quit()            #与setUp()相对y  
        logging.info("***关闭浏览器***")

if __name__=="__main__":
    unittest.main()