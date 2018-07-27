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
sys.stdout = io.TextIOWrapper(sys.stdout.buffer,encoding='utf-8')
from common.getCookie import test_readCookies
from common.getCookie import test_read_txt
from common.constant_all import getConstant


#查询待派发案卷列表    
def test_PendingDistributionList():
   
    cookies = test_readCookies()
    list_url = getConstant.IP+"/dcms/cwsCase/Case-dispatchlist.action?casestate=20&menuId=4028338158a414bd0158a484daae000e&keywords=402880ea2f6bd924012f6c521e8c0034"
    header = {
        "Cookie":cookies
    }
    respons = requests.get(url = list_url,headers=header).text
    return respons

#进入待派发案卷详情并派发
def test_sendDetailsAndSendOut():
    # 获取待派发列表
    res = test_PendingDistributionList()
    result = BeautifulSoup(res,'html.parser')
    number= re.compile('<span id="pagemsg" style="(.*?)"><label>总共(.*?)页,(.*?)条记录</label></span>').search(res).group(3)
    divObj = result.find('div', attrs={'class':'mainContentTableContainer'})
    dcl_tr = divObj.findAll('table')[1].findAll('tr')[1]
    str_tr = str(dcl_tr)




    if int(number)>0:
        menuId = re.compile('<input type="hidden" id="menuId" name="menuId" value="(.*?)" />').search(res).group(1)
        case_state = re.compile('<input type="hidden" name="casestate" id="casestate" value="(.*?)"/>').search(res).group(1)
        Matching_result = re.compile(r'<tr[\s\S]*id="(.*?)"[\s\S]*onclick="casedo[\(](.*?),(.*?),(.*?),(.*?),this[\)]">').search(str_tr)
        dpf_id = Matching_result.group(1)
        dpf_taskprocessId = Matching_result.group(5).strip("'")
        # 进入待派发案卷详情
        detail_url = getConstant.IP+"/dcms/cwsCase/Case-dispatchview.action"
        cookie = test_readCookies()
        header = { "Cookie" : cookie }
        dpfdata = {
            "casestate":case_state,
            "id":dpf_id,
            "menuId":menuId,
            "taskprocess":dpf_taskprocessId
        }

        res = requests.post(url = detail_url,data = dpfdata,headers = header).text
        # print("详情结果是：",res)
        taskcasestateid = re.compile('<input type="hidden" id="taskcasestateid" name="taskcasestateid" value="(.*?)"/>').search(res).group(1)
        applyreturnlist = re.compile('<input type="hidden" id="applyreturnlist" name="applyreturnlist" value="(.*?)" />').search(res).group(1)
        dispatchDeptname = re.compile('<input type="hidden" name="dispatchDeptname" value="(.*)" id="dispatchDeptname"/>').search(res).group(1)
        dispatchDeptid = re.compile('<input type="hidden"  readonly="" id="dispatchDeptid" name="dispatchDeptid"  value="(.*?)"  >').search(res).group(1)
        dispatchUserid = re.compile('<input type="hidden"  readonly="" id="dispatchUserid" name="dispatchUserid"  value="(.*?)"  >').search(res).group(1)
        deptname = re.compile('<input type="text" onclick="(.*?)" readonly="" id="deptname" name="(.*?)" value="(.*?)">').search(res).group(1)
        # print(taskcasestateid)
        # print(applyreturnlist)
        # print(dispatchDeptname)
        # print(dispatchDeptid)
        # print(dispatchUserid)
        # print(deptname)
        # casestate,resultprocess,limittime,operatingComments,sentence
        pfdata = test_read_txt("E:/test/dcms/ChengGuan/testFile/paiFa/paifa.txt")
        pf_list = pfdata.split(',')
        pf_url = getConstant.IP+"/dcms/cwsCase/Case-dispatch.action"
        pf_data = {
            "taskcasestateid":taskcasestateid,
            "menuId":menuId,
            "casestate":case_state,
            "id":dpf_id,
            "taskprocess":dpf_taskprocessId,
            "resultprocess":pf_list[1],
            "applyreturnlist":applyreturnlist,
            "limittime":pf_list[2],
            "dispatchDeptname":dispatchDeptname,
            "dispatchDeptid":dispatchDeptid,
            "dispatchUserid":dispatchUserid,
            "deptname":deptname,
            "operatingComments":pf_list[3],
            "sentence":pf_list[4]
        }
    
   
        pf_result = requests.post(pf_url,pf_data,headers=header).text
        print("派发返回值是：",type(pf_result),pf_result)
        return pf_result

    else:
        print("待派发列表暂无数据！！！")



if __name__=="__main__": 
    test_sendDetailsAndSendOut()