# -*- coding: utf-8 -*-
import re
import unittest
import sys,random
sys.path.append("E:/test/dcms/ChengGuan")
import time,json
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
from tiaoZhengPiSi import adjustmentApproval
from fuHeAndHuiFang import reviewAndReturnVisit
from common.writeAndReadText import writeAndReadTextFile



class MyTest2(unittest.TestCase):     #封装测试环境的初始化和还原的类  
    @classmethod
    def setUpClass(cls): #放对数据可操作的代码，如对mysql、momgodb的初始化等,这里不对数据库进行操作！  
        # cls.driver = webdriver.Chrome("D:/python/chromeDriverSever/chromedriver.exe")
        # logging.info("***打开浏览器***")
        # # 初始化登录数据及登录类对象
        # userData = {}
        # if '180' in getConstant.IP:
        #     ip = getConstant.IP+getConstant.PORT_7897
        #     userData = { 
        #         'sm':{'loginName':'13161577834','password':'123456'},
        #         'wggly':{'role':'2','logonname':'csgly','logonpassword':'123456'},
        #         'qsdw':{'role':'6','logonname':'cshbj','logonpassword':'123456'},
        #         'zfj':{'role':'5','logonname':'cszfj','logonpassword':'123456'},
            
        #     }
        # else:
        #     ip = getConstant.IP
        #     userData = { 
        #         'sm':{'loginName':'13161577834','password':'111111'},
        #         'wggly':{'role':'2','logonname':'gly','logonpassword':'111111'},
        #         'qsdw':{'role':'6','logonname':'hbj','logonpassword':'111111'},
        #         'zfj':{'role':'5','logonname':'zfj','logonpassword':'111111'},
                
        #     }
        
        # url= ip+'/dcms/bms/login.jsp'
        # print("url:",url)
        # cls.loginObj = allLogin(cls.driver,url,userData)
        # 初始化移动端登录人员集合对象
        cls.loginItems = writeAndReadTextFile().test_read_appLoginResult()
        #获取cookies
        cls.cookies = writeAndReadTextFile().test_readCookies()

    #执法局上报案卷（移动端）
    def gongDan(self):
        time.sleep(random.randint(1,3)) 
        markPath = getConstant.PROJECT_PATH+"/common/numberMark.txt"
        mark = writeAndReadTextFile().test_read_txt(markPath)
        dict_mark = json.loads(mark)
        number = int(dict_mark['zfj_sb'])+1
        orderData = self.loginItems['zfj']['user']
        orderData['eorcid'] = getConstant.EORCID_SJ #事部件类型 
        orderData['fieldintro'] = '吉林市 经济开发区 工厂 鑫海实业 '
        orderData['mposl'] = '14077292.84373848'
        orderData['description'] = "流程四，经开区道路不干净，环境脏乱差"+str(number)
        orderData['eventtypeoneId'] = getConstant.SJ_JMZX #大类  街面秩序
        orderData['gridid'] = '220298205118'
        # orderData['bgadminId'] =  #上报人id
        orderData['eventtypetwoId'] = getConstant.SJ_JMZX_LDLF #小类  乱堆乱放
        orderData['mposb'] = '5459844.618760589'
        sb_picpath1 = "E:/test/dcms/ChengGuan/testFile/img/26.png"
        sb_picpath2 = "E:/test/dcms/ChengGuan/testFile/img/27.png"
        orderData['imgPath'] = [sb_picpath1,sb_picpath2]
        res = submitOrder(orderData).test_app_submitOrder()
        if res:
            dict_mark["zfj_sb"] = str(number)
            writeAndReadTextFile().test_write_txt(markPath,json.dumps(dict_mark))
            logging.info("*****3.%s上报案卷完毕*****"%orderData['name'])
        else:
            logging.info("XXXXXXXXXX3.%s执法局上报案卷失败XXXXXXXXXX"%orderData['name'])
              

    #web端立案   
    def liAn(self):
        time.sleep(random.randint(1,3)) 
        lianData = {}
        lianData['resultprocess'] = "立案"
        lianData['startConditionId'] = "4028838358b04eb70158b310c8ba5295"  #立案条件？
        lianData['operatingComments'] = "批准立案"
        lian_result = setUpCase(lianData).test_detailsAndFiling()
        if lian_result:
            logging.info("*****4.web立案完毕*****")
        else:
            logging.info("XXXXXXXXXXX4.web立案失败XXXXXXXXXX")
        

    #web端派发 
    def paiFa(self):
        time.sleep(random.randint(1,3)) 
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
            logging.info("XXXXXXXXXX5.web派发失败XXXXXXXXXX")

    
    # 处理 移动端权属单位apk处理
    def chuLi_lc2(self):
        time.sleep(random.randint(1,2)) 
        cl_loginItem = self.loginItems['qsdw']['user']
        cl_loginItem['resultprocess'] = '处理结束'
        cl_loginItem['operatingComments'] = '处理完成4'
        cl_picpath1 = "E:/test/dcms/ChengGuan/testFile/img/30.png"
        cl_picpath2 = "E:/test/dcms/ChengGuan/testFile/img/31.png"
        cl_loginItem['imgPath'] = [cl_picpath1,cl_picpath2]
        cl_result = fileFandling(cl_loginItem).test_app_handlingDetailsAndHandling()
        if cl_result:
            logging.info("*****6.移动端执法局处理完毕*****")
        else:
            logging.info("XXXXXXXXX6.移动端执法局处理失败XXXXXXXXX")

    # 复核 执法局复核
    def fuHe_lc2(self):
        fh_loginUser = self.loginItems['zfj']['user']
        fh_loginUser['checkdesc'] = '经复核有效'
        fh_picpath1 = "E:/test/dcms/ChengGuan/testFile/img/30.png"
        fh_picpath2 = "E:/test/dcms/ChengGuan/testFile/img/31.png"
        fh_loginUser['imgPath'] = [fh_picpath1,fh_picpath2]
        fh_result = reviewAndReturnVisit(fh_loginUser).test_app_returnDetailsAndVisit()
        if fh_result:
            logging.info("*****7.移动端网格管理员复核完毕*****")
        else:
            logging.info("XXXXXXXXXX7.移动端网格管理员复核失败XXXXXXXXXX")


    def test_liucheng(self):
        for i in range(1):
            self.gongDan()
            self.liAn()
            self.paiFa()
            self.chuLi_lc2()
            self.fuHe_lc2()

    @classmethod
    def tearDownClass(cls): 
        logging.info("***流程结束***")

if __name__=="__main__":
    unittest.main()