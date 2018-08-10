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
sys.stdout = io.TextIOWrapper(sys.stdout.buffer,encoding='utf-8')
from test_2web_chengguan_login import test_cg_login
from common.writeAndReadText import writeAndReadTextFile
from common.constant_all import getConstant
from test_2app_login import appLogin


#执法局app案卷查询   
def test_app_zfj_fileQuery():
    pass
    # results = writeAndReadTextFile().test_read_appLoginResult()
    # if results['zfj']['message']== 'success':
    #     zfjUser = results['zfj']['user']
    #     zfjsubmiturl = getConstant.IP_WEB_180+"/dcms/pwasCase/pwasCase-pdasave.action"
    #     zfj_sb_data = writeAndReadTextFile().test_read_txt('E:/test/dcms/ChengGuan/testFile/shangBao/gongdanluru_app_zfj.txt')
    #     zfjList = zfj_sb_data.split(",")

    #     zfj_shangbao_data = {
    #         "eorc.id":zfjList[0],
    #         "fieldintro":zfjList[1],
    #         "deptId":"",
    #         "mposl":zfjList[2],
    #         "description":zfjList[3],
    #         "objcode":"",
    #         "eventtypeone.id":zfjList[4],
    #         "gridid":zfjList[5],
    #         "bgadminid.id":zfjUser['id'],
    #         "eventtypetwo.id":zfjList[6],
    #         "mposb":zfjList[7]
    #     }
    #     #提交app案卷上报
    #     res = requests.post(url=zfjsubmiturl,data=zfj_shangbao_data).text
    #     result_data= re.compile('<caseInputInfo><issuc>(.*?)</issuc><caseprochisid>(.*?)</caseprochisid><idcase>(.*?)</idcase></caseInputInfo>').search(res)
    #     # issuc = result_data.group(1)
    #     caseprochisid = result_data.group(2)
    #     idcase = result_data.group(3)
    #     # 上传图片地址
    #     imgUrl = getConstant.IP_WEB_180+"/dcms/PwasAdmin/PwasAdmin-imageup.action?imagetype=image&idcase="+idcase+"&prochisid="+caseprochisid
    #     # imgData = {
    #     #     "imagetype":"image",
    #     #     "idcase":idcase,
    #     #     "prochisid":caseprochisid
    #     # }
    #     files = {'upload': ('image', open('E:/test/dcms/ChengGuan/testFile/img/1.jpg', 'rb'))}
    #     r = requests.post(url = imgUrl,files=files).text
    #     print("结果",r)
    #     # print("执法局app案卷上报成功",res)
    #     return r


# 市民我的上报列表
def test_app_sm_myReport():
    results_sm2 = writeAndReadTextFile().test_read_appLoginResult()
    smItem = results_sm2['sm']['result']
    reportUrl = getConstant.IP_APP_180+"/publicworkstation/complaint/getComplaintListByUserId.action?is_login="+smItem['is_login']+"&token="+smItem['token']+"&userid="+smItem['id']
    res_List = requests.get(reportUrl).text
    wdsb_list = json.loads(res_List)
    if 'message' in wdsb_list:
        print("市民-我的上报列表查询成功")
    elif ('errCode' in wdsb_list) and (wdsb_list['errCode'] == '2'):
        appLogin().test_app_allLogin()
        print("appAll登录成功")
    else:
        print("市民-我的上报查询失败！！！")
    return wdsb_list

# 市民案卷详情
def test_app_sm_fileDetails():
    smsb_list = test_app_sm_myReport()
    if 'message' in smsb_list:
        smsb_idcase = smsb_list['result'][0]['idcase']
        fileDetailsUrl = getConstant.IP_APP_180+"/publicworkstation/complaint/getCaseDetailById.action?id="+smsb_idcase
        sm_res_detail = requests.get(fileDetailsUrl).text
        sm_detail = json.loads(sm_res_detail)
        if('message' in sm_detail):
            print("市民-案卷详情正常")
    else:
        print("XXXXXXXX市民案卷详情:上一环节错误(市民-我的上报列表)XXXXXXXX")
    

    
if __name__=="__main__": 
    # test_app_zfj_submitOrder()
    # test_app_sm_submitOrder()
    # test_app_sm_myReport()
    test_app_sm_fileDetails()