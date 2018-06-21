# #encoding=utf-8 

# import requests
# import json  
# import unittest
# import urllib, sys
# import config
# from config.Log import *

# class MyTest(unittest.TestCase):     #封装测试环境的初始化和还原的类  
#     def setUp(self):                 #放对数据可操作的代码，如对mysql、momgodb的初始化等,这里不对数据库进行操作！  
#             print("start test")  
#             pass  
#     def tearDown(self):             #与setUp()相对  
#             print("end test")  
#             pass  
# class test_xxx_get(MyTest):         #把这个接口封装一个类，下面的方法是具体的测试用例  
#     '''''接口名称：新增承包商'''    #这个描述接口名称  
#     def test_xxx_get(self):  
#         '''''测试用例1：新增承包商'''   #这个描述接口用例名称  
#         self.url = 'http://219.149.226.180:7880/jcjs/cor/saveorupdate.action'  #请求url  
#         self.headers = {"Content-Type":"application/x-www-form-urlencoded "}  
#         self.data = {                                   #请求参数  
#             'cbfbh':'测试编号1',
#             'cbfmc':'测试名称1',
#             'cbfgsdz':'测试地址1',
#             'cbffzr':'测试联系人1',
#             'cbffzrdh':13021979651,
#             'cbffrxm':"测试法人1",
#             'cbffrdh':130219796511,
#             'cbfxkztp':"/image/20180509/5ab600bc104a4698b3be8034ce1ef75a.jpeg",
#             'cbfxkzbh':123,
#             'id':''                 
#         }   #self.用在方法属性中，表示是该方法的属性，不会影响其他方法的属性。                                       
#         self.r = requests.post(url = self.url,data = self.data,headers = self.headers)
# #         return r.json()
# #         response = requests.post( self.r) 
# #         data = response.json()
#         print(self.r.text)
#         print(self.r.status_code)
#         self.assertIn("1",self.r.text)
#         logging.info(self.r.text) 
# #         self.assertIn("true",self.a.text)#断言判断接口返回是否符合要求，可以写多个断言！    
          
# if __name__=="__main__":  
#         unittest.main()
