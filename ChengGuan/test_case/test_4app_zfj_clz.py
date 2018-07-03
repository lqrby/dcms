# # -*- coding: utf-8 -*-
# #from config.Log import *
# import requests
# import json  
# import unittest
# import urllib, sys
# import config
# from config.Log import logging
# class MyTest(unittest.TestCase):     #封装测试环境的初始化和还原的类  
#     def setUp(self):                 #放对数据可操作的代码，如对mysql、momgodb的初始化等,这里不对数据库进行操作！  
#             print("start test")  
#             pass  
#     def tearDown(self):             #与setUp()相对  
#             print("end test")  
#             pass  
# class test_zfj_post(MyTest):         #把这个接口封装一个类，下面的方法是具体的测试用例  
#     '''''接口名称：app_执法局_江城集市'''    #这个描述接口名称  
#     def test_jcjs_down(self): 
#         '''''测试用例4：非市场办执法局上报_执法局市场办派发_江城集市处理'''   #这个描述接口用例名称   
#         url3 = 'http://219.149.226.180:7880/jcjs/cp_io/saveorupdate.action'  #请求url  
#         headers3 = {"Content-Type":"application/x-www-form-urlencoded "}  
#         data3 = {                                   #请求参数  
#            'tstwbh' :   12,
#            'tsxxms'  :  '执法局上报',
#             'tsly'   : 4,
#             'tsrid'   : '4028838462ae48f70162ae9426b8003d',
#              'tsscid'  :  23,
#              'tsrdh'   : 13021979651,
#              'tstwdz'   : '李泽林测试1',
#              'tsfjtp'    :'/image/20180510/8ce9561d52e44adebbbefd761708c328.jpeg',
#              'tsrxm'    :'李泽林1'
#         }   #self.用在方法属性中，表示是该方法的属性，不会影响其他方法的属性。                                       
#         r = requests.post(url =url3 ,data = data3,headers = headers3,timeout=60) 
#         a=r.text 
#         b=json.loads(a)
#         c=str(b['status'])
#         if c=="1":
#             print("非市场办执法局上报成功"+r.text)
#             logging.info("非市场办执法局上报成功"+r.text)
#         else: 
#             logging.info("非市场办执法局上报失败"+r.text)
#             print("非市场办执法局上报失败"+r.text)
#             raise Exception(r.text)
#         url="http://219.149.226.180:7880/jcjs/cp_io/getscbrycpiolist.action?rwssjssj=&curPage=1&scbryid=4028838462ae48f70162b28604ee014a&zxzts=1&rwsskssj=&pageSize=15"
#         self_data = urllib.request.urlopen(url,timeout=60)
#         self3 = self_data.read()
#         #转换成字典
#         self2=json.loads(self3)
#         #取首行案卷tsid
#         a=self2['result']['list'][0]['id']
#         b=str(a)
#         #执法局派发
#         url1 = 'http://219.149.226.180:7880/jcjs/elpy_tk/saveorupdate.action'  #请求url  
#         headers1 = {"Content-Type":"application/x-www-form-urlencoded "}  
#         data1 = {                                   #请求参数  
#             'pfry':'李泽林市场领导',
#             'pfzt':2,
#             'id':'',   
#             'pftp':'',
#             'pfyj':'ink哦咯',
#             'zxzt':1,
#             'pfryid':'4028838462ae48f70162b28604ee014a',
#             'tsid':a
#         }   #self.用在方法属性中，表示是该方法的属性，不会影响其他方法的属性。                                     
#         r1 = requests.post(url = url1,data = data1,headers =headers1,timeout=60)      
#         a1=r1.text 
#         b1=json.loads(a1)
#         c1=str(b1['status'])
#         if c1=="1":
#             print("执法局派发成功"+r1.text)
#             logging.info("执法局派发成功"+r1.text)
#         else: 
#             logging.info("执法局派发成功"+r1.text)
#             print("执法局派发成功"+r1.text)
#             raise Exception(r1.text) 
#         #获取江城集市所有未处理数据
#         url2 = "http://219.149.226.180:7880/jcjs/elpy_tk/getlistbypage.action?rwssjssj=&curPage=1&zxzt=1&rwsskssj=&ygid=29&pageSize=15"
#         data4 = urllib.request.urlopen(url2)
#         self3 = data4.read()
#         #转换成字典
#         self2=json.loads(self3)
#         logging.info(self2)
#         #取首行案卷id和tsid
#         a=self2['result']['list'][0]['id']
#         b=str(a)
#         c=self2['result']['list'][0]['tsid']
#         d=str(c)           
#          #江城集市处理
#         url4 = 'http://219.149.226.180:7880/jcjs/elpy_tk/saveorupdate.action'  #请求url  
#         headers4 = {"Content-Type":"application/x-www-form-urlencoded "}  
#         data4 = {                                   #请求参数  
#                 'zxzt':2,
#                 'pfzt':2,
#                 'fjyj':"测试描述1",
#                 'fjtp':"/image/20180517/8d7817e420ed44c48f02131dcb177dbb.jpeg",
#                 'id':b,
#                 'tsid':d
#             }   #self.用在方法属性中，表示是该方法的属性，不会影响其他方法的属性。                                    
#         r2 = requests.post(url = url4,data = data4,headers =headers4,timeout=60)     
#         a2=r2.text 
#         b2=json.loads(a2)
#         c2=str(b2['status'])
#         if c2=="1":
#             print("江城集市处理成功"+r2.text)
#             logging.info("江城集市处理成功"+r2.text)
#         else: 
#             logging.info("江城集市处理失败"+r2.text)
#             print("江城集市处理失败"+r1.text) 
#             raise Exception(r1.text)
# if __name__=="__main__":  
#         unittest.main()
