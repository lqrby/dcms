# -*- coding: utf-8 -*-#encoding=utf-8
#from config.Log import *
import requests
import json  
import unittest
import urllib, sys,io
import config
from config.Log import logging
class MyTest(unittest.TestCase):     #封装测试环境的初始化和还原的类  
    def setUp(self):                 #放对数据可操作的代码，如对mysql、momgodb的初始化等,这里不对数据库进行操作！  
            print("start test")  
            pass  
    def tearDown(self):             #与setUp()相对  
            print("end test")  
            pass  
class test_zfj_post(MyTest):         #把这个接口封装一个类，下面的方法是具体的测试用例  
    '''''接口名称：app_执法局_江城集市'''    #这个描述接口名称  
    def test_jcjs_down(self): 
            '''''测试用例2：江城集市处上报_执法局处理'''   #这个描述接口用例名称   
            self.url = 'http://219.149.226.180:7880/jcjs/cp_io/saveorupdate.action'  #请求url  
            self.headers = {"Content-Type":"application/x-www-form-urlencoded "}  
            self.data = {                                   #请求参数  
            'tstwbh'  :  '1313',
            'tsxxms'   :'江城集市上报',
            'tsly'    :'3',
            'tsrid'    :'29',
            'tsscid'    :'23',
            'tsrdh'    :'13021979651',
            'scmc'    :'测试市场1',
            'tstwdz' :   '吉林市 昌邑区',
            'tsfjtp':    '/image/20180511/00ea49d3fa2d4dd48d8ad735e1a321aa.jpeg',
            'tsrxm':    '管理李泽林测试1市场'
            }   #self.用在方法属性中，表示是该方法的属性，不会影响其他方法的属性。                                       
            self2 = requests.post(url = self.url,data = self.data,headers = self.headers,timeout=60)
            a=self2.text
            b =json.loads(a)
            c=str(b['status'])
            if c=="1":
                print("江城集市上报成功:"+self2.text)
                logging.info("江城集市上报成功"+self2.text)
            else: 
                logging.info("江城集市上报失败"+self2.text)
                print("江城集市上报失败"+self2.text)
                print(self2.status_code)
                raise Exception(self2.status_code+"抛出一个异常")      
              #获取执法局江城集市所有未处理数据
            url = "http://219.149.226.180:7880/jcjs/cp_io/getscbrycpiolist.action?rwssjssj=&curPage=1&scbryid=4028838462ae48f70162b28604ee014a&zxzts=2&rwsskssj=&pageSize=15"
            self_data = urllib.request.urlopen(url)
            self3 = self_data.read()
            #转换成字典
            self2=json.loads(self3)
            print(self3) 
            #取首行案卷pfryid和tsid
            a=self2['result']['list'][0]['pfryid']
            b=str(a)
            c=self2['result']['list'][0]['id']
            d=str(c) 
            self.url1 = 'http://219.149.226.180:7880/jcjs/elpy_tk/saveorupdate.action'  #请求url  
            self.headers1 = {"Content-Type":"application/x-www-form-urlencoded "}  
            self.data1 = {                                   #请求参数  
                'pfry':'李泽林市场领导',
                'pfzt':2,
                'id':'',    
                'pftp':'/image/20180517/2dd44faaa7c64d418dfdce48abda4cbf.jpeg',
                'pfyj':'测试',
                'zxzt':'1',
                'pfryid':b,
                'tsid':d
            }   #self.用在方法属性中，表示是该方法的属性，不会影响其他方法的属性。                                     
            r1 = requests.post(url = self.url1,data = self.data1,headers =self.headers1,timeout=60)     
            a=r1.text 
            b2 =json.loads(a)
            c2=str(b2['status'])
            if c2=="1":
                print("执法局处理成功"+r1.text)
                logging.info("执法局处理成功"+r1.text)
            else: 
                logging.info("执法局处理失败"+r1.text)
                print("执法局处理失败"+r1.text) 
                raise Exception(r1.text+"抛出一个异常")           
if __name__=="__main__":  
        unittest.main()
