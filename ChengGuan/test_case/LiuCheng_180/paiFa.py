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

class distribution():
    def __init__(self,item):
        self.item = item
    #查询待派发案卷列表    
    def test_PendingDistributionList(self):
        cookies = writeAndReadTextFile().test_readCookies()
        list_url = getConstant.IP_WEB_91+"/dcms/cwsCase/Case-dispatchlist.action?casestate=20&menuId=4028338158a414bd0158a484daae000e&keywords=402880ea2f6bd924012f6c521e8c0034"
        header = {
            "Cookie":cookies
        }
        respons = requests.get(url = list_url,headers=header).text
        
        if '<span id="pagemsg"' in respons:
            return respons
        elif '<title>登录</title>' in respons:
            print("对不起请先登录web端")
            return False

    #进入待派发案卷详情并派发
    def test_sendDetailsAndSendOut(self):
        
        pf_res = self.test_PendingDistributionList() # 获取待派发列表
        if pf_res != False:
            result = BeautifulSoup(pf_res,'html.parser')
            number= re.compile('<span id="pagemsg" style="(.*?)"><label>总共(.*?)页,(.*?)条记录</label></span>').search(pf_res).group(3)
            divObj = result.find('div', attrs={'class':'mainContentTableContainer'})
            dcl_tr = divObj.findAll('table')[1].findAll('tr')[1]
            str_tr = str(dcl_tr)
            if number > "0":
                menuId = re.compile('<input type="hidden" id="menuId" name="menuId" value="(.*?)" />').search(pf_res).group(1)
                case_state = re.compile('<input type="hidden" name="casestate" id="casestate" value="(.*?)"/>').search(pf_res).group(1)
                Matching_result = re.compile(r'<tr[\s\S]*id="(.*?)"[\s\S]*onclick="casedo[\(](.*?),(.*?),(.*?),(.*?),this[\)]">').search(str_tr)
                
                dpf_id = Matching_result.group(1)
                dpf_taskprocessId = Matching_result.group(5).strip("'")
                # 进入待派发案卷详情
                detail_url = getConstant.IP_WEB_91+"/dcms/cwsCase/Case-dispatchview.action"
                cookie = writeAndReadTextFile().test_readCookies()
                header = { "Cookie" : cookie }
                dpfdata = {
                    "casestate":case_state,
                    "id":dpf_id,
                    "menuId":menuId,
                    "taskprocess":dpf_taskprocessId
                }

                paifa_res = requests.post(url = detail_url,data = dpfdata,headers = header).text
                # print("详情结果是：",paifa_res)
                taskcasestateid = re.compile('<input type="hidden" id="taskcasestateid" name="taskcasestateid" value="(.*?)"/>').search(paifa_res).group(1)
                applyreturnlist = re.compile('<input type="hidden" id="applyreturnlist" name="applyreturnlist" value="(.*?)" />').search(paifa_res).group(1)
                if self.item == {}:
                    dispatchDeptname = re.compile('<input type="hidden" name="dispatchDeptname" value="(.*)" id="dispatchDeptname"/>').search(paifa_res).group(1)
                    dispatchDeptid = re.compile('<input type="hidden"  readonly="" id="dispatchDeptid" name="dispatchDeptid"  value="(.*?)"  >').search(paifa_res).group(1)
                    dispatchUserid = re.compile('<input type="hidden"  readonly="" id="dispatchUserid" name="dispatchUserid"  value="(.*?)"  >').search(paifa_res).group(1)
                    deptname = re.compile('<input type="text" onclick="(.*?)" readonly="" id="deptname" name="(.*?)" value="(.*?)">').search(paifa_res).group(1)
                else:
                    deptname = self.item["deptname"]
                    dispatchDeptname = self.item["dispatchDeptname"]
                    dispatchDeptid = self.item["deptid"]
                    dispatchUserid = self.item["id"]
                if not deptname.strip() and not dispatchDeptid.strip():
                    deptname = '市环保局'
                    dispatchDeptname = '市环保局'
                    dispatchUserid = "402883845dc59a63015dc68f5b7b034c"
                    dispatchDeptid = "402881795947f3d80159481d06e50097"
                # pfdata = writeAndReadTextFile().test_read_txt("E:/test/dcms/ChengGuan/testFile/paiFa/paifa.txt")
                # pf_list = pfdata.split(',')
                #派发
                pf_url = getConstant.IP_WEB_91+"/dcms/cwsCase/Case-dispatch.action"
                pf_data = {
                    "taskcasestateid":taskcasestateid,
                    "menuId":menuId,
                    "casestate":case_state,
                    "id":dpf_id,
                    "taskprocess":dpf_taskprocessId,
                    "resultprocess":self.item["resultprocess"],
                    "applyreturnlist":applyreturnlist,
                    "limittime":self.item["limittime"],
                    "dispatchDeptname":dispatchDeptname,
                    "dispatchDeptid":dispatchDeptid,
                    "dispatchUserid":dispatchUserid,
                    "deptname":deptname,
                    "operatingComments":self.item["operatingComments"],
                    "sentence":""
                }
                pf_result = requests.post(pf_url,pf_data,headers=header).text
                if pf_result == "0":
                    print("派发:派发成功，返回值是：",pf_result)
                    return True
                elif pf_result == "1":
                    print("XXXXXXXXXX派发: 对不起不可以重复派发，返回值是：",pf_result)
                    return False
                else:
                    print("派发:派发失败，返回值是：",pf_result)
                    return False
            else:
                print("待派发列表暂无数据！！！")
                return False



# if __name__=="__main__": 

#     loginItemsUser = writeAndReadTextFile().test_read_appLoginResult()
#     loginItem_qsdw = loginItemsUser['qsdw']['user']
#     item = {}
#     item['id'] = loginItem_qsdw['id']
#     item["deptname"] = loginItem_qsdw['deptname']
#     item["dispatchDeptname"] = loginItem_qsdw['deptname']
#     item["deptid"] = loginItem_qsdw['deptid']
#     distribution().test_sendDetailsAndSendOut(item)