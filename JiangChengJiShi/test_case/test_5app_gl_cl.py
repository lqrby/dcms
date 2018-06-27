# # -*- coding: utf-8 -*-
# import requests
# import json  
# import unittest
# import urllib,sys
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
#     '''''接口名称：吉林公路管理系统'''    #这个描述接口名称  
#     def test_jcjs_down(self): 
#         '''''测试用例5：pc立案_app核实'''   #这个描述接口用例名称           
#         self.url = 'http://219.149.226.180:7880/roadproject/roadsevent/add?status=1'  #请求url  
#         self.headers = {"Content-Type":"application/x-www-form-urlencoded "}  
#         self.data = {                                   #请求参数  
#             'status' :   1,
#             'roadsectionid'  :  2065,
#             'roadsectionname' :   '自定义蛤蟆河村',
#             'geompublic' :  '14114819.841640804 5455419.392612622',
#             'eventtypeid' :     1,
#             'eventlevelid' :     1,
#             'reporttypeid' :     1,
#             'publicaddress' :    '测试测试测试测试测试测试测试测试测试测试测试',
#             'publicname'   :   '李泽林',
#             'publicphone'   :   13021979651,
#             'publicmessage' :  '测试',
#             'publicimgpaths' : '/image/20180525/88de7566e87a423ab8b74c072da92115.png'
#         }   #self.用在方法属性中，表示是该方法的属性，不会影响其他方法的属性。 
#     #                     i=0
#     #                     while(i<5):                         
#         r = requests.post(url = self.url,data = self.data,headers = self.headers) 
#         a=r.text 
#         b =json.loads(a)
#         c=str(b['code'])
#         if c=="1":
#             print("web录入案卷成功"+r.text)
#             logging.info("web录入案卷成功"+r.text)
#         else: 
#             logging.info("web录入案卷失败比"+r.text)
#             print("web录入案卷失败"+r.text)
#             raise Exception(r.text)
#     #                         i=i+1        
#         url="http://219.149.226.180:7880/roadproject/roadsevent/list?curPage=1&eventtypeid=&status=&roadsectionid=&eventlevelid=&pageSize=20"
#         self_data = urllib.request.urlopen(url)
#         self3 = self_data.read()
#         #转换成字典
#         self2=json.loads(self3)
#         #取首行案卷tsid
#         a=self2['list'][0]['id']
#         b=str(a)                        
#         #app案件核实
#         url2 = 'http://219.149.226.180:7880/roadproject/roadsevent/update'  #请求url  
#         headers2 = {"Content-Type":"application/x-www-form-urlencoded "}  
#         data2 = {                                   #请求参数  
#             'checkedimgpaths':'/image/20180525/f4ab6ebab0a542be84c813b1aaf2ff2e.jpeg',
#             'checkerphone':13021979652,
#             'checkedaddress':'阿飞饿了',
#             'status':2,
#             'checkedmessage':'哈哈哈哈哈哈',
#             'id':b,
#             'geomchecked':'126.79401805199734 43.93714415006764',
#             'checkedistrue':'1',
#             'checkeruserid':'40',
#             'checkername':'lizelin5'#核实人
#         }   #self.用在方法属性中，表示是该方法的属性，不会影响其他方法的属性。                                     
#         r1 = requests.post(url = url2,data = data2,headers =headers2)
#         a1=r1.text 
#         b1=json.loads(a1)
#         c1=str(b1['code'])
#         if c1=="1":
#             print("app复核成功"+r.text)
#             logging.info("app复核成功"+r.text)
#         else: 
#             logging.info("app复核失败"+r.text)
#             print("app复核失败"+r.text)
#             #print(self.status_code)  
#             raise Exception(r.text)               
                          
# if __name__=="__main__":  
#         unittest.main()
