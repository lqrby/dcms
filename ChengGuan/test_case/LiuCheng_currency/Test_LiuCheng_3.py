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
from piSi import Approval
from chuLi import fileFandling
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
        
    # #web端登录
    # def test_1webLogin_lc5(self):
    #     webLogin = self.loginObj.test_web_login()
    #     while webLogin==False:
    #         webLogin = self.loginObj.test_web_login()
    #     logging.info("*****1.web端登录完毕*****")

    # #移动端登录
    # def test_2apkLogin_lc5(self):
    #     time.sleep(random.randint(1,3)) 
    #     appLogin = self.loginObj.test_app_allLogin()
    #     while appLogin == False:
    #         appLogin = self.loginObj.test_app_allLogin()
    #     logging.info("*****2.移动端登录完毕*****")

    # 执法局上报案卷
    def test_3gongDan_lc2(self):
        time.sleep(random.randint(1,3)) 
        markPath = getConstant.PROJECT_PATH+"/common/numberMark.txt"
        mark = writeAndReadTextFile().test_read_txt(markPath)
        dict_mark = json.loads(mark)
        number = int(dict_mark['zfj_sb'])+1
        orderData = self.loginItems['zfj']['user']
        orderData['eorcid'] = getConstant.EORCID_SJ #事部件类型 
        orderData['fieldintro'] = '吉林市 高新开发区 高新开发区街道 恒厦社区 恒厦社区第九网格'
        orderData['mposl'] = '14088524.212997204'
        orderData['description'] = '流程三，路面不干净'+str(number)
        orderData['eventtypeoneId'] = getConstant.SJ_SRHJ #大类  市容环境
        orderData['gridid'] = '22020600100109'
        # orderData['bgadminId'] =  #上报人id
        orderData['eventtypetwoId'] = getConstant.SJ_SRHJ_DLBJ #小类   道路不洁
        orderData['mposb'] = '5437559.658689937'#执法局上报案卷（移动端）
        sb_picpath1 = "E:/test/dcms/ChengGuan/testFile/img/24.png"
        sb_picpath2 = "E:/test/dcms/ChengGuan/testFile/img/25.png"
        # hs_picpath3 = "E:/test/dcms/ChengGuan/testFile/img/12.png"
        orderData['imgPath'] = [sb_picpath1,sb_picpath2]
        res = submitOrder(orderData).test_app_submitOrder()
        # print(sm_res)
        if res:
            dict_mark["zfj_sb"] = str(number)
            writeAndReadTextFile().test_write_txt(markPath,json.dumps(dict_mark))
            logging.info("*****3.执法局上报案卷完毕*****")
        else:
            logging.info("XXXXXXXXXX3.执法局上报案卷失败XXXXXXXXXX")
              


    #web端立案   
    def test_4liAn(self):
        time.sleep(random.randint(1,3)) 
        lianData = {}
        lianData['resultprocess'] = "立案"
        lianData['operatingComments'] = "批准立案"
        lian_result = setUpCase(lianData).test_detailsAndFiling()
        if lian_result:
            logging.info("*****4.web立案完毕*****")
        else:
            logging.info("XXXXXXXXXXX4.web立案失败XXXXXXXXXX")
        

    # #web端派发 
    def test_5paiFa_lc2(self):
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
            logging.info("XXXXXXXXXX5.web派发失败XXXXXXXXXX")

    # 处理 移动端权属单位apk处理
    def test_6chuLi_lc2(self):
        time.sleep(random.randint(1,2)) 
        cl_loginItem = self.loginItems['qsdw']['user']
        cl_loginItem['operatingComments'] = '处理完成3'
        cl_loginItem['resultprocess'] = '处理结束'
        cl_picpath1 = "E:/test/dcms/ChengGuan/testFile/img/29.png"
        cl_picpath2 = "E:/test/dcms/ChengGuan/testFile/img/28.png"
        cl_loginItem['imgPath'] = [cl_picpath1,cl_picpath2]
        cl_result = fileFandling(cl_loginItem).test_app_handlingDetailsAndHandling()
        if cl_result:
            logging.info("*****6.移动端权属单位处理完毕*****")
        else:
            logging.info("XXXXXXXXX6.移动端权属单位处理失败XXXXXXXXX")

    # 复核 执法局复核
    def test_7fuHe_lc2(self):
        time.sleep(random.randint(1,2)) 
        fh_loginUser = self.loginItems['zfj']['user']
        fh_loginUser['checkdesc'] = '经复核有效'

        fh_picpath1 = "E:/test/dcms/ChengGuan/testFile/img/23.png"
        # fh_picpath2 = "E:/test/dcms/ChengGuan/testFile/img/15.png"
        # fh_picpath3 = "E:/test/dcms/ChengGuan/testFile/img/16.png"
        fh_loginUser['imgPath'] = [fh_picpath1]
        fh_result = reviewAndReturnVisit(fh_loginUser).test_app_returnDetailsAndVisit()
        if fh_result:
            logging.info("*****7.移动端执法局复核完毕*****")
        else:
            logging.info("XXXXXXXXXX7.移动端执法局复核失败XXXXXXXXXX")

    @classmethod
    def tearDownClass(cls): 
        # cls.driver.quit()            #与setUp()相对y  
        logging.info("***流程结束***")

if __name__=="__main__":
    unittest.main()