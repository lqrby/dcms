# -*- coding: utf-8 -*-

import requests
from selenium import webdriver
import json  
import re
import sys
sys.path.append("E:/test/dcms/ChengGuan")
from bs4 import BeautifulSoup
from config.Log import logging
from common.writeAndReadText import writeAndReadTextFile
from common.constant_all import getConstant

class deleteFile():
    def __init__(self,condition):
        self.condition = condition
        if '180' in getConstant.IP:
            self.ip = getConstant.IP+getConstant.PORT_7897
        elif '91' in getConstant.IP:
            self.ip = getConstant.IP
        else:
            print("正式库不允许删除案卷！！！")
            self.ip = getConstant.IP+getConstant.PORT_7897
            
        self.gjxtId = writeAndReadTextFile().test_read_systemId('构建系统')
        self.header = {"Cookie":writeAndReadTextFile().test_readCookies()}

    #精确查询未结案的案卷 
    def test_accurateQuery(self):
        queryurl = self.ip+"/dcms/bmsAdmin/PlCaseUpdateAndDel-list.action"
        if 'caseid' in self.condition:
            caseid = self.condition['caseid']
        if 'description' in self.condition:
            description = self.condition['description']
        if caseid != "" or description != "":
            querydata= {
                'page.pageSize':'10',
                'caseType':	"",
                'id':"",	
                'caseid':caseid,
                'description':description,
                'page.pageNo':'1',
                'menuId':'2c94c6a23241b2b0013241b578070019',
                'keywords':self.gjxtId
            } 
            queryRes = requests.post(queryurl,data = querydata,headers = self.header,allow_redirects=False)
            query_res = queryRes.text
            if '<span id="pagemsg"' in query_res:
                number = re.compile('<label>总共(.*?)页,(.*?)条记录</label>').search(query_res).group(2)
                if number > '0':
                    return query_res
                else:
                    print("0000000000查询结果为空0000000000")
                    return False
            elif '/dcms/bms/login' in queryRes.headers['Location']:
                print("对不起，请您先登录！！！")
                return False
            else:
                print("XXXXXXXXXXXXXXXXXXXXXXXXXXX查询出错XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX")
                return False
        else:
            print("请输入要删除案卷的条件！！！")
            return False


    #根据案卷编号精确删除未结案的案卷  
    def test_PreciseDeletion(self):
        queryResult = self.test_accurateQuery()
        if queryResult != False:
            del_url = self.ip+"/dcms/bmsAdmin/PlCaseUpdateAndDel-deleteComplete.action"
            menuId = re.compile('<input type="hidden" name="menuId" id="menuId" value="(.*?)"/>').search(queryResult).group(1)
            ids_arr = re.compile('<input name="ids" id="ids" type="checkbox" value="(.*?)" />').findall(queryResult)
            
            for ids in ids_arr:
                del_data = {
                    'page.pageSize':'10',
                    'caseType':	'',
                    'id':'',	
                    'caseid':self.condition['caseid'],
                    'description':'',	
                    'ids':ids,
                    'page.pageNo':'1',
                    'menuId':menuId,
                    'keywords':	''
                }
                del_res = requests.post(del_url,data = del_data,headers = self.header,allow_redirects=False)
                if 'Location' in del_res.headers and '/PlCaseUpdateAndDel-list.action' in del_res.headers['Location']:
                    print("***************删除成功************")
                else:
                    print("XXXXXXXXXXXXXXX删除失败XXXXXXXXXXXXXXXX")


    
if __name__=="__main__": 
    condition = {}
    condition['caseid'] = "201811280003"
    condition['description'] = ""

    for i in range(1):
        deleteFile(condition).test_PreciseDeletion()
