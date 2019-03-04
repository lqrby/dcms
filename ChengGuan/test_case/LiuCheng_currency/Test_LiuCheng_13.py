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
from tiaoZhengPiSi import adjustmentApproval
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
        orderData['isFh'] = getConstant.ISFH_YES
        orderData['street'] = '220204002'
        orderData['p_name'] = '董楚楚'
        orderData['p_sex'] = '女'
        orderData['p_job'] = '教师'
        orderData['p_phone'] = '0102864987'
        orderData['other_phone'] = '15866993322'
        orderData['feedback'] = '手机'
        orderData['source'] = '402880822f47692b012f4774e5710010'
        orderData['eorc'] = getConstant.EORCID_BJ   #案卷类型
        orderData['eventtypeone'] = getConstant.BJ_SRHJ   #事件大类
        orderData['eventtypetwo'] = getConstant.BJ_SRHJ_LJX #小类
        orderData['regioncode'] = '220204'
        orderData['bgcode'] = '220204002'
        orderData['bgadminid'] = self.loginItems['zfj']['user']['id']
        orderData['bgadminid2'] = self.loginItems['zfj']['user']['name']
        orderData['gridid'] = '220204002003'
        orderData['needconfirm'] = getConstant.NEEDCONFIRM_YES
        orderData['description'] = '流程十三，执法局核实、复核'+str(number)
        orderData['dealWay'] = 'on'
        orderData['fieldintro'] = '吉林市 船营区 南京街道 怀德社区'
        orderData['upload'] = img_value
        gdlr_res = submitOrder(orderData).test_web_submitOrder()
        if gdlr_res:
            dict_mark["web_sb"] = str(number)
            writeAndReadTextFile().test_write_txt(markPath,json.dumps(dict_mark))
            logging.info("*****2.web工单录入完毕*****")
        else:
            logging.info("XXXXXXXXXXX2.web工单录入完毕XXXXXXXXXX")

    #执法局核实案卷(移动端)
    def heShi(self):
        time.sleep(random.randint(1,2))
        loginItem_hs = self.loginItems['zfj']['user']
        hs_picpath1 = "E:/test/dcms/ChengGuan/testFile/img/10.png"
        hs_picpath2 = "E:/test/dcms/ChengGuan/testFile/img/11.png"
        loginItem_hs['imgPath'] = [hs_picpath1,hs_picpath2]
        loginItem_hs['casestateid'] = getConstant.HSYX
        hs_res = verify(loginItem_hs).test_app_daiHeShiDetail()
        if hs_res:
            logging.info("*****3.执法局核实案卷完毕*****")
        else:
            logging.info("XXXXXXXXXX3.执法局核实案卷出错XXXXXXXXXXX")


    # #web端立案
    def liAn(self):
        time.sleep(random.randint(1,3)) 
        lianData = {}
        lianData['resultprocess'] = "立案"
        lianData['operatingComments'] = "批准立案"
        lian_result = setUpCase(lianData).test_detailsAndFiling()
        if lian_result:
            logging.info("*****4.web立案完毕*****")
        else:
            logging.info("XXXXXXXXXXXX4.web立案失败XXXXXXXXXXXX")


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
            logging.info("*****5.web派发完毕*****")
        else:
            logging.info("XXXXXXXXX5.web派发完毕XXXXXXXXX*")

    # 处理 权属单位apk处理(移动端)
    def chuLi(self):
        time.sleep(random.randint(1,2)) 
        cl_loginItem = self.loginItems['qsdw']['user']
        cl_loginItem['resultprocess'] = '处理结束'
        cl_loginItem['operatingComments'] = '处理完成'
        cl_picpath1 = "E:/test/dcms/ChengGuan/testFile/img/31.png"
        cl_picpath2 = "E:/test/dcms/ChengGuan/testFile/img/30.png"
        cl_loginItem['imgPath'] = [cl_picpath1,cl_picpath2]
        result = fileFandling(cl_loginItem).test_app_handlingDetailsAndHandling()
        if result:
            logging.info("*****6.移动端权属单位处理完毕*****")
        else:
            logging.info("XXXXXXXXX6.移动端权属单位处理失败XXXXXXXXX")

    
    # 复核 执法局apk复核 
    def fuHe(self):
        time.sleep(random.randint(1,3)) 
        fh_picpath1 = "E:/test/dcms/ChengGuan/testFile/img/16.png"
        fh_picpath2 = "E:/test/dcms/ChengGuan/testFile/img/17.png"
        fh_picpath3 = "E:/test/dcms/ChengGuan/testFile/img/12.png"
        fh_loginUser = self.loginItems['zfj']['user']
        fh_loginUser['checkdesc'] = '经复核有效'
        fh_loginUser['imgPath'] = [fh_picpath1,fh_picpath2,fh_picpath3]
        fh_result = reviewAndReturnVisit(fh_loginUser).test_app_returnDetailsAndVisit()
        if fh_result:
            logging.info("*****7.移动端网格管理员复核完毕*****")
        else:
            logging.info("XXXXXXXXXXXXX7.移动端网格管理员复核出现问题XXXXXXXXXXXXXX")

    def test_liucheng_1(self):
        for i in range(1):
            self.gongDan()
            self.heShi()
            self.liAn()
            self.paiFa()
            self.chuLi()
            self.fuHe()
    
    @classmethod
    def tearDownClass(cls): 
        logging.info("***流程结束***")

if __name__=="__main__":
    unittest.main()
    
    