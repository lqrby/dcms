# -*- coding: utf-8 -*-
import requests
from selenium import webdriver
import json ,re  
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


#执法局查询待复核案卷列表    
def test_app_zfj_returnVisitList():
    login_items = writeAndReadTextFile().test_read_appLoginResult()
    zfjItem = login_items['zfj']
    if zfjItem['message']== 'success':
        zfjUser = zfjItem['user']
        zfj_userId = zfjUser['id']
    dhf_url = getConstant.IP_WEB_180+"/dcms/pwasCase/Case-checkList.action"
    zfjdfh_data = {
        "page.pageSize":"20",
        "bgadminid.id":zfj_userId,
        "page.pageNo":"1"
    }
    respons = requests.post(dhf_url,zfjdfh_data).text
    return respons

#执法局进入待复核案卷详情并复核
def test_app_zfj_returnDetailsAndVisit():
    # 获取待复核列表
    zfjlist_res = test_app_zfj_returnVisitList()
    if zfjlist_res != None:
        dcl_count = re.search('<caseCheckList count="(.*?)">',zfjlist_res).group(1)
        if 'count' in zfjlist_res:
            print("执法局：案卷列表查询成功")
            if int(dcl_count)>0:
                login_items = writeAndReadTextFile().test_read_appLoginResult()
                zfjItem = login_items['zfj']
                if zfjItem['message']== 'success':
                    zfjUser = zfjItem['user']
                    zfj_userId = zfjUser['id']
                dclId = re.compile('<id>(.*?)</id>').search(zfjlist_res).group(1)
                zfj_cl_url = getConstant.IP_WEB_180+"/dcms/pwasCase/Case-pdacheckCase.action"
                zfj_cl_data = {
                    "id":dclId,
                    "checkdesc":"经复核有效",
                    "casestateid.id":"402880822f3eca29012f3ed146b30006",
                    "checkid.id":zfj_userId,
                    "taskprocess":""
                }
                cl_res = requests.post(zfj_cl_url,zfj_cl_data).text
                
                print(cl_res)
            else:
                print("执法局:待处理列表暂时为空")
        elif 'errorCode' in zfjlist_res and zfjlist_res['errorCode']=='2':
            print("XXXXXXXXXX对不起请您先登录XXXXXXXXXX")
    else:
        print("执法局：列表未返回")
    

# ==================================================================================================
#网格管理员apk查询待复核案卷列表    
def test_app_wggly_returnVisitList():
    login_items_val = writeAndReadTextFile().test_read_appLoginResult()
    wgglyItem = login_items_val['wggly']
    if wgglyItem['message']== 'success':
        wgglyUser = wgglyItem['user']
        wggly_userId = wgglyUser['id']
    dhf_url = getConstant.IP_WEB_180+"/dcms/pwasCase/Case-checkList.action"
    wgglydfh_data = {
        "page.pageSize":"20",
        "bgadminid.id":wggly_userId,
        "page.pageNo":"1"
    }
    respons = requests.post(dhf_url,wgglydfh_data).text
    return respons

#网格管理员进入待复核案卷详情并复核
def test_app_wggly_returnDetailsAndVisit():
    # 获取待复核列表
    wgglylist_res = test_app_wggly_returnVisitList()
    if wgglylist_res != None:
        
        if 'count' in wgglylist_res:
            print("网格管理员：案卷列表查询成功")
            dcl_count = re.search('<caseCheckList count="(.*?)">',wgglylist_res).group(1)
            if int(dcl_count)>0:
                login_items = writeAndReadTextFile().test_read_appLoginResult()
                wgglyItem = login_items['wggly']
                if wgglyItem['message']== 'success':
                    wgglyUser = wgglyItem['user']
                    wggly_userId = wgglyUser['id']
                wgglydclId = re.compile('<id>(.*?)</id>').search(wgglylist_res).group(1)
                wggly_cl_url = getConstant.IP_WEB_180+"/dcms/pwasCase/Case-pdacheckCase.action"
                wggly_cl_data = {
                    "id":wgglydclId,
                    "checkdesc":"经复核有效",
                    "casestateid.id":"402880822f3eca29012f3ed146b30006",
                    "checkid.id":wggly_userId,
                    "taskprocess":""
                }
                cl_res = requests.post(wggly_cl_url,wggly_cl_data).text
                # print(cl_res)
                return cl_res
            else:
                print("网格管理员:待处理列表暂时为空")
        elif 'errorCode' in wgglylist_res and wgglylist_res['errorCode']=='2':
            print("XXXXXXXXXX对不起请您先登录XXXXXXXXXX")
    else:
        print("网格管理员：列表未返回")


if __name__=="__main__": 
    test_app_wggly_returnDetailsAndVisit()