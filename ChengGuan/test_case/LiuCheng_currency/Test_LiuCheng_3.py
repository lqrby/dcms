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
from zongHeChaXun import colligateQuery

class MyTest2(unittest.TestCase):     #封装测试环境的初始化和还原的类  
    @classmethod
    def setUpClass(cls): #放对数据可操作的代码，如对mysql、momgodb的初始化等,这里不对数据库进行操作！  
        # 初始化移动端登录人员集合对象
        cls.loginItems = writeAndReadTextFile().test_read_appLoginResult()
        #获取cookies
        cls.cookies = writeAndReadTextFile().test_readCookies()
        
    # 执法局上报案卷
    def gongDan(self):
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
        if res:
            dict_mark["zfj_sb"] = str(number)
            writeAndReadTextFile().test_write_txt(markPath,json.dumps(dict_mark))
            logging.info("*****3.执法局上报案卷完毕*****")
            return {'description':number}
        
              
    #web端立案   
    def liAn(self):
        time.sleep(random.randint(1,3)) 
        lianData = {}
        lianData['oderNumber'] = self.oderNumber
        lianData['resultprocess'] = "立案"
        lianData['operatingComments'] = "批准立案"
        lian_result = setUpCase(lianData).test_detailsAndFiling()
        if lian_result:
            logging.info("*****4.web立案完毕*****")
            return True
        else:
            logging.info("XXXXXXXXXXX4.web立案失败XXXXXXXXXX")
        

    # #web端派发 
    def paiFa(self):
        time.sleep(random.randint(1,2)) 
        pf_loginItem = self.loginItems['qsdw']['user']
        outDir = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        pf_loginItem['oderNumber'] = self.oderNumber
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
            return True
        else:
            logging.info("XXXXXXXXXX5.web派发失败XXXXXXXXXX")

    # 处理 移动端权属单位apk处理
    def chuLi(self):
        time.sleep(random.randint(1,2)) 
        cl_loginItem = self.loginItems['qsdw']['user']
        cl_loginItem['oderNumber'] = self.oderNumber
        cl_loginItem['operatingComments'] = '处理完成3'
        cl_loginItem['resultprocess'] = '处理结束'
        cl_picpath1 = "E:/test/dcms/ChengGuan/testFile/img/29.png"
        cl_picpath2 = "E:/test/dcms/ChengGuan/testFile/img/28.png"
        cl_loginItem['imgPath'] = [cl_picpath1,cl_picpath2]
        cl_result = fileFandling(cl_loginItem).test_app_handlingDetailsAndHandling()
        if cl_result:
            logging.info("*****6.移动端权属单位处理完毕*****")
            return True
        else:
            logging.info("XXXXXXXXX6.移动端权属单位处理失败XXXXXXXXX")

    # 复核 执法局复核
    def fuHe(self):
        time.sleep(random.randint(1,2)) 
        fh_loginUser = self.loginItems['zfj']['user']
        fh_loginUser['checkdesc'] = '经复核有效'
        fh_picpath1 = "E:/test/dcms/ChengGuan/testFile/img/23.png"
        # fh_picpath2 = "E:/test/dcms/ChengGuan/testFile/img/15.png"
        # fh_picpath3 = "E:/test/dcms/ChengGuan/testFile/img/16.png"
        fh_loginUser['casestateid'] = getConstant.FHYX  #复核通过、复核不通过
        fh_loginUser['oderNumber'] = self.oderNumber
        fh_loginUser['imgPath'] = [fh_picpath1]
        fh_result = reviewAndReturnVisit(fh_loginUser).test_app_returnDetailsAndVisit()
        if fh_result:
            logging.info("*****7.移动端执法局复核完毕*****")
            return True
        else:
            logging.info("XXXXXXXXXX7.移动端执法局复核失败XXXXXXXXXX")

    @classmethod
    def tearDownClass(cls): 
        # cls.driver.quit()            #与setUp()相对y  
        logging.info("***流程结束***")

    def test_liucheng_3(self):
        for i in range(1):
            # 工单录入
            loginItems = self.gongDan()
            if loginItems:
                print(loginItems)
                print("请您耐心等待大约一分钟......")
                time.sleep(random.randint(50,60))
                oderid = colligateQuery(loginItems).selectOder()
                if oderid:
                    self.oderNumber = oderid
                    print("成功获取上报案卷单号:{}".format(self.oderNumber))
                    lian = self.liAn()
                    if lian:
                        time.sleep(random.randint(5,8))
                        paifa = self.paiFa()
                        if paifa:
                            time.sleep(random.randint(5,8))
                            chuli = self.chuLi()
                            if chuli:
                                time.sleep(random.randint(5,8))
                                fuhe = self.fuHe()
                                if fuhe:
                                    print("流程走完啦，帅呆了！！！")
            
            
            

if __name__=="__main__":
    unittest.main()