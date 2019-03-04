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
    #     time.sleep(random.randint(1,2)) 
    #     appLogin = self.loginObj.test_app_allLogin()
    #     while appLogin == False:
    #         appLogin = self.loginObj.test_app_allLogin()
    #     logging.info("*****2.移动端登录完毕*****")

    #移动端市民上报案卷
    def test_3gongDan_lc2(self):
        time.sleep(random.randint(1,3))
        markPath = getConstant.PROJECT_PATH+"/common/numberMark.txt"
        mark = writeAndReadTextFile().test_read_txt(markPath)
        dict_mark = json.loads(mark)
        number = int(dict_mark['sm_sb'])+1
        orderData = self.loginItems['sm']['result']
        orderData['longitude'] = '14090823.883200558'
        orderData['latitude'] = '5446737.409308622'
        orderData['complaincontent'] = '流程二，设施脏污1'+str(number) #描述
        orderData['bgcode'] = '220202003001' #网格
        orderData['bgcodename'] = '锦东社区' #地址
        orderData['gridid'] = '220202003001'
        orderData['wxsource'] = 'GZHJB'
        orderData['imgurl'] = '/image/20181008/f7bffd2e16154c8f817f5fc1b442f21d.jpg'
        orderData['eorcid'] = getConstant.EORCID_SJ
        orderData['eventoneid'] = getConstant.SJ_SGGL
        orderData['eventtwoid'] = getConstant.SJ_SGGL_WZJL
        res = submitOrder(orderData).test_app_sm_submitOrder()
        print(res)
        if res:
            dict_mark["sm_sb"] = str(number)
            writeAndReadTextFile().test_write_txt(markPath,json.dumps(dict_mark))
            logging.info("*****3.市民上报案卷完毕*****")


    #web端确认案卷
    def test_4queRen_lc2(self):
        time.sleep(random.randint(1,3))
        loginUser = self.loginItems['zfj']['user']#核实人
        dataObject = {}
        dataObject['loginUser'] = loginUser
        dataObject['eorcId'] = getConstant.EORCID_SJ #事件
        dataObject['eventtypeoneId'] = getConstant.SJ_SGGL #大类
        dataObject['eventtypetwoId'] = getConstant.SJ_SGGL_WZJL #小类
        dataObject['regioncodeId'] = '220206' #高新开发区
        dataObject['bgcodeId'] = '220206001' #高新开发区街道	
        # dataObject['gridId'] = '22020600100706' #万米网格
        # dataObject['fieldintro'] = '吉林市 高新开发区 高新开发区街道 日升社区 日升社区第六网格' #位置描述
        dataObject['needconfirm'] = getConstant.NEEDCONFIRM_YES #核实
        dataObject['isFh'] = getConstant.ISFH_YES #复核
        qr_picpath = "E:/test/dcms/ChengGuan/testFile/img/36.png"
        qr_img = ('img.png', open(qr_picpath,'rb'),'multipart/form-data')
        dataObject['upload'] = qr_img
        qr_res = confirm(dataObject).test_web_UnconfirmedDetail()
        if qr_res:
            logging.info("*****4.web确认案卷完毕*****")

    #执法局核实案卷(移动端)
    def test_5heShi_lc2(self):
        time.sleep(random.randint(1,2))
        loginItem_hs = self.loginItems['zfj']['user']
        hs_picpath1 = "E:/test/dcms/ChengGuan/testFile/img/10.png"
        hs_picpath2 = "E:/test/dcms/ChengGuan/testFile/img/11.png"
        loginItem_hs['imgPath'] = [hs_picpath1,hs_picpath2]
        loginItem_hs['casestateid'] = getConstant.HSYX
        hs_res = verify(loginItem_hs).test_app_daiHeShiDetail()
        if hs_res:
            logging.info("*****5.执法局核实案卷完毕*****")


    # #web端立案   
    # def test_6liAn_lc2(self):
    #     time.sleep(random.randint(1,2)) 
    #     lianData = {}
    #     lianData['resultprocess'] = "立案"
    #     lianData['operatingComments'] = "批准立案"
    #     lian_result = setUpCase(lianData).test_detailsAndFiling()
    #     if lian_result:
    #         logging.info("*****6.web立案完毕*****")
    #     else:
    #         logging.info("*****6.web立案失败*****")



    # #web端派发 
    # def test_7paiFa(self):
    #     time.sleep(random.randint(1,2))
    #     pf_loginItem = self.loginItems['qsdw']['user']
    #     pf_loginItem['resultprocess'] = "派发"
    #     pf_loginItem['limittime'] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    #     pf_loginItem['operatingComments'] = "尽快处理"
    #     #待派发列表url
    #     pf_loginItem['pflist_url'] = getConstant.dpf_ListUrl
    #     #派发url
    #     pf_loginItem['pf_url'] = getConstant.pf_url
    #     paifa_result = distribution(pf_loginItem).test_sendDetailsAndSendOut()
    #     if paifa_result:
    #         logging.info("*****7.web派发完毕*****")
    #     else:
    #         logging.info("XXXXXXXXXXXXXXX7.web派发失败XXXXXXXXXXXXXXX")

    # # 处理 移动端权属单位apk处理
    # def test_8chuLi(self):
    #     time.sleep(random.randint(1,2)) 
    #     cl_loginItem = self.loginItems['qsdw']['user']
    #     cl_loginItem['resultprocess'] = '处理结束'
    #     cl_loginItem['operatingComments'] = '处理完成2'
    #     cl_picpath1 = "E:/test/dcms/ChengGuan/testFile/img/17.png"
    #     cl_picpath2 = "E:/test/dcms/ChengGuan/testFile/img/18.png"
    #     cl_loginItem['imgPath'] = [cl_picpath1,cl_picpath2]
    #     cl_result = fileFandling(cl_loginItem).test_app_handlingDetailsAndHandling()
    #     if cl_result:
    #         logging.info("*****8.移动端权属单位处理完毕*****")

    # # 复核 执法局复核
    # def test_9fuHe_lc2(self):
    #     time.sleep(random.randint(1,2))
    #     fh_loginUser = self.loginItems['zfj']['user']
    #     fh_loginUser['checkdesc'] = '经复核有效'
    #     fh_picpath1 = "E:/test/dcms/ChengGuan/testFile/img/14.png"
    #     # fh_picpath2 = "E:/test/dcms/ChengGuan/testFile/img/15.png"
    #     # fh_picpath3 = "E:/test/dcms/ChengGuan/testFile/img/16.png"
    #     fh_loginUser['imgPath'] = [fh_picpath1]
    #     fh_result = reviewAndReturnVisit(fh_loginUser).test_app_returnDetailsAndVisit()
    #     if fh_result:
    #         logging.info("*****9.移动端执法局复核完毕*****")

    @classmethod
    def tearDownClass(cls): 
        logging.info("***流程结束***")

if __name__=="__main__":
    
    unittest.main()