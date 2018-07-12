# # -*- coding: utf-8 -*-
# import requests
# #from selenium import webdriver
# import json  
# import unittest
# import urllib, sys, io
# import time
# import config
# from config.Log import logging
# sys.stdout = io.TextIOWrapper(sys.stdout.buffer,encoding='utf-8')
# #driver = webdriver.Chrome("D:/python/chromeDriverSever/chromedriver.exe")
# class MyTest(unittest.TestCase):    #封装测试环境的初始化和还原的类  
#     def setUp(self):     #放对数据可操作的代码，如对mysql、momgodb的初始化等,这里不对数据库进行操作！  
#             print("start test")
#             pass  
#     def tearDown(self):     #与setUp()相对  
#             print("end test")  
#             pass 
# '''''接口名称：web_城管系统_工单录入事件'''             
# class test_web_hjxt_entry(MyTest):   #把这个接口封装一个类，下面的方法是具体的测试用例  
#     '''''测试用例1：工单录入'''
#     def test_web_hjxt_entry(self):  #def test_jcjs_cl_post(self): 工单录入的方法
#         time.sleep(2)
#         #elem=driver.find_element_by_xpath('/html/body/div[1]/div[2]/div/div[1]/div[2]/a[7]/div[1]/img').click()
#            #这个描述接口用例名称 
#         self.url = 'http://219.149.226.180:7897/dcms/bmsAdmin/Admin-subsystem.action'
#         self.headers = {"Content-Type":"application/x-www-form-urlencoded "}  
#         self.data = { #请求参数  
#             'systemId' : '402880ea2f6bd924012f6c521e8c0034', #这是pc端登录人员的id
#         }   #self.用在方法属性中，表示是该方法的属性，不会影响其他方法的属性。
                                          
#         self.r = requests.post(url = self.url,data = self.data,headers = self.headers,timeout=30)         
#         a=self.r.text 
#         b =json.loads(a)
#         c=str(b['sysId'])
#         if c=="1":
#             print("执法局下派成功"+self.r.text)
#             logging.info("执法局下派成功"+self.r.text)
#         else: 
#             logging.info("执法局下派失败"+self.r.text)
#             print("执法局下派失败"+self.r.text) 
#             # raise Exception(self.r.text+"抛出一个异常")         
#         #获取江城集市所有未处理数据
#         url = "http://219.149.226.180:7880/jcjs/elpy_tk/getlistbypage.action?rwssjssj=&curPage=1&zxzt=1&rwsskssj=&ygid=29&pageSize=15"
#         self_data = urllib.request.urlopen(url,timeout=60)
#         self3 = self_data.read()
#         #转换成字典
#         self2=json.loads(self3)
#         #logging.info(self2)
#         #取首行案卷id和tsid
#         a=self2['result']['list'][0]['id']
#         b=str(a)
#         c=self2['result']['list'][0]['tsid']
#         d=str(c)
#         #江城集市处理
#         self.url1 = 'http://219.149.226.180:7880/jcjs/elpy_tk/saveorupdate.action'  #请求url  
#         self.headers1 = {"Content-Type":"application/x-www-form-urlencoded "}  
#         self.data1 = {#请求参数  
#             'zxzt':2,
#             'pfzt':2,
#             'fjyj':"测试描述1",
#             'fjtp':"/image/20180517/8d7817e420ed44c48f02131dcb177dbb.jpeg",
#             'id':b,
#             'tsid':d
#         }   #self.用在方法属性中，表示是该方法的属性，不会影响其他方法的属性。                                     
#         r2 = requests.post(url = self.url1,data = self.data1,headers =self.headers1,timeout=60)  
#         a=r2.text 
#         b =json.loads(a)
#         c=str(b['status'])
#         if c=="1":
#             print("江城集市处理成功"+r2.text)
#             logging.info("江城集市处理成功"+r2.text)
#         else: 
#             # logging.info("江城集市处理失败"+r2.text)
#             print("江城集市处理失败"+r2.text)
#             # raise Exception(r2.text+"抛出一个异常")    
# if __name__=="__main__":  
#         unittest.main()
