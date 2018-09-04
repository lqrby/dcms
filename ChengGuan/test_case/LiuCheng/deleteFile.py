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


#删除城管未结案的案卷
# 查询所有案卷列表(不包含已结案)
def test_chengGuan_qureyList():
    cookiestr = writeAndReadTextFile().test_readCookies()
    gjxtId = writeAndReadTextFile().test_read_systemId('构建系统')
    gjxt_url = getConstant.IP_WEB_180+"/dcms//bmsAdmin/PlCaseUpdateAndDel-list.action?menuId=2c94c6a23241b2b0013241b578070019&keywords="+gjxtId
    header = {
        "Cookie":cookiestr
    }
    res = requests.get(gjxt_url,headers=header,allow_redirects=False)
    return res

# 选择要删除的案卷并删除
def test_chengGuan_deleteFile(describe):
    dsc_list = []
    file_List = test_chengGuan_qureyList()
    fileList = file_List.text
    obj= re.compile('<span id="pagemsg" style="(.*?)"><label>总共(.*?)页,(.*?)条记录</label></span>').search(fileList)
    if obj != None:
        if int(obj.group(3))>0:
            html_file = BeautifulSoup(fileList,'html.parser')
            table = html_file.find('table', attrs={'class':'ixtablokt'})
            obj_tr = table.findAll('tr')
            del(obj_tr[0])
            if describe == "":
                inputval = obj_tr[0].find('td').find('input')
                input_val = re.search('<input id="ids" name="ids" type="checkbox" value="(.*?)"/>',str(inputval)).group(1)
                dsc_list.append(input_val)
            else:
                for i,item in enumerate(obj_tr):
                    objtd = item.findAll('td')
                    # 案卷列表的列是可变得
                    td_value4 = objtd[6].get_text()
                    tdval4 = td_value4.strip()
                    tdval1 = re.search('<input id="ids" name="ids" type="checkbox" value="(.*?)"/>',str(objtd[0])).group(1)
                    if (tdval4 == describe):
                        dsc_list.append(tdval1)
            if len(dsc_list)>0:
                gjxtId = writeAndReadTextFile().test_read_systemId('构建系统')
                # 删除案卷的url
                dlt_url = getConstant.IP_WEB_180+"/dcms/bmsAdmin/PlCaseUpdateAndDel-deleteComplete.action"
                dsc_header = {
                    "Cookie":writeAndReadTextFile().test_readCookies()
                }
                for ids in dsc_list:
                    dlt_dat = {
                        "page.pageSize":"100",
                        "caseType":"",
                        "id":"",
                        "caseid":"",	
                        "description":"",	
                        "ids":ids,
                        "page.pageNo":"1",
                        "menuId":"2c94c6a23241b2b0013241b578070019",
                        "keywords":gjxtId
                    }
                    dle_res = requests.post(dlt_url,data = dlt_dat,headers=dsc_header,allow_redirects=False)
                    loc_url = getConstant.IP_WEB_180+"/dcms/bmsAdmin/PlCaseUpdateAndDel-list.action?page.pageNo=1&menuId=2c94c6a23241b2b0013241b578070019&msg="
                    if 'Location' in dle_res.headers and dle_res.headers['Location'] == loc_url:
                        print("案卷删除成功")
                    else:
                        print("删除失败，意想不到的错误，请重试")
            else:
                print("列表中的描述没有匹配*****",describe,"*****的删除条件")
    elif ('Set-Cookie' in file_List.headers):
        print("====================对不起请先登录=====================")
    else:
        print("XXXXXXXXXX删除案卷列表:意想不到的错误XXXXXXXXXX")
    

    
if __name__=="__main__": 
    k = ""
    for i in range(100):
        test_chengGuan_deleteFile(k)
