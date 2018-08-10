#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018-07-09 14:00
# constant/constant_1.py
# 常量部分（固定不变使用频繁的参数维护在此处）
#正式库ip地址
#IP = 'http://122.137.242.15'  
#uat服务ip地址
#IP = 'http://122.137.242.91'
#180服务ip地址
from PIL import Image
import unittest
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
# from com.aliyun.api.gateway.sdk import client
# from com.aliyun.api.gateway.sdk.http import request
# from com.aliyun.api.gateway.sdk.common import constant
import base64
import json
import requests
import os.path
import urllib
import time
import urllib, sys

from PIL import Image
from selenium import webdriver
import time
from PIL import ImageGrab
class getConstant():
    IP = "http://219.149.226.180:7897"
    IP_WEB_180 = "http://219.149.226.180:7897"
    IP_APP_180 = "http://219.149.226.180:7880"
    # IP_WEB_91 = "http://122.137.242.91"
    # IP_APP_91 = "http://122.137.242.91"
    # IP_WEB_15 = "http://122.137.242.15"
    # IP_APP_15 = "http://122.137.242.15"
    
    PROJECT_PATH = "E:/test/dcms/ChengGuan"
    
    