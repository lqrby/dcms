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
        if '180' in getConstant.IP:
            self.ip = getConstant.IP+getConstant.PORT_7897
        else:
            self.ip = getConstant.IP
        self.header = {
            "User-Agent":"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36",
            "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
            "Accept-Encoding":"gzip, deflate",
            "Accept-Language":"zh-CN,zh;q=0.9,en;q=0.8",
            "Cookie":writeAndReadTextFile().test_readCookies()
        }

    #查询待派发案卷列表    
    def test_PendingDistributionList(self):
        dpftr = {}
        list_url = self.ip+self.item['pflist_url']
        pfRespons = requests.get(url = list_url,headers=self.header,allow_redirects=False,timeout = 20)
        respons = pfRespons.text
        pfRespons.connection.close()
        if '<span id="pagemsg"' in respons:
            listcount = re.compile('<label>总共(.*?)页,(.*?)条记录</label>').search(respons).group(2)
            if listcount > '0':
                daipaifaresult = BeautifulSoup(respons,'html.parser')
                liandivObj = daipaifaresult.find('div', attrs={'class': 'mainContentTableContainer'})
                liandivObj.findAll('table')[1].findAll('tr')[0].extract()
                dpftrlist = liandivObj.findAll('table')[1].findAll('tr')
                for tr in dpftrlist:
                    tdvalue = tr.findAll('td')[-3].get_text()
                    if 'oderNumber' in self.item and tdvalue == self.item['oderNumber']:
                        dpftr = tr
                        break
                return dpftr
            else:
                print("待派发列表暂时为空！！！")
                
        elif '<title>登录</title>' in respons:
            print("对不起请您先登录PC端")
        else:
            print("XXXXXXXXXX待立案列表查询出错XXXXXXXXXX")

    #进入待派发案卷详情并派发
    def test_sendDetailsAndSendOut(self):
        dpf_tr = self.test_PendingDistributionList() # 获取待派发列表
        # print("待派发列表返回值",pf_res)
        if dpf_tr:
            Matching_result = re.compile(r'<tr[\s\S]*id="(.*?)"[\s\S]*onclick="casedo[\(](.*?),(.*?),(.*?)casestate=(.*?),(.*?),this[\)]">').search(str(dpf_tr))
            dpf_id = Matching_result.group(1)
            casestate = Matching_result.group(5).strip("'")
            dpf_taskprocessId = Matching_result.group(6).strip("'")
            detail_url = self.ip+"/dcms/cwsCase/Case-dispatchview.action"
            dpfxqData = {
                "casestate":"casestate",
                "id":dpf_id,
                "menuId":"4028338158a414bd0158a484daae000e",
                "taskprocess":dpf_taskprocessId
            }
            paifares = requests.get(detail_url,params = dpfxqData,headers = self.header,timeout = 20)
            # print("派发详情结果是：",paifares.text)
            paifa_res = paifares.text
            paifares.connection.close()
            if '<title>派遣案卷</title>' in paifa_res:
                taskcasestateid = re.compile('<input type="hidden" id="taskcasestateid" name="taskcasestateid" value="(.*?)"/>').search(paifa_res).group(1)
                applyreturnlist = re.compile('<input type="hidden" id="applyreturnlist" name="applyreturnlist" value="(.*?)" />').search(paifa_res).group(1)
                if self.item == {}:
                    dispatchDeptname = re.compile('<input type="hidden" name="dispatchDeptname" value="(.*)" id="dispatchDeptname"/>').search(paifa_res).group(1)
                    dispatchDeptid = re.compile('<input type="hidden"  readonly="" id="dispatchDeptid" name="dispatchDeptid"  value="(.*?)"  >').search(paifa_res).group(1)
                    dispatchUserid = re.compile('<input type="hidden"  readonly="" id="dispatchUserid" name="dispatchUserid"  value="(.*?)"  >').search(paifa_res).group(1)
                    deptname = re.compile('<input type="text" onclick="(.*?)" readonly="" id="deptname" name="(.*?)" value="(.*?)">').search(paifa_res).group(1)
                else:
                    deptname = self.item["name"]
                    dispatchDeptname = self.item["deptname"]
                    dispatchDeptid = self.item["deptid"]
                    dispatchUserid = self.item["id"]
                if not deptname.strip() and not dispatchDeptid.strip():
                    deptname = '市环保局'
                    dispatchDeptname = '市环保局'
                    dispatchUserid = "402883845dc59a63015dc68f5b7b034c"
                    dispatchDeptid = "402881795947f3d80159481d06e50097"
                
                #派发/挂起
                # pf_url = self.ip+"/dcms/cwsCase/Case-dispatch.action"
                pf_url = self.ip+self.item['pf_url']
                if 'operatingComments' in self.item:
                    operatingComments = self.item["operatingComments"]
                else:
                    operatingComments = ""
                    
                pf_data = {
                    "taskcasestateid":taskcasestateid,
                    "menuId":"4028338158a414bd0158a484daae000e",
                    "casestate":casestate,
                    "id":dpf_id,
                    "taskprocess":dpf_taskprocessId,
                    "resultprocess":self.item["resultprocess"],
                    "applyreturnlist":applyreturnlist,
                    "limittime":self.item["limittime"],
                    "dispatchDeptname":dispatchDeptname,
                    "dispatchDeptid":dispatchDeptid,
                    "dispatchUserid":dispatchUserid,
                    "deptname":deptname,
                    "operatingComments":operatingComments,
                    "sentence":""
                }
                pf_result = requests.post(pf_url,pf_data,headers=self.header,allow_redirects = False,timeout = 20)
                pf_result.connection.close()
                if pf_result.text == "0" or ('Location' in pf_result.headers and 'cwsCase/Case-dispatchlist.action' in pf_result.headers['Location']):
                    print("**************%s成功******************"%self.item["resultprocess"])
                    return True
                elif pf_result.text == "1":
                    print("_________对不起不可以重复%s_______"%self.item["resultprocess"])
                else:
                    print("XXXXXXXXXXXXXXX%s失败XXXXXXXXXXXXXXXXX"%self.item["resultprocess"])
            else:
                print("XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX进入待派发案卷详情出错XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX")
        else:
            print("待派发列表中没有该工单号:{}".format(self.item['oderNumber']))



# if __name__=="__main__": 

    # loginItemsUser = writeAndReadTextFile().test_read_appLoginResult()
    # item = loginItemsUser['qsdw']['user']
    # item['pflist_url'] = 'http://122.137.242.91/dcms/cwsCase/Case-dispatchlist.action?casestate=20&menuId=4028338158a414bd0158a484daae000e&keywords=402880ea2f6bd924012f6c521e8c0034'
    # # item['id'] = loginItem_qsdw['id']
    # item["deptname"] = loginItem_qsdw['deptname']
    # item["dispatchDeptname"] = loginItem_qsdw['deptname']
    # item["deptid"] = loginItem_qsdw['deptid']
    # distribution().test_sendDetailsAndSendOut(item)
    # distribution(item).test_PendingDistributionList()