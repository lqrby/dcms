# -*- coding: utf-8 -*-
#from config.Log import *
import requests
import json  
import unittest
import urllib, sys

class MyTest(unittest.TestCase):     #封装测试环境的初始化和还原的类  
    def setUp(self):                 #放对数据可操作的代码，如对mysql、momgodb的初始化等,这里不对数据库进行操作！  
            print("start test")  
            pass  
    def tearDown(self):             #与setUp()相对  
            print("end test")  
            pass  
class test_zfj_post(MyTest):         #把这个接口封装一个类，下面的方法是具体的测试用例  
    '''''接口名称：app_爱吉林_江城集市'''    #这个描述接口名称  
    def test_jcjs_down(self):  
        '''''测试用例3：市场投诉_执法派发_江城集市处理'''   #这个描述接口用例名称 
        self.url = 'http://219.149.226.180:7880/publicworkstation/mktcp_io/saveComplaint.action'  #请求url  
        self.headers = {"Content-Type":"application/x-www-form-urlencoded "}  
        self.data = {                                   #请求参数  
        'tsrxm'  :  '李泽林',
        'tsrdh'  :  '13021979652',
        'tsrxb':  1,
        'tsscid':  23,
        'tstwdz':  '李泽林测试1',
        'tsxxms' : '测试',
        'tstwbh'  :  '1234',
        'tsfjtp'   : '/image/20180517/72f7c964fa304002993761fae2601187.jpg',
        'tsrid'   : 'c65ef0509d3c4f22814db04b49333eb7',
        'tsly'  :  1
        }   #self.用在方法属性中，表示是该方法的属性，不会影响其他方法的属性。                                       
        self2 = requests.post(url = self.url,data = self.data,headers = self.headers,timeout=60)
        a=self2.text 
        b =json.loads(a)
        c=str(b['status'])
        if c=="1":
            print("爱吉林上报成功"+self2.text)
            #logging.info("爱吉林上报成功"+self2.text)
        else: 
            #logging.info("爱吉林上报失败"+self2.text)
            print("爱吉林上报失败"+self2.text)
            raise Exception(self2.text)    
        url="http://219.149.226.180:7880/jcjs/cp_io/getscbrycpiolist.action?rwssjssj=&curPage=1&scbryid=4028838462ae48f70162b28604ee014a&zxzts=1&rwsskssj=&pageSize=15"
        self_data = urllib.request.urlopen(url)
        self3 = self_data.read()
        #转换成字典
        self2=json.loads(self3)
        #取首行案卷tsid
        a=self2['result']['list'][0]['id']
        b=str(a)
        #执法局派发
        url1 = 'http://219.149.226.180:7880/jcjs/elpy_tk/saveorupdate.action'  #请求url  
        headers1 = {"Content-Type":"application/x-www-form-urlencoded "}  
        data1 = {                                   #请求参数  
            'pfry':'李泽林市场领导',
            'pfzt':2,
            'id':'',   
            'pftp':'',
            'pfyj':'ink哦咯',
            'zxzt':1,
            'pfryid':'4028838462ae48f70162b28604ee014a',
            'tsid':a
        }   #self.用在方法属性中，表示是该方法的属性，不会影响其他方法的属性。                                     
        r1 = requests.post(url = url1,data = data1,headers =headers1,timeout=60)      
        a1=r1.text 
        b1 =json.loads(a1)
        c1=str(b1['status'])
        if c1=="1":
            print("执法局派发成功"+r1.text)
            #logging.info("执法局派发成功"+r1.text)
        else: 
            #logging.info("执法局派发失败"+r1.text)
            print("执法局派发失败"+r1.text) 
            raise Exception(r1.text)      
        #获取列表id
        #获取江城集市所有未处理数据
        url = "http://219.149.226.180:7880/jcjs/elpy_tk/getlistbypage.action?rwssjssj=&curPage=1&zxzt=1&rwsskssj=&ygid=29&pageSize=15"
        self_data = urllib.request.urlopen(url)
        self3 = self_data.read()
        #转换成字典
        self2=json.loads(self3)
#         logging.info(self2)
        #取首行案卷id和tsid
        a=self2['result']['list'][0]['id']
        b=str(a)
        c=self2['result']['list'][0]['tsid']
        d=str(c)              
         #江城集市处理
        self.url2 = 'http://219.149.226.180:7880/jcjs/elpy_tk/saveorupdate.action'  #请求url  
        self.headers2 = {"Content-Type":"application/x-www-form-urlencoded "}  
        self.data2 = {                                   #请求参数  
                'zxzt':2,
                'pfzt':2,
                'fjyj':"测试描述1",
                'fjtp':"/image/20180517/8d7817e420ed44c48f02131dcb177dbb.jpeg",
                'id':b,
                'tsid':d
            }   #self.用在方法属性中，表示是该方法的属性，不会影响其他方法的属性。                                     
        r2 = requests.post(url = self.url2,data = self.data2,headers =self.headers2,timeout=60)     
        a1=r1.text 
        b2 =json.loads(a1)
        c2=str(b2['status'])
        if c2=="1":
            print("江城集市处理成功"+r2.text)
            #logging.info("江城集市处理成功"+r2.text)
        else: 
            #logging.info("江城集市处理失败"+r2.text)
            print("江城集市处理失败"+r2.text)      
            raise Exception(r2.text) 
if __name__=="__main__":  
        unittest.main()
