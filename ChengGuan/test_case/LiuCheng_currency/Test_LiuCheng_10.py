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
from piSi import Approval
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
    def test_03gongDan(self):
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
        orderData['description'] = '流程十，调整批示'+str(number)
        orderData['dealWay'] = 'on'
        orderData['fieldintro'] = '吉林市 船营区 南京街道 怀德社区'
        orderData['upload'] = img_value
        gdlr_res = submitOrder(orderData).test_web_submitOrder()
        if gdlr_res:
            dict_mark["web_sb"] = str(number)
            writeAndReadTextFile().test_write_txt(markPath,json.dumps(dict_mark))
            logging.info("*****3.web工单录入完毕*****")

    # #web端立案
    def test_04liAn(self):
        time.sleep(random.randint(1,3)) 
        lianData = {}
        lianData['resultprocess'] = "立案"
        lianData['operatingComments'] = "批准立案"
        lian_result = setUpCase(lianData).test_detailsAndFiling()
        if lian_result:
            logging.info("*****4.web立案完毕*****")
        else:
            logging.info("*****4.web立案失败*****")


    # #web端派发
    def test_05paiFa(self):
        time.sleep(random.randint(1,2))  
        pf_loginItem = self.loginItems['zfj']['user']
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

    # 申请调整 移动端权属单位apk申请调整
    def test_06chuLi(self):
        time.sleep(random.randint(1,2)) 
        cl_loginItem = self.loginItems['zfj']['user']
        cl_loginItem['resultprocess'] = '申请调整'   #不可更改
        cl_loginItem['operatingComments'] = '请求调整'  #
        cl_loginItem['applyReason'] = '非我辖区'  #调整原因
        cl_result = fileFandling(cl_loginItem).test_requestAdjustment()
        if cl_result:
            logging.info("*****6.移动端权属单位申请调整成功*****")

    
    #调整批示    
    def test_07tiaoZhengPiShi(self):
        time.sleep(random.randint(1,2)) 
        dataItem = {}
        dataItem['resultprocess'] = "批准"
        dataItem['leaderComments'] = "批准了"
        tzpsOK = adjustmentApproval(dataItem).adjustmentApprovalDetail()
        if tzpsOK != False:
            logging.info("*****7.web端调整批示成功(%s)*****"%dataItem['resultprocess'])

    # #web端派发>申请非正常结案
    def test_08feiZhengChangJieAn(self):
        time.sleep(random.randint(1,2))  
        dtz_loginItem = self.loginItems['qsdw']['user']
        dtz_loginItem['limittime'] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        dtz_loginItem['resultprocess'] = "申请非正常结案"
        dtz_loginItem['operatingComments'] = "流程无法继续，申请非正常结案"
        #待调整列表url
        dtz_loginItem['pflist_url'] = '/dcms/cwsCase/Case-adjustlist.action?casestate=40&menuId=402880822f9490ad012f949b98b4004c&keywords=402880eb2f90e905012f9138a5fb00a4'
        #申请非正常结案url
        dtz_loginItem['pf_url'] = '/dcms/cwsCase/Case-applyabnormal.action'
        paifa_result = distribution(dtz_loginItem).test_sendDetailsAndSendOut()
        if paifa_result:
            logging.info("*****8.web申请非正常结案完毕*****")    

    #批示（批准结案）
    def test_09piZhunJieAn(self):
        time.sleep(random.randint(1,2)) 
        dataItem = {}
        dataItem['resultprocess'] = "批准"
        dataItem['leaderComments'] = "批准了"
        psres = Approval(dataItem).stayApprovalDetail()
        if psres:
            logging.info("*****9.web批示完毕(%s)*****"%dataItem['resultprocess'])  
        else:
            logging.info("*****9.web批示出错(%s)*****"%dataItem['resultprocess']) 
    
    @classmethod
    def tearDownClass(cls): 
        logging.info("***流程结束***")

if __name__=="__main__":
    unittest.main()
    
    