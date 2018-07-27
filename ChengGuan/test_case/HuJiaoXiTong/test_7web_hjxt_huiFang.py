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
from chengguan_authCode import test_login_authCode
from common.getCookie import test_getCookie
from common.getCookie import test_write_txt


#查询待回访案卷列表    
def test_returnVisitList():
    cookies = test_readCookies()
    dhf_url = getConstant.IP+"/dcms/cwsCase/Case-hflist.action?casestate=55&menuId=2c94ccad37c600e30137c607846b0003&keywords=402880ea2f6bd924012f6c521e8c0034"
    header = {
        "Cookie":cookies
    }
    respons = requests.get(url = dhf_url,headers=header).text
    return respons

#进入待回访案卷详情并回访
def test_returnDetailsAndVisit():
    # 获取待回访列表
    res = test_returnVisitList()
    result = BeautifulSoup(res,'html.parser')
    divObj = result.find('div', attrs={'class':'mainContentTableContainer'})
    dcl_tr = divObj.findAll('table')[1].findAll('tr')[1]
    str_tr = str(dcl_tr)
    number= re.compile('<span id="pagemsg" style="(.*?)"><label>总共(.*?)页,(.*?)条记录</label></span>').search(res).group(3)
    if int(number)>0:
        dhfobj = re.compile(r'<tr[\s\S]*id="(.*?)"[\s\S]*onclick="casedo[\(](.*?),(.*?),(.*?),(.*?),this[\)]">')
        dhfid = dhfobj.search(str_tr).group(1)
        dhf_menuid = dhfobj.search(str_tr).group(2).strip("'")
        dhf_taskprocess = dhfobj.search(str_tr).group(5).strip("'")
        # 待回访详情url
        dclxq_url = getConstant.IP+"/dcms/cwsCase/Case-hf.action?id="+dhfid+"&menuId="+dhf_menuid+"&taskprocess="+dhf_taskprocess
        dclxq_cookies = test_readCookies()
        header = {
           "Cookie":dclxq_cookies
        }
        dclxq_res = requests.get(url = dclxq_url,headers=header).text
        hflist = test_read_txt('E:/test/dcms/ChengGuan/testFile/huiFang/anjuanhuifang.txt')
        hf_list = hflist.split(',')
        hf_taskcasestateid = re.compile('<input type="hidden" id="taskcasestateid" name="taskcasestateid" value="(.*?)"/>').search(dclxq_res).group(1)
        hf_casestate = re.compile('<input type="hidden" id="casestate" name="casestate" value="(.*?)" />').search(dclxq_res).group(1)
        hf_taskprocess = re.compile('<input type="hidden" id="taskprocess" name="taskprocess" value="(.*?)" />').search(dclxq_res).group(1)
        # 回访案卷url
        hf_url = getConstant.IP+"/dcms/cwsCase/Case-check.action"
        hf_data = {
            "taskcasestateid":hf_taskcasestateid,
            "menuId":dhf_menuid,
            "casestate":hf_casestate,
            "id":dhfid,
            "taskprocess":hf_taskprocess,
            "resultprocess":hf_list[0],
            "isFaction":"",
            "myd":"on",
            "operatingComments":hf_list[1],
            "sentence":""
        }
        hf_header = {
            "Cookie":dclxq_cookies
        }
        hf_result = requests.post(hf_url,hf_data,headers = hf_header).text
        print("回访完成",hf_result)
        return hf_result
    else:
        print("待回访列表暂无数据！！！")


if __name__=="__main__": 
    test_returnDetailsAndVisit()