# -*- coding: utf-8 -*-

import requests
from selenium import webdriver
import json  
import re
import ast
import unittest
import urllib, sys, io
sys.path.append("E:/test/dcms/ChengGuan")
import datetime
import time
from bs4 import BeautifulSoup
# import config
from config.Log import logging
sys.stdout = io.TextIOWrapper(sys.stdout.buffer,encoding='utf-8')
from test_2web_chengguan_login import test_cg_login
from common.writeAndReadText import writeAndReadTextFile
from common.constant_all import getConstant
from test_2app_login import appLogin
from common.appReportPicture import test_app_ReportPicture

#网格管理员app上报案卷，表单数据gongdanluru_app_wggly.txt无需核实需要复核   
def test_app_wggly_submitOrder():
    login_results = writeAndReadTextFile().test_read_appLoginResult()
    wgglyUser = login_results['wggly']['user']
    wgglysubmiturl = getConstant.IP_WEB_180+"/dcms/pwasCase/pwasCase-pdasave.action"
    wggly_sb_data = writeAndReadTextFile().test_read_txt('E:/test/dcms/ChengGuan/testFile/shangBao/gongdanluru_app_wggly.txt')
    wgglyList = wggly_sb_data.split(",")

    wggly_shangbao_data = {
        "eorc.id":wgglyList[0],
        "fieldintro":wgglyList[1],
        "deptId":"",
        "mposl":wgglyList[2],
        "description":wgglyList[3],
        "objcode":"",
        "eventtypeone.id":wgglyList[4],
        "gridid":wgglyList[5],
        "bgadminid.id":wgglyUser['id'],
        "eventtypetwo.id":wgglyList[6],
        "mposb":wgglyList[7]
    }
    #提交app案卷上报
    wggly_respon = requests.post(wgglysubmiturl,wggly_shangbao_data).text
    resultData= re.compile('<caseInputInfo><issuc>(.*?)</issuc><caseprochisid>(.*?)</caseprochisid><idcase>(.*?)</idcase></caseInputInfo>').search(wggly_respon)
    wgglydhs_issuc = resultData.group(1)
    wgglydhs_caseprochisid = resultData.group(2)
    wgglydhs_idcase = resultData.group(3)
    if wgglydhs_issuc:
        print("网格管理员：案卷上报成功")
    else:
        print("XXXXXXXXXX网格管理员：案卷上报失败XXXXXXXXXX")
    # 上传图片地址
    wgglyimgUrl = getConstant.IP_WEB_180+"/dcms/PwasAdmin/PwasAdmin-imageup.action?imagetype=image&idcase="+wgglydhs_idcase+"&prochisid="+wgglydhs_caseprochisid
    imgpicpath = "E:/test/dcms/ChengGuan/testFile/img/10.jpg"
    test_app_ReportPicture(wgglyimgUrl,imgpicpath)
#=====================================================================================================================
#执法局app上报案卷，表单数据gongdanluru_app_zfj.txt无需核实复核   
def test_app_zfj_submitOrder():
    results = writeAndReadTextFile().test_read_appLoginResult()
    zfjUser = results['zfj']['user']
    zfjsubmiturl = getConstant.IP_WEB_180+"/dcms/pwasCase/pwasCase-pdasave.action"
    zfj_sb_data = writeAndReadTextFile().test_read_txt('E:/test/dcms/ChengGuan/testFile/shangBao/gongdanluru_app_zfj.txt')
    zfjList = zfj_sb_data.split(",")

    zfj_shangbao_data = {
        "eorc.id":zfjList[0],
        "fieldintro":zfjList[1],
        "deptId":"",
        "mposl":zfjList[2],
        "description":zfjList[3],
        "objcode":"",
        "eventtypeone.id":zfjList[4],
        "gridid":zfjList[5],
        "bgadminid.id":zfjUser['id'],
        "eventtypetwo.id":zfjList[6],
        "mposb":zfjList[7]
    }
    #提交app案卷上报
    zfj_respon = requests.post(zfjsubmiturl,zfj_shangbao_data).text
    result_data= re.compile('<caseInputInfo><issuc>(.*?)</issuc><caseprochisid>(.*?)</caseprochisid><idcase>(.*?)</idcase></caseInputInfo>').search(zfj_respon)
    issuc = result_data.group(1)
    caseprochisid = result_data.group(2)
    idcase = result_data.group(3)
    if issuc:
        print("执法局：案卷上报成功")
    else:
        print("XXXXXXXXXX执法局：上报失败XXXXXXXXXX")
    # 上传图片地址
    imgUrl = getConstant.IP_WEB_180+"/dcms/PwasAdmin/PwasAdmin-imageup.action?imagetype=image&idcase="+idcase+"&prochisid="+caseprochisid
    picpath = "E:/test/dcms/ChengGuan/testFile/img/1.jpg"
    test_app_ReportPicture(imgUrl,picpath)

#####################################################################################################################
#市民app上报案卷，表单数据gongdanluru_app_sm.txt_需核实复核  
def test_app_sm_submitOrder():
    results_sm = writeAndReadTextFile().test_read_appLoginResult()
    smUser = results_sm['sm']['result']
    smsubmiturl = getConstant.IP_APP_180+"/publicworkstation/complaint/saveComplaint.action"
    sm_sb_data = writeAndReadTextFile().test_read_txt('E:/test/dcms/ChengGuan/testFile/shangBao/gongdanluru_app_sm.txt')
    smList = sm_sb_data.split(",")
    sm_data = {
        "is_login":smUser['is_login'],
        "token":smUser['token'],
        "name":smUser['name'],
        "phone":smUser['phoneNumber'],
        "longitude":smList[0],
        "latitude":smList[1],
        "complaincontent":smList[2],
        "bgcode":smList[3],
        "bgcodename":smList[4],
        "gridid":smList[5],
        "wxsource":smList[6],
        "imgurl":smList[7],
        "userid":smUser['id'],
        "eorcid":smList[8],
        "eventoneid":smList[9],
        "eventtwoid":smList[10],
    }
    res = requests.post(smsubmiturl,sm_data).text
    smsb_list = json.loads(res)
    if 'message' in smsb_list:
        print("市民-案卷上报成功")
    elif ('errCode' in smsb_list) and (smsb_list['errCode'] == '2'):
        appLogin().test_app_allLogin()
        print("@@@appAll登录成功，市民:请重新上报@@@")
    else:
        print("市民-上报案卷失败！！！")
    return smsb_list

if __name__=="__main__": 
    test_app_wggly_submitOrder()
    # test_app_zfj_submitOrder()
    # test_app_sm_submitOrder()