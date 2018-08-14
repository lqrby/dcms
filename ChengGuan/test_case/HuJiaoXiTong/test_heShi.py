# -*- coding: utf-8 -*-

import requests
from selenium import webdriver
import json,ast 
import unittest
import urllib, sys, io,re
sys.path.append("E:/test/dcms/ChengGuan")
import time
# import config
from bs4 import BeautifulSoup
from config.Log import logging
from test_2web_chengguan_login import test_cg_login
from common.writeAndReadText import writeAndReadTextFile
from common.constant_all import getConstant
from requests_toolbelt import MultipartEncoder

# 网格管理员进入待核实列表
def test_app_wggly_heShiList():
    dhs_url = getConstant.IP+"/dcms/pwasCase/Case-confirmList.action"
    results = writeAndReadTextFile().test_read_appLoginResult()
    wgglyUser = results['wggly']['user']
    dhs_data = {
        "page.pageSize":"20",
        "bgadminid.id":wgglyUser['id'],
        "page.pageNo":"1"
    }
    dqr_res = requests.get(dhs_url,dhs_data,allow_redirects=False).text
    if 'count' in dqr_res:
        # print("待核实列表查询成功")
        return dqr_res
    else:
        print("待核实列表查询失败")
# 网格管理员核实
def test_app_wggly_daiHeShiDetail():
    dhsResult = test_app_wggly_heShiList()
    if dhsResult != None:
        count = re.compile('<caseCheckList count="(.*?)">').search(dhsResult).group(1)
        if count>'0':
            dhs_id = re.compile('<id>(.*?)</id>').search(dhsResult).group(1)
            dhs_description = re.compile('<description>(.*?)</description>').search(dhsResult).group(1)
            dhs_eorc = re.compile('<eorc>(.*?)</eorc>').search(dhsResult).group(1)
            dhs_eventtypeone = re.compile('<eventtypeone>(.*?)</eventtypeone>').search(dhsResult).group(1)
            dhs_eventtypetwo = re.compile('<eventtypetwo>(.*?)</eventtypetwo>').search(dhsResult).group(1)
            dhs_fieldintro = re.compile('<fieldintro>(.*?)</fieldintro>').search(dhsResult).group(1)
            dhs_gridid = re.compile('<gridid>(.*?)</gridid>').search(dhsResult).group(1)
            dhs_mposl = re.compile('<mposl>(.*?)</mposl>').search(dhsResult).group(1)
            dhs_mposb = re.compile('<mposb>(.*?)</mposb>').search(dhsResult).group(1)
            
            hs_url = getConstant.IP_WEB_180+"/dcms/pwasCase/Case-pdaconfirmCase.action"
            results = writeAndReadTextFile().test_read_appLoginResult()
            wgglyUser = results['wggly']['user']
            hs_data = {
                "eorc.id":dhs_eorc,
                "fieldintro":dhs_fieldintro,
                "confirmid.id":wgglyUser['id'],#核实人id
                "mposl":dhs_mposl,
                "description":dhs_description,
                "id":dhs_id,
                "eventtypeone.id":dhs_eventtypeone,
                "casestateid.id":"402880822f3eca29012f3ed0218c0002",#核实有效:402880822f3eca29012f3ed0218c0002   核实无效:402880822f3eca29012f3ecf72020001
                "gridid":dhs_gridid,
                "eventtypetwo.id":dhs_eventtypetwo,
                "mposb":dhs_mposb
            }
            hs_result = requests.post(hs_url,hs_data).text
            if '<issuc>true</issuc>' in hs_result:
                print("核实：网格管理员",wgglyUser['name'],"核实完毕")
                return True
            else:
                print("核实：网格管理员",wgglyUser['name'],"核实失败")
                return False
            
#****************************************************************************************************************

# 执法局待核实列表
def test_app_zfj_heShiList():
    zfjdhs_url = getConstant.IP+"/dcms/pwasCase/Case-confirmList.action"
    zfjresults = writeAndReadTextFile().test_read_appLoginResult()
    zfjUser = zfjresults['zfj']['user']
    zfjdhs_data = {
        "page.pageSize":"20",
        "bgadminid.id":zfjUser['id'],
        "page.pageNo":"1"
    }
    zfjdqr_res = requests.get(zfjdhs_url,zfjdhs_data,allow_redirects=False).text
    if 'count' in zfjdqr_res:
        # print("待核实列表查询成功")
        return zfjdqr_res
    else:
        print("待核实列表查询失败")
#执法局核实
def test_app_zfj_daiHeShiDetail():
    dhs_Result = test_app_zfj_heShiList()
    if dhs_Result != None:
        count = re.compile('<caseCheckList count="(.*?)">').search(dhs_Result).group(1)
        if count>'0':
            dhs_id = re.compile('<id>(.*?)</id>').search(dhs_Result).group(1)
            dhs_description = re.compile('<description>(.*?)</description>').search(dhs_Result).group(1)
            dhs_eorc = re.compile('<eorc>(.*?)</eorc>').search(dhs_Result).group(1)
            dhs_eventtypeone = re.compile('<eventtypeone>(.*?)</eventtypeone>').search(dhs_Result).group(1)
            dhs_eventtypetwo = re.compile('<eventtypetwo>(.*?)</eventtypetwo>').search(dhs_Result).group(1)
            dhs_fieldintro = re.compile('<fieldintro>(.*?)</fieldintro>').search(dhs_Result).group(1)
            dhs_gridid = re.compile('<gridid>(.*?)</gridid>').search(dhs_Result).group(1)
            dhs_mposl = re.compile('<mposl>(.*?)</mposl>').search(dhs_Result).group(1)
            dhs_mposb = re.compile('<mposb>(.*?)</mposb>').search(dhs_Result).group(1)
            
            zfjhsurl = getConstant.IP_WEB_180+"/dcms/pwasCase/Case-pdaconfirmCase.action"
            results = writeAndReadTextFile().test_read_appLoginResult()
            zfjUser = results['zfj']['user']
            zfjhsdata = {
                "eorc.id":dhs_eorc,
                "fieldintro":dhs_fieldintro,
                "confirmid.id":zfjUser['id'],#核实人id
                "mposl":dhs_mposl,
                "description":dhs_description,
                "id":dhs_id,
                "eventtypeone.id":dhs_eventtypeone,
                "casestateid.id":"402880822f3eca29012f3ed0218c0002",#核实有效:402880822f3eca29012f3ed0218c0002   核实无效:402880822f3eca29012f3ecf72020001
                "gridid":dhs_gridid,
                "eventtypetwo.id":dhs_eventtypetwo,
                "mposb":dhs_mposb
            }
            zfjhs_result = requests.post(zfjhsurl,zfjhsdata).text
            if '<issuc>true</issuc>' in zfjhs_result:
                print("核实：执法局核实完毕")
                return True
            else:
                print("核实：执法局",zfjUser['name'],"核实失败")
                return False

# if __name__=="__main__": 
#     #test_app_wggly_daiHeShiDetail()
#     test_app_zfj_daiHeShiDetail()