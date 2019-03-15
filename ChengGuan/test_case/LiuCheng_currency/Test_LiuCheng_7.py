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
from guaZhang import hangUp
from piSi import Approval
from chuLi import fileFandling
from fuHeAndHuiFang import reviewAndReturnVisit
from common.writeAndReadText import writeAndReadTextFile



class MyTest2(unittest.TestCase):     #封装测试环境的初始化和还原的类  
    @classmethod
    def setUpClass(cls): #放对数据可操作的代码，如对mysql、momgodb的初始化等,这里不对数据库进行操作！  
        
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
        orderData['eorcid'] = getConstant.EORCID_BJ #事部件类型 
        orderData['fieldintro'] = '吉林市 高新开发区 高新开发区街道 恒厦社区 恒厦社区第九网格'
        orderData['mposl'] = '14088524.212997204'
        orderData['description'] = '流程七，路面不干净'+str(number)
        orderData['eventtypeoneId'] = getConstant.BJ_YLLH #大类  园林绿化
        orderData['gridid'] = '22020600100109'
        # orderData['bgadminId'] =  #上报人id
        orderData['eventtypetwoId'] = getConstant.BJ_YLLH_LDHL #小类   绿地
        orderData['mposb'] = '5437559.658689937'
        sb_picpath1 = "E:/test/dcms/ChengGuan/testFile/img/12.png"
        sb_picpath2 = "E:/test/dcms/ChengGuan/testFile/img/15.png"
        # hs_picpath3 = "E:/test/dcms/ChengGuan/testFile/img/12.png"
        orderData['imgPath'] = [sb_picpath1,sb_picpath2]
        res = submitOrder(orderData).test_app_submitOrder()
        if res:
            dict_mark["zfj_sb"] = str(number)
            writeAndReadTextFile().test_write_txt(markPath,json.dumps(dict_mark))
            logging.info("*****3.执法局上报案卷完毕*****")
        else:
            logging.info("XXXXXXXXXX3.执法局上报案卷失败XXXXXXXXXX")
              


    #web端立案   
    def liAn(self):
        time.sleep(random.randint(1,3)) 
        lianData = {}
        lianData['resultprocess'] = "立案"
        lianData['operatingComments'] = "批准立案"
        lian_result = setUpCase(lianData).test_detailsAndFiling()
        if lian_result:
            logging.info("*****4.web立案完毕*****")
        else:
            logging.info("XXXXXXXXXXX4.web立案失败XXXXXXXXXX")


    # #web端派发时挂起
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
            logging.info("*****5.web挂起完毕*****")

    #挂账》恢复
    def huiFu(self):
        gzItem = {}
        gzItem['resultprocess'] = '恢复'
        gzItem['operatingComments'] = '恢复案卷流程'
        gz_res = hangUp(gzItem).test_hangUpDetail()
        if gz_res ==True:
            logging.info("*****6.web挂账案卷恢复成功*****")  

    # #web端派发>申请非正常结案
    def feiZhengChangJieAn(self):
        time.sleep(random.randint(1,2))  
        pf_loginItem = self.loginItems['qsdw']['user']
        pf_loginItem['limittime'] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        pf_loginItem['resultprocess'] = "申请非正常结案"
        pf_loginItem['operatingComments'] = "流程无法继续，申请非正常结案"
        #待派发列表url
        pf_loginItem['pflist_url'] = '/dcms/cwsCase/Case-dispatchlist.action?casestate=20&menuId=4028338158a414bd0158a484daae000e&keywords=402880ea2f6bd924012f6c521e8c0034'
        #申请非正常结案url
        pf_loginItem['pf_url'] = '/dcms/cwsCase/Case-applyabnormal.action'
        paifa_result = distribution(pf_loginItem).test_sendDetailsAndSendOut()
        if paifa_result:
            logging.info("*****7.web申请非正常结案完毕*****")    

    #批示（批准结案）
    def piShi(self):
        time.sleep(random.randint(1,2)) 
        dataItem = {}
        dataItem['oderNumber'] = self.oderNumber
        dataItem['resultprocess'] = "批准"
        dataItem['leaderComments'] = "批准了"
        psres = Approval(dataItem).stayApprovalDetail()
        if psres:
            logging.info("*****8.web批示完毕(%s)*****"%dataItem['resultprocess'])  
        else:
            logging.info("*****8.web批示出错(%s)*****"%dataItem['resultprocess'])  

      
  
    @classmethod
    def tearDownClass(cls): 
        logging.info("***流程结束***")



    def test_liucheng_1(self):
        self.oderNumber = '201902270025'
        for i in range(1):
            # self.gongDan()
            # self.liAn()
            # self.paiFa()
            # self.chuLi()
            # self.tiaoZhengPiShi()
            self.piShi()
            # self.daiTiaoZheng()
            # self.chuLis()
            # self.fuHe()

if __name__=="__main__":
    unittest.main()