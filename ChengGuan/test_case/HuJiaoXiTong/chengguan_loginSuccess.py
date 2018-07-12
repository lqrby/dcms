# # -*- coding: utf-8 -*-
# from PIL import Image
# import unittest
# from selenium import webdriver
# from selenium.webdriver.support.ui import Select
# from selenium.webdriver.support.wait import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# from selenium.webdriver.common.action_chains import ActionChains
# from selenium.webdriver.common.by import By
# # from com.aliyun.api.gateway.sdk import client
# # from com.aliyun.api.gateway.sdk.http import request
# # from com.aliyun.api.gateway.sdk.common import constant
# import base64
# import json
# import requests
# import urllib.request
# import os.path
# import urllib
# import time
# import sys,http
# from PIL import Image
# from selenium import webdriver
# import time
# from PIL import ImageGrab
# import traceback
# from bs4 import BeautifulSoup
# from test_web_chengguan_authCode import test_login_authCode
# from test_getCookie import test_getCookie
# from test_web_chengguanLogin import test_cg_login
# from constant_all import IP 

# def test_chengguan_success(driver):
#     try:
#         login_result = test_cg_login(driver)
#         while login_result == "" :
#             login_result = test_cg_login(driver) 
#         else:
#         # header = {'cookie':cookiestr} 
#             url = IP+"/dcms/bmsAdmin/Admin-redirectLogonPage.action"
#         # wbdata = requests.get(url,headers=header).text
#         # soup = BeautifulSoup(wbdata,'html.parser')
#         # input = soup.find('input', attrs={'id': 'sysMenu'})
#         # #获取了input中的value属性值
#         # value = input['value']
#         # json_value = json.loads(value)
#         # print("@@@@@@@@@@@@@@@@@",json_value)
        
#     except:
#         traceback.print_exc() 
