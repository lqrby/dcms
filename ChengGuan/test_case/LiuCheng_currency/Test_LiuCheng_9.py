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
from chuLi import fileFandling
from tiaoZhengPiSi import adjustmentApproval
from fuHeAndHuiFang import reviewAndReturnVisit
from common.writeAndReadText import writeAndReadTextFile



class MyTest2(unittest.TestCase):     #封装测试环境的初始化和还原的类  
    @classmethod
    def setUpClass(cls): #放对数据可操作的代码，如对mysql、momgodb的初始化等,这里不对数据库进行操作！  
        # 初始化移动端登录人员集合对象
        cls.loginItems = writeAndReadTextFile().test_read_appLoginResult()
        #获取cookies
        cls.cookies = writeAndReadTextFile().test_readCookies()

    #网格管理员上报案卷（移动端）
    def test_03gongDan(self):
        time.sleep(random.randint(1,3)) 
        markPath = getConstant.PROJECT_PATH+"/common/numberMark.txt"
        mark = writeAndReadTextFile().test_read_txt(markPath)
        dict_mark = json.loads(mark)
        number = int(dict_mark['wggly_sb'])+1
        orderData = self.loginItems['wggly']['user']
        orderData['eorcid'] = getConstant.EORCID_SJ #事部件类型 
        orderData['fieldintro'] = '吉林市 高新开发区 高新开发区街道 恒厦社区 恒厦社区第九网格'
        orderData['mposl'] = '14088524.212997204'
        orderData['description'] = "流程九，道路不干净，环境脏乱差"+str(number)
        orderData['eventtypeoneId'] = getConstant.SJ_SRHJ #大类  市容环境
        orderData['gridid'] = '22020600100109'
        # orderData['bgadminId'] =  #上报人id
        orderData['eventtypetwoId'] = getConstant.SJ_SRHJ_DLBJ #小类   道路不洁
        orderData['mposb'] = '5437559.658689937'
        sb_picpath1 = "E:/test/dcms/ChengGuan/testFile/img/26.png"
        sb_picpath2 = "E:/test/dcms/ChengGuan/testFile/img/27.png"
        orderData['imgPath'] = [sb_picpath1,sb_picpath2]
        res = submitOrder(orderData).test_app_submitOrder()
        if res:
            dict_mark["wggly_sb"] = str(number)
            writeAndReadTextFile().test_write_txt(markPath,json.dumps(dict_mark))
            logging.info("*****3.%s上报案卷完毕*****"%orderData['name'])
        else:
            logging.info("XXXXXXXXXX3.%s执法局上报案卷失败XXXXXXXXXX"%orderData['name'])
              
    #web端立案   
    def test_04liAn(self):
        time.sleep(random.randint(1,3)) 
        lianData = {}
        lianData['resultprocess'] = "立案"
        lianData['operatingComments'] = "批准立案"
        lian_result = setUpCase(lianData).test_detailsAndFiling()
        if lian_result:
            logging.info("*****4.web立案完毕*****")
        else:
            logging.info("XXXXXXXXXXX4.web立案失败XXXXXXXXXX")
        

    #web端派发 
    def test_05paiFa(self):
        time.sleep(random.randint(1,3)) 
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
        else:
            logging.info("XXXXXXXXXX5.web派发失败XXXXXXXXXX")

    # 申请调整 移动端权属单位apk申请调整
    def test_06shenQingTiaoZheng(self):
        time.sleep(random.randint(1,3)) 
        cl_loginItem = self.loginItems['zfj']['user']
        cl_loginItem['resultprocess'] = '申请调整'   #不可更改
        cl_loginItem['operatingComments'] = '请求调整'  #
        cl_loginItem['applyReason'] = '非我辖区'  #调整原因
        cl_result = fileFandling(cl_loginItem).test_requestAdjustment()
        if cl_result:
            logging.info("*****6.移动端权属单位申请调整成功*****")
        else:
            logging.info("XXXXXXXXXXXXXXXXXXXXXX6.移动端权属单位申请调整失败XXXXXXXXXXXXXXXXXXX")

    
    #调整批示    
    def test_07tiaoZhengPiShi(self):
        time.sleep(random.randint(1,2)) 
        dataItem = {}
        dataItem['resultprocess'] = "批准"
        dataItem['leaderComments'] = "批准了"
        tzpsOK = adjustmentApproval(dataItem).adjustmentApprovalDetail()
        if tzpsOK != False:
            logging.info("*****7.web端调整批示成功(%s)*****"%dataItem['resultprocess'])
        else:
            logging.info("XXXXXXXXXXXXX7.web端调整批示失败(%s)XXXXXXXXXXX"%dataItem['resultprocess'])

    #待调整 》挂起
    def test_08daiTiaoZheng(self):
        time.sleep(random.randint(1,2)) 
        dtz_dataItem = self.loginItems['qsdw']['user']
        dtz_dataItem['resultprocess'] = "挂账"
        dtz_dataItem['limittime'] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        dtz_dataItem['operatingComments'] = "暂时挂起"
        #待调整列表url
        dtz_dataItem['pflist_url'] = getConstant.dtz_ListUrl
        dtz_dataItem['pf_url'] = getConstant.pf_url
        paifa_result = distribution(dtz_dataItem).test_sendDetailsAndSendOut()
        if paifa_result:
            logging.info("*****8.web调整完毕(%s)*****"%dtz_dataItem['resultprocess'])

    #挂账》恢复
    def test_09huiFu(self):
        time.sleep(random.randint(1,2)) 
        gzItem = {}
        gzItem['resultprocess'] = '恢复'
        gzItem['operatingComments'] = '恢复案卷流程'
        gz_res = hangUp(gzItem).test_hangUpDetail()
        if gz_res ==True:
            logging.info("*****9.web挂账案卷恢复成功*****")
        

    # #web端派发
    def test_10paiFa(self):
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
            logging.info("*****10.web派发完毕*****")


    # 处理 移动端权属单位apk处理
    def test_11chuLi(self):
        time.sleep(random.randint(1,2)) 
        cl_loginItem = self.loginItems['qsdw']['user']
        cl_loginItem['resultprocess'] = '处理结束'
        cl_loginItem['operatingComments'] = '处理完成4'
        cl_picpath1 = "E:/test/dcms/ChengGuan/testFile/img/30.png"
        cl_picpath2 = "E:/test/dcms/ChengGuan/testFile/img/31.png"
        cl_loginItem['imgPath'] = [cl_picpath1,cl_picpath2]
        cl_result = fileFandling(cl_loginItem).test_app_handlingDetailsAndHandling()
        if cl_result:
            logging.info("*****11.移动端执法局处理完毕*****")
        else:
            logging.info("XXXXXXXXX11.移动端执法局处理失败XXXXXXXXX")

    # 复核 执法局复核
    def test_12fuHe(self):
        time.sleep(random.randint(1,2)) 
        fh_loginUser = self.loginItems['wggly']['user']
        fh_loginUser['checkdesc'] = '经复核有效'
        fh_picpath1 = "E:/test/dcms/ChengGuan/testFile/img/10.png"
        fh_picpath2 = "E:/test/dcms/ChengGuan/testFile/img/11.png"
        fh_loginUser['imgPath'] = [fh_picpath1,fh_picpath2]
        fh_result = reviewAndReturnVisit(fh_loginUser).test_app_returnDetailsAndVisit()
        if fh_result:
            logging.info("*****12.移动端网格管理员复核完毕*****")
        else:
            logging.info("XXXXXXXXXX12.移动端网格管理员复核失败XXXXXXXXXX")

    @classmethod
    def tearDownClass(cls): 
        logging.info("***流程结束***")

if __name__=="__main__":
    unittest.main()