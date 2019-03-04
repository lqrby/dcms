# -*- coding: utf-8 -*-
import unittest
import sys
sys.path.append("E:/test/dcms/ChengGuan")
import time,random,json
import threading
from config.Log import logging
from selenium import webdriver
from login import allLogin
from jobEntry import submitOrder
from queRen import confirm
from heShi import verify
from liAn import setUpCase
from paiFa import distribution
from guaZhang import hangUp
from chuLi import fileFandling
from fuHeAndHuiFang import reviewAndReturnVisit
from common.writeAndReadText import writeAndReadTextFile
from common.constant_all import getConstant

class MyTest(unittest.TestCase):     #封装测试环境的初始化和还原的类  
    @classmethod
    def setUpClass(cls): #放对数据可操作的代码，如对mysql、momgodb的初始化等,这里不对数据库进行操作！  
        # 初始化移动端登录人员集合对象
        cls.loginItems = writeAndReadTextFile().test_read_appLoginResult()
        #获取cookies
        cls.cookies = writeAndReadTextFile().test_readCookies()
    
    
    #web端工单录入
    def gongDan(self):
        time.sleep(random.randint(2,4))
        markPath = getConstant.PROJECT_PATH+"/common/numberMark.txt"
        mark = writeAndReadTextFile().test_read_txt(markPath)
        dict_mark = json.loads(mark)
        number = int(dict_mark['web_sb'])+1
        orderData = {}
        picpath = "E:/test/dcms/ChengGuan/testFile/img/1.png"
        img_value = ('1.png', open(picpath,'rb'),'multipart/form-data')
        orderData['mposl'] = '14088659.985423975'
        orderData['mposb'] = '5442040.762812978'
        orderData['menuId'] = '402880822f9490ad012f949eb313008a'
        orderData['isFh'] = '1'
        orderData['street'] = '220204002'
        orderData['p_name'] = '董楚楚'
        orderData['p_sex'] = '女'
        orderData['p_job'] = '教师'
        orderData['p_phone'] = '0102864987'
        orderData['other_phone'] = '15866993322'
        orderData['feedback'] = '手机'
        orderData['source'] = '402880822f47692b012f4774e5710010'
        orderData['eorc'] = getConstant.EORCID_SJ   #案卷类型
        orderData['eventtypeone'] = getConstant.SJ_XCGG   #事件大类
        orderData['eventtypetwo'] = getConstant.SJ_XCGG_FFXGG  #小类
        orderData['regioncode'] = '220204'
        orderData['bgcode'] = '220204002'
        orderData['bgadminid'] = self.loginItems['wggly']['user']['id']
        orderData['bgadminid2'] = self.loginItems['wggly']['user']['name']
        orderData['gridid'] = '220204002003'
        orderData['needconfirm'] = '0'
        orderData['description'] = '流程一，非法小广告'+str(number)
        orderData['dealWay'] = 'on'
        orderData['fieldintro'] = '吉林市 船营区 南京街道 怀德社区'
        orderData['upload'] = img_value
        gdlr_res = submitOrder(orderData).test_web_submitOrder()
        if gdlr_res:
            dict_mark["web_sb"] = str(number)
            writeAndReadTextFile().test_write_txt(markPath,json.dumps(dict_mark))
            logging.info("3.web工单录入完毕")

    # #web端立案
    def liAn(self):
        time.sleep(random.randint(1,3)) 
        lianData = {}
        lianData['resultprocess'] = "立案"
        lianData['operatingComments'] = "批准立案"
        lian_result = setUpCase(lianData).test_detailsAndFiling()
        if lian_result:
            logging.info("4.web立案完毕")
        else:
            logging.info("XXXXXXXXXXXXXXXX4.web立案失败XXXXXXXXXXXXXXX")


    # #web端待派发》挂起
    def guaQi(self):
        time.sleep(random.randint(1,2))  
        pf_loginItem = self.loginItems['qsdw']['user']
        outDir = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        pf_loginItem['resultprocess'] = "挂账"
        pf_loginItem['limittime'] = outDir
        pf_loginItem['operatingComments'] = "先挂起，暂时不知道派发部门"
        #待派发列表url
        pf_loginItem['pflist_url'] = getConstant.dpf_ListUrl
        #派发url
        pf_loginItem['pf_url'] = getConstant.pf_url
        paifa_result = distribution(pf_loginItem).test_sendDetailsAndSendOut()
        if paifa_result:
            logging.info("5.web挂起完毕")

    #挂账》恢复
    def huiFu(self):
        time.sleep(random.randint(1,2)) 
        gzItem = {}
        gzItem['resultprocess'] = '恢复'
        gzItem['operatingComments'] = '恢复案卷流程'
        gz_res = hangUp(gzItem).test_hangUpDetail()
        if gz_res ==True:
            logging.info("6.web挂账案卷恢复成功")

    # #web端派发
    def paiFa(self):
        time.sleep(random.randint(1,2))  
        pf_loginItem = self.loginItems['qsdw']['user']
        outDir = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        pf_loginItem['resultprocess'] = "派发"
        pf_loginItem['limittime'] = outDir
        pf_loginItem['operatingComments'] = "尽快处理"
        #待派发列表url
        pf_loginItem['pflist_url'] = getConstant.dpf_ListUrl
        #派发url
        pf_loginItem['pf_url'] = getConstant.pf_url
        paifa_result = distribution(pf_loginItem).test_sendDetailsAndSendOut()
        if paifa_result:
            logging.info("7.web派发完毕")

    # 处理 移动端权属单位apk处理 
    def chuLi(self):
        time.sleep(random.randint(1,2)) 
        cl_loginItem = self.loginItems['qsdw']['user']
        cl_loginItem['resultprocess'] = '处理结束'
        cl_loginItem['operatingComments'] = '处理完成1'
        cl_picpath1 = "E:/test/dcms/ChengGuan/testFile/img/9.png"
        cl_picpath2 = "E:/test/dcms/ChengGuan/testFile/img/28.png"
        cl_loginItem['imgPath'] = [cl_picpath1,cl_picpath2]
        cl_result = fileFandling(cl_loginItem).test_app_handlingDetailsAndHandling()
        if cl_result:
            logging.info("8.移动端权属单位处理完毕")

    # 复核 网格管理员apk复核 
    def fuHe(self):
        time.sleep(random.randint(1,3)) 
        fh_picpath1 = "E:/test/dcms/ChengGuan/testFile/img/6.png"
        fh_picpath2 = "E:/test/dcms/ChengGuan/testFile/img/7.png"
        fh_loginUser = self.loginItems['wggly']['user']
        fh_loginUser['checkdesc'] = '经复核有效'
        fh_loginUser['imgPath'] = [fh_picpath1,fh_picpath2]
        fh_result = reviewAndReturnVisit(fh_loginUser).test_app_returnDetailsAndVisit()
        if fh_result:
            logging.info("9.移动端网格管理员复核完毕")
    
    def test_liucheng_1(self):
        for i in range(1):
            self.gongDan()
            self.liAn()
            self.guaQi()
            self.huiFu()
            self.paiFa()
            self.chuLi()
            self.fuHe()
    @classmethod
    def test_tearDownClass(cls): 
        # cls.driver.quit()            #与setUp()相对y  
        logging.info("***流程结束***")

if __name__=="__main__":
    
    unittest.main()
    
    