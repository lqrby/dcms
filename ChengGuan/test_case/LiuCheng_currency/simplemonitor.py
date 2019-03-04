#!/usr/bin/env python  
#coding=utf-8  
import unittest
import sys
sys.path.append("E:/test/dcms/ChengGuan")
import time,random,json
import threading
from config.Log import logging
from selenium import webdriver
# from login import allLogin
# from jobEntry import submitOrder
# from queRen import confirm
# from heShi import verify
# from liAn import setUpCase
# from paiFa import distribution
# from guaZhang import hangUp
# from chuLi import fileFandling
# from fuHeAndHuiFang import reviewAndReturnVisit
# from common.writeAndReadText import writeAndReadTextFile
# from common.constant_all import getConstant  
# import time  
import telnetoperate
# from telnetoperate import TelnetAction
  
  
  
remote_server=telnetoperate.TelnetAction("219.149.226.180:7897","#","wangnannan","123456")  
#get cpu information  
cpu=remote_server.get_output("sar 1 1 |tail -1")  
memory=remote_server.get_output("top | head -5 |grep -i memory")  
io=remote_server.get_output("iostat -x 1 2|grep -v '^$' |grep -vi 'dev'")  