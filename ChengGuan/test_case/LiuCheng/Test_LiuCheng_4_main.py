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
    def test_1webLogin_lc4(self):
        webLogin = allLogin().test_web_login(self.driver)
        while webLogin==False:
            webLogin = allLogin().test_web_login(self.driver)
        logging.info("*****1.web端登录完毕*****")

    #移动端登录
    time.sleep(2)
    def test_2apkLogin_lc4(self):
        appLogin = allLogin().test_app_allLogin()
        while appLogin == False:
            appLogin = allLogin().test_app_allLogin()
        logging.info("*****2.移动端登录完毕*****")

    #移动端网格管理员上报案卷
    time.sleep(2)
    def test_3gongDan_lc4(self):
        
        results = writeAndReadTextFile().test_read_appLoginResult()
        markPath = getConstant.PROJECT_PATH+"/common/numberMark.txt"
        mark = writeAndReadTextFile().test_read_txt(markPath)
        number = int(mark)+1
        sb_dataObject = {}
        sb_dataObject['loginUser'] = results['wggly']['user']
        sb_dataObject['eorcId'] = getConstant.EORCID_SJ #案件类型
        sb_dataObject['eventtypeoneId'] = getConstant.SJ_SRHJ #大类
        sb_dataObject['eventtypetwoId'] = getConstant.SJ_SRHJ_DLBJ #小类
        sb_dataObject['description'] = str(number)+"道理不干净，环境脏乱差"
        sb_dataObject['fieldintro'] = "吉林市 高新开发区 高新开发区街道 恒厦社区 恒厦社区第九网格"
        sb_dataObject['gridid'] = "22020600100109"
        sb_dataObject['mposl'] = "14088524.212997204"
        sb_dataObject['mposb'] = "5437559.658689937"
        sb_dataObject['needconfirm'] = getConstant.NEEDCONFIRM_YES #是否核实
        sb_dataObject['isFh'] = getConstant.ISFH_NO #是否复核 
        writeAndReadTextFile().test_write_txt(markPath,str(number))
        wggly_res = submitOrder().test_app_submitOrder(sb_dataObject)
        if wggly_res:
            logging.info("*****3.网格管理员上报案卷完毕*****")


    #web端立案   
    time.sleep(2)
    def test_4liAn_lc4(self):
        lian_result = setUpCase().test_detailsAndFiling()
        if lian_result:
            logging.info("*****4.web立案完毕*****")

    #web端派发 
    time.sleep(2)  
    def test_5paiFa_lc4(self):
        loginItemsUser = writeAndReadTextFile().test_read_appLoginResult()
        loginItem_qsdw = loginItemsUser['zfj']['user']
        item = {}
        item['id'] = loginItem_qsdw['id']
        item["deptname"] = loginItem_qsdw['deptname']
        item["dispatchDeptname"] = loginItem_qsdw['deptname']
        item["deptid"] = loginItem_qsdw['deptid']
        paifa_result = distribution().test_sendDetailsAndSendOut(item)
        if paifa_result:
            logging.info("*****5.web端派发完毕*****")

    # 处理 移动端执法局apk处理
    time.sleep(2)    
    def test_6chuLi_lc4(self):
        loginItemsUser = writeAndReadTextFile().test_read_appLoginResult()
        loginItem_qsdw = loginItemsUser['zfj']['user']
        qsdw_result = fileFandling().test_app_handlingDetailsAndHandling(loginItem_qsdw)
        if qsdw_result:
            logging.info("*****6.移动端执法局处理完毕*****")

    # 复核 
    time.sleep(2)    
    def test_7fuHe_lc4(self):
        loginItemsUser = writeAndReadTextFile().test_read_appLoginResult()
        fh_loginUser = loginItemsUser['wggly']['user']
        fh_result = reviewAndReturnVisit().test_app_returnDetailsAndVisit(fh_loginUser)
        if fh_result:
            logging.info("*****7.移动端网格管理员复核完毕*****")

    @classmethod
    def tearDownClass(cls): 
        cls.driver.quit()            #与setUp()相对y  
        logging.info("***关闭浏览器***")

if __name__=="__main__":
    unittest.main()