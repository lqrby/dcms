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
        # 初始化移动端登录人员集合对象
        cls.loginItems = writeAndReadTextFile().test_read_appLoginResult()
        #获取cookies
        cls.cookies = writeAndReadTextFile().test_readCookies()
        
    #执法局上报案卷（移动端）
    def test_3gongDan_lc2(self):
        time.sleep(random.randint(1,3)) 
        markPath = getConstant.PROJECT_PATH+"/common/numberMark.txt"
        mark = writeAndReadTextFile().test_read_txt(markPath)
        dict_mark = json.loads(mark)
        number = int(dict_mark['zfj_sb'])+1
        orderData = self.loginItems['zfj']['user']
        orderData['eorcid'] = getConstant.EORCID_BJ #事部件类型 
        orderData['fieldintro'] = '吉林市 高新开发区 高新开发区街道 恒厦社区 恒厦社区第九网格'
        orderData['mposl'] = '14088524.212997204'
        orderData['description'] = '流程八，路面不干净'+str(number)
        orderData['eventtypeoneId'] = getConstant.BJ_GGSS #大类  
        orderData['gridid'] = '22020600100109'
        # orderData['bgadminId'] =  #上报人id
        orderData['eventtypetwoId'] = getConstant.BJ_GGSS_DLJG #小类   
        orderData['mposb'] = '5437559.658689937'
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
    def test_4liAn_lc2(self):
        time.sleep(random.randint(1,3)) 
        lianData = {}
        lianData['resultprocess'] = "立案"
        lianData['operatingComments'] = "批准立案"
        lian_result = setUpCase(lianData).test_detailsAndFiling()
        if lian_result:
            logging.info("*****4.web立案完毕*****")
        else:
            logging.info("XXXXXXXXXXX4.web立案失败XXXXXXXXXX")
        

    # #web端派发>申请非正常结案
    def test_5feiZhengChangJieAn(self):
        time.sleep(random.randint(1,2))  
        pf_loginItem = self.loginItems['qsdw']['user']
        pf_loginItem['limittime'] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        pf_loginItem['resultprocess'] = "申请非正常结案"
        pf_loginItem['operatingComments'] = "流程无法继续，申请非正常结案"
        #待派发列表url
        pf_loginItem['pflist_url'] = getConstant.dpf_ListUrl
        #申请非正常结案url
        pf_loginItem['pf_url'] = getConstant.sqfzcja_url
        paifa_result = distribution(pf_loginItem).test_sendDetailsAndSendOut()
        if paifa_result:
            logging.info("*****5.web申请非正常结案完毕*****")   


    #批示（不批准结案）
    def test_6piZhunJieAn(self):
        time.sleep(random.randint(1,2)) 
        dataItem = {}
        dataItem['resultprocess'] = "不批准"
        dataItem['leaderComments'] = "确实归贵部门处理"
        psres = Approval(dataItem).stayApprovalDetail()
        if psres:
            logging.info("*****6.web批示完毕(%s)*****"%dataItem['resultprocess'])  
        else:
            logging.info("*****6.web批示出错(%s)*****"%dataItem['resultprocess'])   




    # #web端待调整
    def test_7tiaoZheng(self):
        time.sleep(random.randint(1,2))  
        pf_loginItem = self.loginItems['qsdw']['user']
        pf_loginItem['resultprocess'] = "派发"
        pf_loginItem['limittime'] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        pf_loginItem['operatingComments'] = "请尽快处理"
        #待派发列表url
        # pf_loginItem['pflist_url'] = '/dcms/cwsCase/Case-dispatchlist.action?casestate=20&menuId=4028338158a414bd0158a484daae000e&keywords=402880ea2f6bd924012f6c521e8c0034'
        #待调整列表url
        pf_loginItem['pflist_url'] = '/dcms/cwsCase/Case-adjustlist.action?casestate=40&menuId=402880822f9490ad012f949b98b4004c&keywords=402880eb2f90e905012f9138a5fb00a4'
        # pf_loginItem['pf_url'] = '/dcms/cwsCase/Case-applyabnormal.action'
        pf_loginItem['pf_url'] = '/dcms/cwsCase/Case-dispatch.action'
        paifa_result = distribution(pf_loginItem).test_sendDetailsAndSendOut()
        if paifa_result:
            logging.info("*****7.web调整完毕*****")   
        else:
             logging.info("*****7.web调整出错*****")       
  
    # 处理 移动端权属单位apk处理
    def test_8chuLi_lc2(self):
        time.sleep(random.randint(1,2)) 
        cl_loginItem = self.loginItems['qsdw']['user']
        cl_loginItem['operatingComments'] = '处理完成8'
        cl_loginItem['resultprocess'] = '处理结束'
        cl_picpath1 = "E:/test/dcms/ChengGuan/testFile/img/29.png"
        cl_picpath2 = "E:/test/dcms/ChengGuan/testFile/img/28.png"
        cl_loginItem['imgPath'] = [cl_picpath1,cl_picpath2]
        cl_result = fileFandling(cl_loginItem).test_app_handlingDetailsAndHandling()
        if cl_result:
            logging.info("*****8.移动端权属单位处理完毕*****")
        else:
            logging.info("XXXXXXXXX8.移动端权属单位处理失败XXXXXXXXX")

    # 复核 执法局复核
    def test_9fuHe_lc2(self):
        time.sleep(random.randint(1,2)) 
        fh_loginUser = self.loginItems['zfj']['user']
        fh_loginUser['checkdesc'] = '经复核有效'

        fh_picpath1 = "E:/test/dcms/ChengGuan/testFile/img/23.png"
        # fh_picpath2 = "E:/test/dcms/ChengGuan/testFile/img/15.png"
        # fh_picpath3 = "E:/test/dcms/ChengGuan/testFile/img/16.png"
        fh_loginUser['imgPath'] = [fh_picpath1]
        fh_result = reviewAndReturnVisit(fh_loginUser).test_app_returnDetailsAndVisit()
        if fh_result:
            logging.info("*****9.移动端执法局复核完毕*****")
        else:
            logging.info("XXXXXXXXXX9.移动端执法局复核失败XXXXXXXXXX")

    @classmethod
    def tearDownClass(cls): 
        logging.info("***流程结束***")

if __name__=="__main__":
    unittest.main()