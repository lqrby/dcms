# -*- coding: utf-8 -*-
#from config.Log import *
import requests
import json  
import unittest
import urllib,sys

class MyTest(unittest.TestCase):     #封装测试环境的初始化和还原的类  
    def setUp(self):                 #放对数据可操作的代码，如对mysql、momgodb的初始化等,这里不对数据库进行操作！  
            print("start test")  
            pass  
    def tearDown(self):             #与setUp()相对  
            print("end test")  
            pass  
class test_zfj_post(MyTest):         #把这个接口封装一个类，下面的方法是具体的测试用例  
    '''''接口名称：app_爱吉林_江城集市_获取城市动态'''    #这个描述接口名称  
    def test_jcjs_down(self):  
        '''''测试用例6：app_爱吉林_江城集市_获取城市动态'''   #这个描述接口用例名称 
        url1 = 'http://219.149.226.180:7880/publicworkstation/jeecms/getNewsList.action?subId=59'  #请求url  
        headers1 = {"Content-Type":"application/x-www-form-urlencoded "}  
        data1 = {                                   #请求参数  
          'subId':59
         }
        r = requests.get(url =url1 ,data = data1,headers = headers1,timeout=60)
        r1=r.text
        b1=json.loads(r1)
        c1=str(b1['status'])
        if c1=="1":
                print("爱吉林城市动态获取成功"+r.text)
                #logging.info("爱吉林城市动态获取成功"+r.text)
        else:
                #logging.info("爱吉林城市动态获取失败"+r.text)
                print("爱吉林城市动态获取失败"+r.text)  
                raise Exception(r.text)
if __name__=="__main__":  
        unittest.main()