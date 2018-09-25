# -*- coding: utf-8 -*-

import requests
import json
import re
import ast
import sys
sys.path.append("E:/test/dcms/ChengGuan")
import time
from bs4 import BeautifulSoup
from config.Log import logging
from common.constant_all import getConstant
from common.writeAndReadText import writeAndReadTextFile

class fileFandling():

    def __init__(self,loginUser):
        self.loginUser = loginUser

    #web查询待处理案卷列表    
    def test_web_PendingList(self):
        cookies = writeAndReadTextFile().test_readCookies()
        dcl_url = getConstant.IP_WEB_91+"/dcms//cwsCase/Case-deallist.action?casestate=30&menuId=402880822f9490ad012f949be0e80053&keywords=402880eb2f90e905012f9138a5fb00a4"
        header = {
            "Cookie":cookies
        }
        respons = requests.get(url = dcl_url,headers=header).text
        # print("待处理列表",respons)
        return respons

    #web进入待处理案卷详情并处理
    def test_web_handlingDetailsAndHandling(self):
        # 获取待处理列表
        res = self.test_web_PendingList()
        result = BeautifulSoup(res,'html.parser')
        divObj = result.find('div', attrs={'class':'mainContentTableContainer'})
        dcl_tr = divObj.findAll('table')[1].findAll('tr')[1]
        str_tr = str(dcl_tr)
        # print("res的类型是：",tables)
        number= re.compile('<span id="pagemsg" style="(.*?)"><label>总共(.*?)页,(.*?)条记录</label></span>').search(res).group(3)
        if int(number)>0:
            pattern = re.compile(r'<tr[\s\S]*id="(.*?)"[\s\S]*onclick="casedo[\(](.*?),(.*?),(.*?),(.*?),this[\)]">')
            dclid = pattern.search(str_tr).group(1)
            dcl_menuid = pattern.search(str_tr).group(2).strip("'")
            dcl_taskprocess = pattern.search(str_tr).group(5).strip("'")
            # 待处理详情url
            dclxq_url = getConstant.IP_WEB_91+"/dcms/cwsCase/Case-dealview.action?id="+dclid+"&menuId="+dcl_menuid+"&taskprocess="+dcl_taskprocess
            dclxq_cookies = writeAndReadTextFile().test_readCookies()
            header = {
            "Cookie":dclxq_cookies
            }
            dclxq_res = requests.get(url = dclxq_url,headers=header).text
            # print("待处理详情",dclxq_res)
            # -----------------------------------------------------------------
            cllist = writeAndReadTextFile().test_read_txt('E:/test/dcms/ChengGuan/testFile/chuLi/anjuanchuli.txt')
            cl_list = cllist.split(',')
            cl_taskcasestateid = re.compile('<input type="hidden" id="taskcasestateid" name="taskcasestateid" value="(.*?)"/>').search(dclxq_res).group(1)
            cl_casestate = re.compile('<input type="hidden" id="casestate" name="casestate" value="(.*?)" />').search(dclxq_res).group(1)
            cl_taskDeptID = re.compile('<input type="hidden" id="taskDeptID" name="taskDeptID" value="(.*?)" />').search(dclxq_res).group(1)
            cl_applyreturnlist = re.compile('<input type="hidden" id="applyreturnlist" name="applyreturnlist" value="(.*?)" />').search(dclxq_res).group(1)
            # 处理案卷url
            cl_url = getConstant.IP_WEB_180+"/dcms/cwsCase/Case-deal.action"
            cl_data = {
                "taskcasestateid":cl_taskcasestateid,
                "menuId":dcl_menuid,
                "casestate":cl_casestate,
                "id":dclid,
                "taskprocess":dcl_taskprocess,
                "taskDeptID":cl_taskDeptID,
                "resultprocess":cl_list[0],
                "applyreturnlist":cl_applyreturnlist,
                "operatingComments":cl_list[1],
                "upload":"",
                "dispatchDeptid":"",
                "dispatchDeptname":"",
                "limittime": "",
                "operatingComments_dis": "",
                "sentence": ""
            }
            cl_header = {
                "Cookie":dclxq_cookies
            }
            cl_result = requests.post(cl_url,cl_data,headers = cl_header).text
            return cl_result
        else:
            print("待处理列表暂无数据！！！")


#移动端案卷处理==================================================================================
#查询app待处理案卷列表
    def test_app_PendingList(self):
        app_dcl_url = getConstant.IP_WEB_91+"/dcms/PwasAdmin/MobileCase-deallist.action"
        app_dcl_data = {
            "casestate":"30",
            "description":"",
            "page.pageSize":"20",
            "deptid":self.loginUser['deptid'],
            "startTime":"",
            "endTime":"",
            "userid":self.loginUser['id'],
            "page.pageNo":"1"
        }   
        respons = requests.post(app_dcl_url,app_dcl_data).text
        if '"message":"success"' in respons:
            return respons
        else:
            return False
    
        


    #进入待处理案卷详情并处理
    def test_app_handlingDetailsAndHandling(self):
        # 获取待处理列表
        ajlb_Result = self.test_app_PendingList()
        # print(ajlb_Result)
        if ajlb_Result != False:
            ajlbResult = json.loads(ajlb_Result)
            if 'message' in ajlbResult and ajlbResult['message']=='success':
                # print("待处理：案卷列表查询成功")
                if ajlbResult['count']>0:
                    ajxqItem = ajlbResult['data'][0]
                    ajxq_id = ajxqItem['id']
                    ajxq_isFh = ajxqItem['isFh']
                    ajxq_dealDeptName = ajxqItem['dealDeptName']
                    ajxq_taskID = ajxqItem['taskID']
                    ajxq_stateId = ajxqItem['stateId']
                    cl_url = getConstant.IP_WEB_91+"/dcms/PwasAdmin/MobileCase-deal.action"
                    cl_data = {
                        "operatingComments":self.loginUser['operatingComments'],
                        "username":self.loginUser['name'],
                        "stateId":ajxq_stateId,
                        "isFh":ajxq_isFh,                               
                        "deptid":self.loginUser['deptid'],
                        "deptname":ajxq_dealDeptName,
                        "caseid":ajxq_id,
                        "resultprocess":"案件回访",
                        "userid":self.loginUser['id'],
                        "taskprocess":ajxq_taskID
                    }
                    cl_res = requests.post(cl_url,cl_data).text
                    clres = json.loads(cl_res)
                    if 'message' in clres and clres['message'] == 'success':
                        print("处理：处理成功")
                        return True
                    else:
                        print("XXXXXXXXXX处理：处理时出现错误XXXXXXXXXX")
                        return False
                    
   

# if __name__=="__main__": 
#     # 权属单位案卷处理
#     loginitems = writeAndReadTextFile().test_read_appLoginResult()
#     qsdwItem = loginitems['qsdw']
#     # if qsdwItem['message'] == 'success':
#     loginUser = qsdwItem['user']
#     fileFandling(loginUser).test_app_handlingDetailsAndHandling()