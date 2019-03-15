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
from piSi import Approval
from tiaoZhengPiSi import adjustmentApproval
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
    
    
    #移动端市民上报案卷
    def gongDan(self):
        time.sleep(random.randint(1,3))
        markPath = getConstant.PROJECT_PATH+"/common/numberMark.txt"
        mark = writeAndReadTextFile().test_read_txt(markPath)
        dict_mark = json.loads(mark)
        number = int(dict_mark['sm_sb'])+1
        orderData = self.loginItems['sm']['result']
        orderData['longitude'] = '14090823.883200558'
        orderData['latitude'] = '5446737.409308622'
        orderData['complaincontent'] = '流程十一，设施脏污'+str(number) #描述
        orderData['bgcode'] = '220202003001' #网格
        orderData['bgcodename'] = '锦东社区' #地址
        orderData['gridid'] = '220202003001'
        orderData['wxsource'] = 'GZHJB'
        orderData['imgurl'] = '/image/20181008/f7bffd2e16154c8f817f5fc1b442f21d.jpg'
        orderData['eorcid'] = getConstant.EORCID_SJ
        orderData['eventoneid'] = getConstant.SJ_JMZX
        orderData['eventtwoid'] = getConstant.SJ_JMZX_LTSK
        res = submitOrder(orderData).test_app_sm_submitOrder()
        if res:
            dict_mark["sm_sb"] = str(number)
            writeAndReadTextFile().test_write_txt(markPath,json.dumps(dict_mark))
            logging.info("*****3.市民上报案卷完毕*****")


    #web端确认案卷
    def queRen(self):
        time.sleep(random.randint(1,3))
        loginUser = self.loginItems['wggly']['user']#核实人
        dataObject = {}
        dataObject['loginUser'] = loginUser
        dataObject['eorcId'] = getConstant.EORCID_SJ #事件
        dataObject['eventtypeoneId'] = getConstant.SJ_JMZX #大类
        dataObject['eventtypetwoId'] = getConstant.SJ_JMZX_LTSK #小类
        dataObject['regioncodeId'] = '220206' #高新开发区
        dataObject['bgcodeId'] = '220206001' #高新开发区街道	
        dataObject['needconfirm'] = getConstant.NEEDCONFIRM_NO #不核实
        dataObject['isFh'] = getConstant.ISFH_NO #不复核
        qr_picpath = "E:/test/dcms/ChengGuan/testFile/img/36.png"
        qr_img = ('img.png', open(qr_picpath,'rb'),'multipart/form-data')
        dataObject['upload'] = qr_img
        qr_res = confirm(dataObject).test_web_UnconfirmedDetail()
        if qr_res:
            logging.info("*****4.web确认案卷完毕*****")


    # #web端立案
    def liAn(self):
        time.sleep(random.randint(1,3)) 
        lianData = {}
        lianData['resultprocess'] = "立案"
        lianData['operatingComments'] = "批准立案"
        lian_result = setUpCase(lianData).test_detailsAndFiling()
        if lian_result:
            logging.info("*****5.web立案完毕*****")
        else:
            logging.info("*****5.web立案失败*****")


    # #web端派发
    def paiFa(self):
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
            logging.info("*****6.web派发完毕*****")

    # 申请调整 移动端执法局apk申请调整
    def chuLi(self):
        time.sleep(random.randint(1,2)) 
        cl_loginItem = self.loginItems['zfj']['user']
        cl_loginItem['resultprocess'] = '申请调整'   #不可更改
        cl_loginItem['operatingComments'] = '请求调整'  #
        cl_loginItem['applyReason'] = '非我辖区'  #调整原因
        cl_result = fileFandling(cl_loginItem).test_requestAdjustment()
        if cl_result:
            logging.info("*****7.移动端权属单位申请调整成功*****")
    
    #调整批示    
    def tiaoZhengPiShi(self):
        time.sleep(random.randint(1,2)) 
        dataItem = {}
        dataItem['resultprocess'] = "批准"
        dataItem['leaderComments'] = "批准了"
        tzpsOK = adjustmentApproval(dataItem).adjustmentApprovalDetail()
        if tzpsOK != False:
            logging.info("*****8.web端调整批示成功(%s)*****"%dataItem['resultprocess'])


    #待调整（相当于派发）
    def daiTiaoZheng(self):
        time.sleep(random.randint(1,2)) 
        dtz_dataItem = self.loginItems['zfj']['user']
        outDir = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        dtz_dataItem['resultprocess'] = "派发"
        dtz_dataItem['limittime'] = outDir
        dtz_dataItem['operatingComments'] = "尽快处理"
        #待调整列表url
        dtz_dataItem['pflist_url'] = getConstant.dtz_ListUrl
        dtz_dataItem['pf_url'] = getConstant.pf_url
        paifa_result = distribution(dtz_dataItem).test_sendDetailsAndSendOut()
        if paifa_result:
            logging.info("*****9.web调整完毕*****")

    # 处理 移动端执法局apk处理 
    def chuLis(self):
        time.sleep(random.randint(1,2)) 
        cl_loginItem = self.loginItems['zfj']['user']
        cl_loginItem['resultprocess'] = '处理结束'
        cl_loginItem['operatingComments'] = '处理完成11'
        cl_picpath1 = "E:/test/dcms/ChengGuan/testFile/img/15.png"
        cl_picpath2 = "E:/test/dcms/ChengGuan/testFile/img/18.png"
        cl_loginItem['imgPath'] = [cl_picpath1,cl_picpath2]
        cl_result = fileFandling(cl_loginItem).test_app_handlingDetailsAndHandling()
        if cl_result:
            logging.info("*****10.移动端权属单位处理完毕*****")
    
    # 回访 web回访
    def huiFang(self):
        hfItem = {}
        hfItem['resultprocess'] = '回访通过'
        hfItem['operatingComments'] = '回访用户很满意。'
        hfItem['oderNumber'] = self.oderNumber
        ff_result = reviewAndReturnVisit(hfItem).test_returnDetailsAndVisit()
        if ff_result:
            logging.info("*****11.web端回访完毕*****")
        else:
            logging.info("XXXXXXXXXX11.web端回访失败XXXXXXXXXX")

    
    @classmethod
    def tearDownClass(cls): 
        logging.info("***流程结束***")
        

    def test_liucheng_15(self):
        self.oderNumber = '201902280011'
        for i in range(1):
            # self.gongDan()
            # self.queRen()
            # self.heShi()
            #self.liAn()
            #self.paiFa()
            #self.chuLi()
            self.huiFang()


    

# if __name__=="__main__":
    
#     unittest.main()
    