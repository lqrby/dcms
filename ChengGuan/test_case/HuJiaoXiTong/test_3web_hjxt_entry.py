# -*- coding: utf-8 -*-

import requests
from selenium import webdriver
import json,ast 
import unittest
import urllib, sys, io
sys.path.append("E:/test/dcms/ChengGuan")
import time
# import config
from config.Log import logging
sys.stdout = io.TextIOWrapper(sys.stdout.buffer,encoding='utf-8')
from test_2web_chengguan_login import test_cg_login
from common.writeAndReadText import writeAndReadTextFile
from common.constant_all import getConstant
from requests_toolbelt import MultipartEncoder


class test_submitOrder():       
#web提交工单录入表单gongdanluru_2.txt_无需核实需要复核   
    def test_web_submitOrder(self):
        cookies = writeAndReadTextFile().test_readCookies()
        submiturl = getConstant.IP_WEB_180+"/dcms/ccsCase/Case-callToCaseStart.action"
        webdata = writeAndReadTextFile().test_read_txt('E:/test/dcms/ChengGuan/testFile/shangBao/gongdanluru_web_4ny.txt')
        picpath = "E:/test/dcms/ChengGuan/testFile/img/1.png"
        img_value = ('1.png', open(picpath,'rb'),'multipart/form-data')
        webdata_list = webdata.split(",")
        m = MultipartEncoder(
            fields = {
                "mposl":webdata_list[0],
                "mposb":webdata_list[1],
                "menuId":webdata_list[2],
                "removeFileId":"",	
                "updateCaseGetUrl":"",	
                "casecallId":"",	
                "imageid":"",
                "px":"",	
                "py":"",	
                "deptId":"",
                "isFh":webdata_list[3],
                "casesource":"",
                "dispatchDeptname":"",
                "street":webdata_list[4],
                "p_name":webdata_list[5],
                "p_sex":webdata_list[6],
                "p_job":webdata_list[7],
                "p_phone":webdata_list[8],
                "other_phone":webdata_list[9],
                "feedback":webdata_list[10],
                "source.id":webdata_list[11],
                "id":"",
                "eorc.id":webdata_list[12],
                "eventtypeone.id":webdata_list[13],
                "eventtypetwo.id":webdata_list[14],
                "startConditionId":webdata_list[15],
                "regioncode.id":webdata_list[16],
                "bgcode.id":webdata_list[17],
                "objcode":"",
                "bgadminid.id":webdata_list[18],
                "bgadminid2":webdata_list[19],
                "gridid":webdata_list[20],
                "needconfirm":webdata_list[21],
                "description":webdata_list[22],
                "dealWay":webdata_list[23],
                "fieldintro":webdata_list[24],
                "upload":img_value
            }
        )
        
        header = {
            "Content-Type":m.content_type,
            "Cookie":cookies
        }
        #重定向没有返回值
        webres = requests.post(url = submiturl, data=m, headers=header,allow_redirects=False)
        web_res = webres.text
        mystr = web_res.find("errorCode")
        if mystr != -1:
            print("XXXXXXXXXXweb工单提交失败XXXXXXXXXX")
            return False
        elif ('Set-Cookie' in webres.headers):
            print("====================对不起您未登录，请登录后再上报工单=====================")
            return False
        else:
            print("web工单提交成功")  
            return True



if __name__=="__main__": 
    test_submitOrder().test_web_submitOrder()