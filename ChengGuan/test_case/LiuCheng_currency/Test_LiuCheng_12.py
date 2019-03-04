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
        
        # 初始化移动端登录人员集合对象
        cls.loginItems = writeAndReadTextFile().test_read_appLoginResult()
        #获取cookies
        cls.cookies = writeAndReadTextFile().test_readCookies()

    
    #移动端市民上报案卷
    def test_03gongDan_lc2(self):
        time.sleep(random.randint(1,3))
        markPath = getConstant.PROJECT_PATH+"/common/numberMark.txt"
        mark = writeAndReadTextFile().test_read_txt(markPath)
        dict_mark = json.loads(mark)
        number = int(dict_mark['sm_sb'])+1
        orderData = self.loginItems['sm']["result"]
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
    def test_4queRen_lc5(self):
        time.sleep(random.randint(1,3))
        loginUser = self.loginItems['wggly']['user']#核实人
        dataObject = {}
        dataObject['loginUser'] = loginUser
        dataObject['eorcId'] = getConstant.EORCID_BJ #部件
        dataObject['eventtypeoneId'] = getConstant.BJ_GGSS #大类
        dataObject['eventtypetwoId'] = getConstant.BJ_GGSS_RLJG #小类
        dataObject['regioncodeId'] = '220299' #高新开发区
        dataObject['bgcodeId'] = '220299040' #高新开发区街道	
        # dataObject['gridId'] = '22020600100706' #万米网格
        # dataObject['fieldintro'] = '吉林市 高新开发区 高新开发区街道 日升社区 日升社区第六网格' #位置描述
        dataObject['needconfirm'] = getConstant.NEEDCONFIRM_YES #核实
        dataObject['isFh'] = getConstant.ISFH_NO #复核
        qr_picpath = "E:/test/dcms/ChengGuan/testFile/img/35.png"
        qr_img = ('img.png', open(qr_picpath,'rb'),'multipart/form-data')
        dataObject['upload'] = qr_img
        webqueren_res = confirm(dataObject).test_web_UnconfirmedDetail()
        if webqueren_res:
            logging.info("4.web确认案卷完毕")

    #网格管理员核实案卷(移动端)(核实无效)
    def test_5heShi_lc5(self):
        time.sleep(random.randint(1,2))
        loginItem_hs = self.loginItems['wggly']['user']
        loginItem_hs['casestateid'] = getConstant.HSYX
        hs_picpath1 = "E:/test/dcms/ChengGuan/testFile/img/33.png"
        hs_picpath2 = "E:/test/dcms/ChengGuan/testFile/img/34.png"
        loginItem_hs['casestateid'] = getConstant.HSWX
        loginItem_hs['imgPath'] = [hs_picpath1,hs_picpath2]
        hs_res = verify(loginItem_hs).test_app_daiHeShiDetail()
        if hs_res:
            logging.info("5.网格管理员核实案卷完毕(核实无效)")

    @classmethod
    def tearDownClass(cls): 
        logging.info("***流程结束***")

if __name__=="__main__":
    unittest.main()