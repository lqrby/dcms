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
from processSet import ProcessSet 


class MyTest(unittest.TestCase):     #封装测试环境的初始化和还原的类  
    @classmethod
    def setUpClass(cls): #放对数据可操作的代码，如对mysql、momgodb的初始化等,这里不对数据库进行操作！  
        # 初始化移动端登录人员集合对象
        cls.loginItems = writeAndReadTextFile().test_read_appLoginResult()
        #获取cookies
        cls.cookies = writeAndReadTextFile().test_readCookies()


    
    def test_liucheng_1(self):
        """
        pc端工单录入
        """
        # 用户对象
        zfjUser = self.loginItems['zfj']['user']
        wgyUser = self.loginItems['wggly']['user']
        qsdwUser = self.loginItems['qsdw']['user']
        smUser = self.loginItems['sm']['result']
        
        hsfhUser = zfjUser
        chuliUser = qsdwUser
        # 工单上报
        processOBJ = ProcessSet()
        hsfhUser['needconfirm'] = getConstant.NEEDCONFIRM_YES #是否核实
        hsfhUser['isFh'] = getConstant.ISFH_YES #是否复核
        gongdan = processOBJ.gongDan(hsfhUser)
        if gongdan:
            print("请您耐心等待大约一分钟......")
            time.sleep(random.randint(50,60))
            self.oderid = colligateQuery(gongdan).selectOder()
            if self.oderid:
                print("成功获取上报案卷单号:{}".format(self.oderid))   

                # 案卷核实[wggly,zfj]
                hsfhUser['oderNumber'] = self.oderid
                chuliUser['oderNumber'] = self.oderid

                heshi = processOBJ.heShi(hsfhUser)
                if heshi:
                    time.sleep(random.randint(5,8))
                    lian = processOBJ.liAn(self.oderid)
                    if lian:
                        time.sleep(random.randint(5,8))
                        paifa = processOBJ.paiFa(qsdwUser)
                        if paifa:
                            time.sleep(random.randint(5,8))
                            chuli = processOBJ.chuLi(chuliUser) # 权属单位处理
                            if chuli:
                                time.sleep(random.randint(5,8))
                                fuhe = processOBJ.fuHe(hsfhUser) # 复核
                                if fuhe:
                                    print("流程走完啦，帅呆了！！！")




    
    

    
    
    


    
    



    
    



    


    



    
    

    


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
    
    