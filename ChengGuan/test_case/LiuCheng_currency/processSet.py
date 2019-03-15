# -*- coding: utf-8 -*-
import unittest
import sys
sys.path.append("E:/test/dcms/ChengGuan")
import time,random,json,datetime
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
from fuHeAndHuiFang import reviewAndReturnVisit
from common.writeAndReadText import writeAndReadTextFile
from common.constant_all import getConstant
from zongHeChaXun import colligateQuery

class ProcessSet():
    def __init__(self):
        # self.oderNumber = oderNumber
        if '180' in getConstant.IP:
            self.ip = getConstant.IP+getConstant.PORT_7897
        else:
            self.ip = getConstant.IP
        self.header = {
            "User-Agent":"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36",
            "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
            "Accept-Encoding":"gzip, deflate",
            "Accept-Language":"zh-CN,zh;q=0.9,en;q=0.8",
            "Cookie":writeAndReadTextFile().test_readCookies()
        }
        self.keywords = writeAndReadTextFile().test_read_systemId('呼叫系统')
        # 初始化移动端登录人员集合对象
        self.loginItems = writeAndReadTextFile().test_read_appLoginResult()
        #获取cookies
        self.cookies = writeAndReadTextFile().test_readCookies()


    def gongDan(self,userItem):
        """
        pc端工单录入
        """
        time.sleep(random.randint(2,4))
        markPath = getConstant.PROJECT_PATH+"/common/numberMark.txt"
        mark = writeAndReadTextFile().test_read_txt(markPath)
        dict_mark = json.loads(mark)
        number = int(dict_mark['web_sb'])+1
        orderData = {}
        # userItem = self.loginItems['wggly'] #网格管理员
        picpath = "E:/test/dcms/ChengGuan/testFile/img/1.png"
        img_value = ('1.png', open(picpath,'rb'),'multipart/form-data')
        orderData['mposl'] = '14088659.985423975'
        orderData['mposb'] = '5442040.762812978'
        orderData['menuId'] = '402880822f9490ad012f949eb313008a'
        orderData['isFh'] = userItem['isFh']
        orderData['street'] = '220204002'
        orderData['p_name'] = '董楚楚'
        orderData['p_sex'] = '女'
        orderData['p_job'] = '教师'
        orderData['p_phone'] = '0102864987'
        orderData['other_phone'] = '15866993322'
        orderData['feedback'] = '手机'
        orderData['source'] = '402880822f47692b012f4774e5710010'  #案卷来源
        orderData['eorc'] = getConstant.EORCID_SJ   #案卷类型
        orderData['eventtypeone'] = getConstant.SJ_XCGG   #事件大类
        orderData['eventtypetwo'] = getConstant.SJ_XCGG_FFXGG  #小类
        orderData['regioncode'] = '220204'
        orderData['bgcode'] = '220204002'
        orderData['bgadminid'] = userItem['id']
        orderData['bgadminid2'] = userItem['name']
        orderData['gridid'] = '220204002003'
        orderData['needconfirm'] = userItem['needconfirm']
        orderData['description'] = '流程一，非法小广告'+str(number)
        orderData['dealWay'] = 'on'
        orderData['fieldintro'] = '吉林市 船营区 南京街道 怀德社区'
        orderData['upload'] = img_value
        gdlr_res = submitOrder(orderData).test_web_submitOrder()
        if gdlr_res:
            dict_mark["web_sb"] = str(number)
            writeAndReadTextFile().test_write_txt(markPath,json.dumps(dict_mark))
            logging.info("3.web工单录入完毕")
            return {'description':number}


    
    def anJuanShangBao_zfj(self,orderData):
        """
        执法局apk上报案卷
        """
        time.sleep(random.randint(1,3)) 
        markPath = getConstant.PROJECT_PATH+"/common/numberMark.txt"
        mark = writeAndReadTextFile().test_read_txt(markPath)
        dict_mark = json.loads(mark)
        number = int(dict_mark['zfj_sb'])+1
        # orderData = self.loginItems['zfj']['user']
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


    
    def anJuanShangBao_xjsb(self,orderData):
        """
        执法局apk 》巡检上报案卷
        """
        time.sleep(random.randint(1,3)) 
        markPath = getConstant.PROJECT_PATH+"/common/numberMark.txt"
        mark = writeAndReadTextFile().test_read_txt(markPath)
        dict_mark = json.loads(mark)
        number = int(dict_mark['zfj_sb'])+1
        # orderData = self.loginItems['zfj']['user']
        orderData['fieldintro'] = '吉林市 市管主街路 越山路 越山路 越山路（沙河子广场-解放中路）'
        orderData['gridid'] = '22029904000101'
        orderData['description'] = '流程五，建筑垃圾,渣土管理'+str(number)
        orderData['mposl'] = '14086190.785638873'
        orderData['mposb'] = '5441341.7074305825'
        res = submitOrder(orderData).test_app_reportInspection()
        if res:
            dict_mark["zfj_sb"] = str(number)
            writeAndReadTextFile().test_write_txt(markPath,json.dumps(dict_mark))
            logging.info("*****3.%s上报案卷完毕*****"%orderData['name'])
            return {'description':number}
        else:
            logging.info("XXXXXXXXXX3.执法局%s上报案卷失败XXXXXXXXXX"%orderData['name'])


    def anJuanShangBao_wggly(self,orderData):
        """
        网格管理员apk 》案卷上报
        """
        time.sleep(random.randint(1,3)) 
        markPath = getConstant.PROJECT_PATH+"/common/numberMark.txt"
        mark = writeAndReadTextFile().test_read_txt(markPath)
        dict_mark = json.loads(mark)
        number = int(dict_mark['wggly_sb'])+1
        # orderData = self.loginItems['wggly']['user']
        orderData['eorcid'] = getConstant.EORCID_BJ #事部件类型 
        orderData['fieldintro'] = '吉林市 高新开发区 高新开发区街道 恒厦社区 恒厦社区第九网格'
        orderData['mposl'] = '14088524.212997204'
        orderData['description'] = "流程四，道路不干净，环境脏乱差"+str(number)
        orderData['eventtypeoneId'] = getConstant.BJ_JTSS #大类  市容环境
        orderData['gridid'] = '22020600100109'
        # orderData['bgadminId'] =  #上报人id
        orderData['eventtypetwoId'] = getConstant.BJ_JTSS_DXTD #小类   道路不洁
        orderData['mposb'] = '5437559.658689937'
        sb_picpath1 = "E:/test/dcms/ChengGuan/testFile/img/26.png"
        sb_picpath2 = "E:/test/dcms/ChengGuan/testFile/img/27.png"
        orderData['imgPath'] = [sb_picpath1,sb_picpath2]
        res = submitOrder(orderData).test_app_submitOrder()
        if res:
            dict_mark["wggly_sb"] = str(number)
            writeAndReadTextFile().test_write_txt(markPath,json.dumps(dict_mark))
            logging.info("*****3.%s上报案卷完毕*****"%orderData['name'])
            return {'description':number}
        else:
            logging.info("XXXXXXXXXX3.%s执法局上报案卷失败XXXXXXXXXX"%orderData['name'])
              


    
    def anJuanShangBao_sm(self,orderData):
        """
        市民apk案卷上报
        """
        time.sleep(random.randint(1,3))
        markPath = getConstant.PROJECT_PATH+"/common/numberMark.txt"
        mark = writeAndReadTextFile().test_read_txt(markPath)
        dict_mark = json.loads(mark)
        number = int(dict_mark['sm_sb'])+1
        # orderData = self.loginItems['sm']['result']
        orderData['longitude'] = '14090823.883200558'
        orderData['latitude'] = '5446737.409308622'
        orderData['complaincontent'] = '流程二，设施脏污'+str(number) #描述
        orderData['bgcode'] = '220202003001' #网格
        orderData['bgcodename'] = '锦东社区' #地址
        orderData['gridid'] = '220202003001'
        orderData['wxsource'] = 'GZHJB'
        orderData['imgurl'] = '/image/20181008/f7bffd2e16154c8f817f5fc1b442f21d.jpg'
        orderData['eorcid'] = getConstant.EORCID_SJ
        orderData['eventoneid'] = getConstant.SJ_SGGL
        orderData['eventtwoid'] = getConstant.SJ_SGGL_WZJL
        res = submitOrder(orderData).test_app_sm_submitOrder()
        if res:
            dict_mark["sm_sb"] = str(number)
            writeAndReadTextFile().test_write_txt(markPath,json.dumps(dict_mark))
            logging.info("*****3.市民上报案卷完毕*****")
            return {'description':number}



    
    def queRen(self,userItem):
        """
        web端坐席确认案卷
        """
        time.sleep(random.randint(1,3))
        # dataObject = self.loginItems['zfj']['user']#核实人
        # userItem['oderNumber'] = self.oderNumber #工单号
        userItem['eorcId'] = getConstant.EORCID_SJ #事件
        userItem['eventtypeoneId'] = getConstant.SJ_SGGL #大类
        userItem['eventtypetwoId'] = getConstant.SJ_SGGL_WZJL #小类
        userItem['regioncodeId'] = '220206' #高新开发区
        userItem['bgcodeId'] = '220206001' #高新开发区街道	
        # dataObject['gridId'] = '22020600100706' #万米网格
        # dataObject['fieldintro'] = '吉林市 高新开发区 高新开发区街道 日升社区 日升社区第六网格' #位置描述
        userItem['needconfirm'] = getConstant.NEEDCONFIRM_YES #核实
        userItem['isFh'] = getConstant.ISFH_YES #复核
        qr_picpath = "E:/test/dcms/ChengGuan/testFile/img/36.png"
        qr_img = ('img.png', open(qr_picpath,'rb'),'multipart/form-data')
        userItem['upload'] = qr_img
        qr_res = confirm(userItem).test_web_UnconfirmedDetail()
        if qr_res:
            logging.info("*****4.web确认案卷完毕*****")
            return True



    #执法局核实案卷(移动端)
    def heShi(self,userItem):
        """
        #移动端apk核实案卷
        """
        time.sleep(random.randint(1,2))
        # loginItem_hs = self.loginItems['zfj']
        hs_picpath1 = "E:/test/dcms/ChengGuan/testFile/img/10.png"
        hs_picpath2 = "E:/test/dcms/ChengGuan/testFile/img/11.png"
        # userItem['oderNumber'] = self.oderNumber #工单号
        userItem['imgPath'] = [hs_picpath1,hs_picpath2]
        userItem['casestateid'] = getConstant.HSYX
        hs_res = verify(userItem).test_app_daiHeShiDetail()
        if hs_res:
            logging.info("*****5.执法局核实案卷完毕(%s)*****"%(userItem['oderNumber']))
            return True


    def liAn(self,oderNumber):
        """
        web端坐席立案
        """
        time.sleep(random.randint(1,3)) 
        lianData = {}
        lianData['oderNumber'] = oderNumber
        lianData['resultprocess'] = "立案"
        lianData['operatingComments'] = "批准立案"
        lian_result = setUpCase(lianData).test_detailsAndFiling()
        if lian_result:
            logging.info("4.web立案完毕")
            return True
        else:
            logging.info("XXXXXXXXXXXXXXXX4.web立案失败XXXXXXXXXXXXXXX")



    def paiFa(self,userItem):
        """
        web端坐席派发 》派发
        """
        time.sleep(random.randint(1,2))
        # userItem = self.loginItems['qsdw']['user']
        # userItem['oderNumber'] = self.oderNumber #工单号
        userItem['resultprocess'] = "派发"
        userItem['limittime'] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        userItem['operatingComments'] = "尽快处理"
        #待派发列表url
        userItem['pflist_url'] = getConstant.dpf_ListUrl
        #派发url
        userItem['pf_url'] = getConstant.pf_url
        paifa_result = distribution(userItem).test_sendDetailsAndSendOut()
        if paifa_result:
            logging.info("*****7.web派发完毕*****")
            return True
        


    def paiFa_guaQi(self,userItem): 
        """
        web端坐席派发 》挂起
        """
        time.sleep(random.randint(1,2))  
        # pf_loginItem = self.loginItems['qsdw']['user']
        outDir = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        # userItem['oderNumber'] = self.oderNumber
        userItem['resultprocess'] = "挂账"
        userItem['limittime'] = outDir
        userItem['operatingComments'] = "先挂起，暂时不知道派发部门"
        #待派发列表url
        userItem['pflist_url'] = getConstant.dpf_ListUrl
        #派发url
        userItem['pf_url'] = getConstant.pf_url
        paifa_result = distribution(userItem).test_sendDetailsAndSendOut()
        if paifa_result:
            logging.info("5.web挂起完毕")
            return True

    
    def huiFu(self):
        """
        web端坐席挂账》恢复
        """
        time.sleep(random.randint(1,2)) 
        gzItem = {}
        # gzItem['oderNumber'] = self.oderNumber
        gzItem['resultprocess'] = '恢复'
        gzItem['operatingComments'] = '恢复案卷流程'
        gz_res = hangUp(gzItem).test_hangUpDetail()
        if gz_res:
            logging.info("6.web挂账案卷恢复成功")
            return True


    # 处理 移动端权属单位apk处理 
    def chuLi(self,userItem):
        """
        移动端apk处理 [zfj,qsdw]
        """
        time.sleep(random.randint(1,2)) 
        # cl_loginItem = self.loginItems['qsdw']['user']
        userItem['resultprocess'] = '处理结束'
        userItem['operatingComments'] = '处理完成1'
        cl_picpath1 = "E:/test/dcms/ChengGuan/testFile/img/9.png"
        cl_picpath2 = "E:/test/dcms/ChengGuan/testFile/img/28.png"
        userItem['imgPath'] = [cl_picpath1,cl_picpath2]
        cl_result = fileFandling(userItem).test_app_handlingDetailsAndHandling()
        if cl_result:
            logging.info("8.移动端权属单位处理完毕")
            return True

    # 复核 网格管理员apk复核 
    def fuHe(self,userItem):
        """
        移动端apk复核[zfj,gly]
        """
        time.sleep(random.randint(1,3)) 
        fh_picpath1 = "E:/test/dcms/ChengGuan/testFile/img/6.png"
        fh_picpath2 = "E:/test/dcms/ChengGuan/testFile/img/7.png"
        # fh_loginUser = self.loginItems['wggly']['user']
        # userItem['oderNumber'] = self.oderNumber
        userItem['casestateid'] = getConstant.FHYX  #复核通过、复核不通过
        userItem['checkdesc'] = '经复核有效'
        userItem['imgPath'] = [fh_picpath1,fh_picpath2]
        fh_result = reviewAndReturnVisit(userItem).test_app_returnDetailsAndVisit()
        if fh_result:
            logging.info("9.移动端网格管理员复核完毕")
            return True
    

    


    # def test_liucheng_1(self):
    #     for i in range(1):
    #         # 上报描述编号
    #         loginItems = self.gongDan()  
    #         if loginItems:
    #             print("请您耐心等待大约一分钟......")
    #             time.sleep(random.randint(50,60))
    #             oderid = colligateQuery(loginItems).selectOder()
    #             if oderid:
    #                 self.oderNumber = oderid
    #                 print("成功获取上报案卷单号:{}".format(self.oderNumber))
    #                 lianRes = self.liAn()
    #                 if lianRes:
    #                     time.sleep(random.randint(5,8))
    #                     pfgq = self.paiFa_guaQi()
    #                     if pfgq:
    #                         time.sleep(random.randint(5,8))
    #                         huifu = self.huiFu()
    #                         if huifu:
    #                             time.sleep(random.randint(5,8))
    #                             paifa = self.paiFa()
    #                             if paifa:
    #                                 time.sleep(random.randint(5,8))
    #                                 chuli = self.chuLi()
    #                                 if chuli:
    #                                     time.sleep(random.randint(5,8))
    #                                     fuhe = self.fuHe()
    #                                     if fuhe:
    #                                         print("流程走完啦，帅呆了！！！")


            

    # def test_singleStep(self):
    #     self.oderNumber = '201903140010'
    #     # self.liAn()
    #     # self.paiFa_guaQi()
    #     # self.huiFu()
    #     # self.paiFa()
    #     # self.chuLi()
    #     self.fuHe()

    @classmethod
    def test_tearDownClass(cls): 
        # cls.driver.quit()            #与setUp()相对y  
        logging.info("***流程结束***")

if __name__=="__main__":
    unittest.main()
    
    