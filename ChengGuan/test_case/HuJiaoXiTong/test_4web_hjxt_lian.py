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


#查询待立案列表    
def test_toBePutOnRecordList():
    # res_result = test_goToWorkOrderEntry(driver) #进入呼叫页面的返回值
    # cookies = test_getCookie(driver)
    print("开始开始")
    cookies = test_readCookies()
    # print("cookies是：",cookies)
    # list_url = getConstant.IP+"/dcms/ccsCase/Case-callsavelist.action?menuId=402880822f9490ad012f949eb313008a"
    list_url = getConstant.IP+"/dcms/cwsCase/Case-startlist.action?menuId=4028338158a414bd0158a4848a7f000d&keywords=402880ea2f6bd924012f6c521e8c0034"
    header = {
        "Cookie":cookies
    }
    respons = requests.get(url = list_url,headers=header).text
    return respons

#进入详情并立案
def test_detailsAndFiling():
    # 获取待立案列表
    res = test_toBePutOnRecordList()
    result = BeautifulSoup(res,'html.parser')
    # 获取class为mainContentTableContainer的div对象
    divObj = result.find('div', attrs={'class': 'mainContentTableContainer'})
    tables = divObj.findAll('table')[1]
    # print("列表结果是：",tables)
    # 获取正则第一个匹配的对象
    pattern  = re.compile('<tr id="(.*?)"')
    result  = pattern.search(str(tables))
    # print(result.group(1))
    if result:
        orderId = result.group(1)
        detail_url = getConstant.IP+"/dcms/cwsCase/Case-startview.action?id="+orderId+"&menuId=4028338158a414bd0158a4848a7f000d"
        cookie = test_readCookies()
        header = { "Cookie" : cookie }
        res = requests.get(url=detail_url,headers=header).text
        print("详情结果是：",res)
        str_data = test_read_txt("E:/test/dcms/ChengGuan/testFile/lian.txt")
        li_list = str_data.split(',')
        lian_menuid = re.compile('<input type="hidden" name="menuId" id="menuId" value="(.*?)"/>').search(res).group(1)
        lian_eorcdictname = re.compile('<input type="hidden" name="eorc.dictname" id="eorcdictname" value="(.*?)"/>').search(res).group(1)
        lian_taskcasestateid = re.compile('<input type="hidden" id="taskcasestateid" name="taskcasestateid" value="(.*?)"/>').search(res).group(1)
        lian_mposb = re.compile('<input type="hidden" id="mposb" name="mposb" value="(.*?)">').search(res).group(1)
        lian_gridid = re.compile('<input type="hidden" id="gridid" name="gridid" value="(.*?)">').search(res).group(1)
        lian_bgadminidid = re.compile('<input type="hidden" id="bgadminidid" name="bgadminid.id" value="(.*?)">').search(res).group(1)
        lian_bgcodeid = re.compile('<input type="hidden" id="bgcodeid" name="bgcode.id" value="(.*?)">').search(res).group(1)
        lian_casesource = re.compile('<input type="hidden" id="casesource" name="casesource" value="(.*?)">').search(res).group(1)
        lian_eorc_id = re.compile('<input type="hidden" id="eorc.id" name="eorc.id" value="(.*?)"/>').search(res).group(1)
        lian_eventtypeoneId = re.compile('<input type="hidden" id="eorc.id" name="eorc.id" value="(.*?)"/>').search(res).group(1)
        lian_eventtypetwoId = re.compile('<input type="hidden" id="eorc.id" name="eorc.id" value="(.*?)"/>').search(res).group(1)	
        
        lian_fieldintro = re.compile('<textarea id="fieldintro" rows="2" name="fieldintro">(.*?)</textarea>').search(res).group(1)
        lian_description = re.compile('<textarea id="description" rows="2" name="description" class="(.*?)">(.*?)</textarea>').search(res).group(2)
        lian_url = getConstant.IP+"/dcms/cwsCase/Case-startupdate.action"
        str_data = test_read_txt("E:/test/dcms/ChengGuan/testFile/lian.txt")
        li_list = str_data.split(',')
        lian_data = {
            "menuId": lian_menuid,
            "eorc.dictname":lian_eorcdictname,
            "id":orderId,
            "taskcasestateid":lian_taskcasestateid,
            "resultprocess":li_list[0],
            "px":"",
            "py":"",
            "deptId":"",
            "mposb":lian_mposb,
            "objcode":"",
            "gridid":lian_gridid,
            "bgadminid.id":lian_bgadminidid,
            "imageid":"",
            "bgcode.id":lian_bgcodeid,
            "casesource":lian_casesource,
            "eorc.id":lian_eorc_id,
            "eventtypeone.id":li_list[1],
            "eventtypetwo.id":li_list[2],
            "fieldintro":lian_fieldintro,
            "description":lian_description,
            "startConditionId":li_list[3],
            "operatingComments":li_list[4],
            "sentence":""
        }
        print("orderId的值是",orderId)
        lian_result = requests.post(lian_url,lian_data,headers=header).text
        print("立案返回值是：",type(lian_result),lian_result)
        return lian_result

    else:
        print("列表暂无数据！！！")



# 进入详情不予立案
def test_detailsAndNoFiling():
     # 获取待立案列表
    res = test_toBePutOnRecordList()
    result = BeautifulSoup(res,'html.parser')
    # 获取class为mainContentTableContainer的div对象
    divObj = result.find('div', attrs={'class': 'mainContentTableContainer'})
    tables = divObj.findAll('table')[1]
    # print("列表结果是：",tables)
    # 获取正则第一个匹配的对象
    pattern  = re.compile('<tr id="(.*?)"')
    result  = pattern.search(str(tables))
    # print(result.group(1))
    if result:
        orderId = result.group(1)
        detail_url = getConstant.IP+"/dcms/cwsCase/Case-startview.action?id="+orderId+"&menuId=4028338158a414bd0158a4848a7f000d"
        cookie = test_readCookies()
        header = { "Cookie" : cookie }
        res = requests.get(url=detail_url,headers=header).text
        print("详情结果是：",res)
        str_data = test_read_txt("E:/test/dcms/ChengGuan/testFile/liAn/lian.txt")
        li_list = str_data.split(',')
        lian_menuid = re.compile('<input type="hidden" name="menuId" id="menuId" value="(.*?)"/>').search(res).group(1)
        lian_eorcdictname = re.compile('<input type="hidden" name="eorc.dictname" id="eorcdictname" value="(.*?)"/>').search(res).group(1)
        lian_taskcasestateid = re.compile('<input type="hidden" id="taskcasestateid" name="taskcasestateid" value="(.*?)"/>').search(res).group(1)
        lian_mposb = re.compile('<input type="hidden" id="mposb" name="mposb" value="(.*?)">').search(res).group(1)
        lian_gridid = re.compile('<input type="hidden" id="gridid" name="gridid" value="(.*?)">').search(res).group(1)
        lian_bgadminidid = re.compile('<input type="hidden" id="bgadminidid" name="bgadminid.id" value="(.*?)">').search(res).group(1)
        lian_bgcodeid = re.compile('<input type="hidden" id="bgcodeid" name="bgcode.id" value="(.*?)">').search(res).group(1)
        lian_casesource = re.compile('<input type="hidden" id="casesource" name="casesource" value="(.*?)">').search(res).group(1)
        lian_eorc_id = re.compile('<input type="hidden" id="eorc.id" name="eorc.id" value="(.*?)"/>').search(res).group(1)
        lian_fieldintro = re.compile('<textarea id="fieldintro" rows="2" name="fieldintro">(.*?)</textarea>').search(res).group(1)
        lian_description = re.compile('<textarea id="description" rows="2" name="description" class="(.*?)">(.*?)</textarea>').search(res).group(2)
        lian_url = getConstant.IP+"/dcms/cwsCase/Case-startupdate.action"
        str_data = test_read_txt("E:/test/dcms/ChengGuan/testFile/lian.txt")
        li_list = str_data.split(',')
        lian_data = {
            "menuId": lian_menuid,
            "eorc.dictname":lian_eorcdictname,
            "id":orderId,
            "taskcasestateid":lian_taskcasestateid,
            "resultprocess":"",
            "px":"",
            "py":"",
            "deptId":"",
            "mposb":lian_mposb,
            "objcode":"",
            "gridid":lian_gridid,
            "bgadminid.id":lian_bgadminidid,
            "imageid":"",
            "bgcode.id":lian_bgcodeid,
            "casesource":lian_casesource,
            "eorc.id":lian_eorc_id,
            "eventtypeone.id":li_list[1],
            "eventtypetwo.id":li_list[2],
            "fieldintro":lian_fieldintro,
            "description":lian_description,
            "startConditionId":li_list[3],
            "operatingComments":li_list[4],
            "sentence":""
        }
        print("orderId的值是",orderId)
        lian_result = requests.post(lian_url,lian_data,headers=header).text
        print("立案返回值是：",type(lian_result),lian_result)
        return lian_result

    else:
        print("列表暂无数据！！！")

# 进入详情退回核实
def test_detailsAndReturnVerification():
    pass



if __name__=="__main__": 
        # driver = webdriver.Chrome("D:/python/chromeDriverSever/chromedriver.exe") 
        # test_toBePutOnRecordList()
        test_detailsAndFiling()
        # test_putOnRecord()
        # driver.close()