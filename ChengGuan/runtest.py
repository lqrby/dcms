# -*- coding: utf-8 -*-
import unittest  
import json  
import requests 
from HTMLTestRunner import HTMLTestRunner
import time,sys,os
from imp import reload
from config.Log import logging
default_encoding ='utf-8'

if sys.getdefaultencoding() != default_encoding:
    reload(sys)
    sys.getdefaultencoding() 
    'utf-8'
 #定义测试用例的目录为当前目录  
test_dir = './test_case/HuJiaoXiTong'  
print("开始")
#unittest.defaultTestLoader(): defaultTestLoader()类，通过该类下面的discover()方法可自动更具测试目录start_dir匹配查找
#测试用例文件（test*.py），并将查找到的测试用例组装到测试套件，因此可以直接通过run()方法执行discover。
discover = unittest.defaultTestLoader.discover(test_dir,pattern = 'test*.py')  

if __name__=="__main__":  
#     #按照一定的格式获取当前的时间  
#     now = time.strftime("%Y-%m-%d %H-%M-%S")  
#     print now
    #定义报告存放路径
        filename ='E:/test/dcms/ChengGuan/test_report/TestRunner.html'  
        #filename ='D:/jmeter/jenkins/workspace/jiangcheng_test_script/JiangChengJiShi/test_report/TestRunner.html'  
        fp = open(filename,"wb")  
        #定义测试报告  
        runner = HTMLTestRunner(stream = fp,  
                                title='城管接口测试报告',
                                description='城管测试用例执行情况:')  
        #运行测试  
        runner.run(discover) 
        print("结束")    
        fp.close() #关闭报告文件
        #os.system("E:/test/dcms/JiangChengJiShi/sendemail.py")
        #os.system("D:/jmeter/jenkins/workspace/jiangcheng_test_script/sendemail.py")
        logging.info("测试结束")