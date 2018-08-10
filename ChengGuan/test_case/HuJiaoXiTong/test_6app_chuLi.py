# -*- coding: utf-8 -*-

import requests
from selenium import webdriver
import json
import re
import ast
import unittest
import urllib, sys, io
sys.path.append("E:/test/dcms/ChengGuan")
import time
from bs4 import BeautifulSoup
# import config
from config.Log import logging
# sys.stdout = io.TextIOWrapper(sys.stdout.buffer,encoding='utf-8')
from common.constant_all import getConstant
from chengguan_authCode import test_login_authCode
from common.writeAndReadText import writeAndReadTextFile


#查询app待处理案卷列表(权属单位环保局cshbj)    
def test_app_qsdw_PendingList():
    loginitems = writeAndReadTextFile().test_read_appLoginResult()
    qsdwItem = loginitems['qsdw']
    if qsdwItem['message']== 'success':
        qsdwUser = qsdwItem['user']
        qsdw_userId = qsdwUser['id']
        qsdw_deptId = qsdwUser['deptid']
        app_dcl_url = getConstant.IP_WEB_180+"/dcms/PwasAdmin/MobileCase-deallist.action"
        app_dcl_data = {
            "casestate":"30",
            "description":"",
            "page.pageSize":"20",
            "deptid":qsdw_deptId,
            "startTime":"",
            "endTime":"",
            "userid":qsdw_userId,
            "page.pageNo":"1"
        }   
        respons = requests.post(app_dcl_url,app_dcl_data).text
        # print("app待处理列表",respons)
        return respons
    else:
        print("请先登录权属单位！！！")
    


#权属单位进入待处理案卷详情并处理
def test_app_qsdw_handlingDetailsAndHandling():
    # 获取待处理列表
    qsdw_res = test_app_qsdw_PendingList()
    if qsdw_res != None:
        qsdw_list = json.loads(qsdw_res)
        if 'message' in qsdw_list and qsdw_list['message']=='success':
            print("权属单位-案卷列表查询成功")
            if qsdw_list['count']>0:
                qsdwItem = qsdw_list['data'][0]
                qsdw_id = qsdwItem['id']
                qsdw_isFh = qsdwItem['isFh']
                qsdw_dealDeptName = qsdwItem['dealDeptName']
                qsdw_taskID = qsdwItem['taskID']
                qsdw_stateId = qsdwItem['stateId']
                login_qsdwItem = writeAndReadTextFile().test_read_appLoginResult()
                qsdwItem = login_qsdwItem['qsdw']
                if qsdwItem['message']== 'success':
                    qsdwUser = qsdwItem['user']
                    qsdw_userId = qsdwUser['id']
                    qsdw_username = qsdwUser['name']
                    qsdw_deptId = qsdwUser['deptid']
                cl_url = getConstant.IP_WEB_180+"/dcms/PwasAdmin/MobileCase-deal.action"
                cl_data = {
                    "operatingComments":"处理完成",
                    "username":qsdw_username,
                    "stateId":qsdw_stateId,
                    "isFh":qsdw_isFh,                               
                    "deptid":qsdw_deptId,
                    "deptname":qsdw_dealDeptName,
                    "caseid":qsdw_id,
                    "resultprocess":"案件回访",
                    "userid":qsdw_userId,
                    "taskprocess":qsdw_taskID
                }
                cl_res = requests.post(cl_url,cl_data).text
                # print("处理后返回值：",cl_res)
                clres = json.loads(cl_res)
                if 'message' in clres and clres['message'] == 'success':
                    print("权属单位：处理成功")
                    return clres
                else:
                    print("XXXXXXXXXX权属单位：处理时出现错误XXXXXXXXXX")
                
# *********************************************************************************************************
#执法局app查询待处理案卷列表(执法局待处理案卷)    
def test_app_zfj_PendingList():
    login_items = writeAndReadTextFile().test_read_appLoginResult()
    zfjItem = login_items['zfj']
    if zfjItem['message']== 'success':
        zfjUser = zfjItem['user']
        zfj_userId = zfjUser['id']
        zfj_deptId = zfjUser['deptid']
        appdcl_url = getConstant.IP_WEB_180+"/dcms/PwasAdmin/MobileCase-deallist.action"
        appdcl_data = {
            "casestate":"30",
            "description":"",
            "page.pageSize":"20",
            "deptid":zfj_deptId,
            "startTime":"",
            "endTime":"",
            "userid":zfj_userId,
            "page.pageNo":"1"
        }   
        zfj_respons = requests.post(appdcl_url,appdcl_data).text
        return zfj_respons
    else:
        print("请先登录移动端执法局")

#执法局app进入待处理案卷详情并处理
def test_app_zfj_handlingDetailsAndHandling():
    # 获取待处理列表
    zfj_res = test_app_zfj_PendingList()
    if zfj_res != None:
        zfj_list = json.loads(zfj_res)
        if 'message' in zfj_list and zfj_list['message']=='success':
            print("执法局-案卷列表查询成功")
            if zfj_list['count']>0:
                zfjItem = zfj_list['data'][0]
                zfj_id = zfjItem['id']
                zfj_isFh = zfjItem['isFh']
                zfj_dealDeptName = zfjItem['dealDeptName']
                zfj_taskID = zfjItem['taskID']
                zfj_stateId = zfjItem['stateId']
                loginItem = writeAndReadTextFile().test_read_appLoginResult()
                zfjItem = loginItem['zfj']
                if zfjItem['message']== 'success':
                    zfjUser = zfjItem['user']
                    zfj_userId = zfjUser['id']
                    zfj_username = zfjUser['name']
                    zfj_deptId = zfjUser['deptid']
                cl_url = getConstant.IP_WEB_180+"/dcms/PwasAdmin/MobileCase-deal.action"
                cl_data = {
                    "operatingComments":"处理完成",
                    "username":zfj_username,
                    "stateId":zfj_stateId,
                    "isFh":zfj_isFh,                               
                    "deptid":zfj_deptId,
                    "deptname":zfj_dealDeptName,
                    "caseid":zfj_id,
                    "resultprocess":"案件回访",
                    "userid":zfj_userId,
                    "taskprocess":zfj_taskID
                }
                zfjcl_res = requests.post(cl_url,cl_data).text
                print("处理后返回值：",zfjcl_res)
                zfjclres = json.loads(zfjcl_res)
                print(zfjclres['message'])
                if 'message' in zfjclres and zfjclres['message'] == 'success':
                    print("执法局：处理成功")
                else:
                    print("XXXXXXXXXX执法局：出现错误XXXXXXXXXX")




if __name__=="__main__": 
    # 权属单位案卷处理
    test_app_qsdw_handlingDetailsAndHandling()
    # test_app_zfj_handlingDetailsAndHandling()