# -*- coding: utf-8 -*-
import requests
import json ,re  
import sys
sys.path.append("E:/test/dcms/ChengGuan")
import time
from bs4 import BeautifulSoup
from config.Log import logging
from common.writeAndReadText import writeAndReadTextFile
from common.constant_all import getConstant

#查询待派发案卷列表    
def test_PendingDistributionList():
    cookies = writeAndReadTextFile().test_readCookies()
    list_url = getConstant.IP_WEB_180+"/dcms/cwsCase/Case-dispatchlist.action?casestate=20&menuId=4028338158a414bd0158a484daae000e&keywords=402880ea2f6bd924012f6c521e8c0034"
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
        detail_url = getConstant.IP_WEB_180+"/dcms/cwsCase/Case-dispatchview.action"
        cookie = writeAndReadTextFile().test_readCookies()
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
        if not deptname.strip() and not dispatchDeptid.strip():
            deptname = '市环保局'
            dispatchDeptid = '市环保局'
            dispatchUserid = "402883845dc59a63015dc68f5b7b034c"
            dispatchDeptid = "402881795947f3d80159481d06e50097"
        pfdata = writeAndReadTextFile().test_read_txt("E:/test/dcms/ChengGuan/testFile/paiFa/paifa.txt")
        pf_list = pfdata.split(',')
        #派发
        pf_url = getConstant.IP_WEB_180+"/dcms/cwsCase/Case-dispatch.action"
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
        if int(pf_result) == 0:
            print("派发:派发成功，返回值是：",pf_result)
            return pf_result
        elif int(pf_result) == 1:
            print("XXXXXXXXXX派发: 对不起不可以重复派发，返回值是：",pf_result)
        else:
            print("派发:派发失败，返回值是：",pf_result)
    else:
        print("待派发列表暂无数据！！！")



# if __name__=="__main__": 
#     test_sendDetailsAndSendOut()