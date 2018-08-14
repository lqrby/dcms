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

    #查询待处理案卷列表    
    def test_PendingList(self):
        cookies = writeAndReadTextFile().test_readCookies()
        dcl_url = getConstant.IP_WEB_180+"/dcms//cwsCase/Case-deallist.action?casestate=30&menuId=402880822f9490ad012f949be0e80053&keywords=402880eb2f90e905012f9138a5fb00a4"
        header = {
            "Cookie":cookies
        }
        respons = requests.get(url = dcl_url,headers=header).text
        # print("待处理列表",respons)
        return respons

    #进入待处理案卷详情并处理
    def test_handlingDetailsAndHandling(self):
        # 获取待处理列表
        res = self.test_PendingList()
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
            dclxq_url = getConstant.IP_WEB_180+"/dcms/cwsCase/Case-dealview.action?id="+dclid+"&menuId="+dcl_menuid+"&taskprocess="+dcl_taskprocess
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
#查询app待处理案卷列表(权属单位环保局cshbj)    
    def test_app_qsdw_PendingList(self):
        loginitems = writeAndReadTextFile().test_read_appLoginResult()
        qsdwItem = loginitems['qsdw']
        if qsdwItem['message'] == 'success':
            qsdwUser = qsdwItem['user']
            qsdw_userId = qsdwUser['id']
            qsdw_deptId = qsdwUser['deptid']
            app_dcl_url = getConstant.IP_WEB_180+"/dcms/PwasAdmin/MobileCase-deallist.action"
            app_dcl_data = {
                "casestate":"30",
                "description":"",
                "page.pageSize":"20",
                "deptid":qsdw_deptId,
                "startTime":"",
                "endTime":"",
                "userid":qsdw_userId,
                "page.pageNo":"1"
            }   
            respons = requests.post(app_dcl_url,app_dcl_data).text
            # print("app待处理列表",respons)
            return respons
        else:
            print("请先登录权属单位apk！！！")
            return False
        


    #权属单apk位进入待处理案卷详情并处理
    def test_app_qsdw_handlingDetailsAndHandling(self):
        # 获取待处理列表
        qsdw_res = self.test_app_qsdw_PendingList()
        if qsdw_res != None:
            qsdw_list = json.loads(qsdw_res)
            if 'message' in qsdw_list and qsdw_list['message']=='success':
                # print("待处理(权属单位apk)：案卷列表查询成功")
                if qsdw_list['count']>0:
                    qsdwItem = qsdw_list['data'][0]
                    qsdw_id = qsdwItem['id']
                    qsdw_isFh = qsdwItem['isFh']
                    qsdw_dealDeptName = qsdwItem['dealDeptName']
                    qsdw_taskID = qsdwItem['taskID']
                    qsdw_stateId = qsdwItem['stateId']
                    login_qsdwItem = writeAndReadTextFile().test_read_appLoginResult()
                    qsdwItem = login_qsdwItem['qsdw']
                    if qsdwItem['message']== 'success':
                        qsdwUser = qsdwItem['user']
                        qsdw_userId = qsdwUser['id']
                        qsdw_username = qsdwUser['name']
                        qsdw_deptId = qsdwUser['deptid']
                    cl_url = getConstant.IP_WEB_180+"/dcms/PwasAdmin/MobileCase-deal.action"
                    cl_data = {
                        "operatingComments":"处理完成",
                        "username":qsdw_username,
                        "stateId":qsdw_stateId,
                        "isFh":qsdw_isFh,                               
                        "deptid":qsdw_deptId,
                        "deptname":qsdw_dealDeptName,
                        "caseid":qsdw_id,
                        "resultprocess":"案件回访",
                        "userid":qsdw_userId,
                        "taskprocess":qsdw_taskID
                    }
                    cl_res = requests.post(cl_url,cl_data).text
                    clres = json.loads(cl_res)
                    if 'message' in clres and clres['message'] == 'success':
                        print("处理(权属单位apk)：处理成功")
                        return True
                    else:
                        print("XXXXXXXXXX处理(权属单位apk)：处理时出现错误XXXXXXXXXX")
                        return False
                    
    # *********************************************************************************************************
    #执法局app查询待处理案卷列表(执法局待处理案卷)    
    def test_app_zfj_PendingList(self):
        login_items = writeAndReadTextFile().test_read_appLoginResult()
        zfjItem = login_items['zfj']
        if zfjItem['message']== 'success':
            zfjUser = zfjItem['user']
            zfj_userId = zfjUser['id']
            zfj_deptId = zfjUser['deptid']
            appdcl_url = getConstant.IP_WEB_180+"/dcms/PwasAdmin/MobileCase-deallist.action"
            appdcl_data = {
                "casestate":"30",
                "description":"",
                "page.pageSize":"20",
                "deptid":zfj_deptId,
                "startTime":"",
                "endTime":"",
                "userid":zfj_userId,
                "page.pageNo":"1"
            }   
            zfj_respons = requests.post(appdcl_url,appdcl_data).text
            return zfj_respons
        else:
            print("请先登录移动端执法局apk")

    #执法局app进入待处理案卷详情并处理
    def test_app_zfj_handlingDetailsAndHandling(self):
        # 获取待处理列表
        zfj_res = self.test_app_zfj_PendingList()
        if zfj_res != None:
            zfj_list = json.loads(zfj_res)
            if 'message' in zfj_list and zfj_list['message']=='success':
                # print("待处理(执法局apk):案卷列表查询成功")
                if zfj_list['count']>0:
                    zfjItem = zfj_list['data'][0]
                    zfj_id = zfjItem['id']
                    zfj_isFh = zfjItem['isFh']
                    zfj_dealDeptName = zfjItem['dealDeptName']
                    zfj_taskID = zfjItem['taskID']
                    zfj_stateId = zfjItem['stateId']
                    loginItem = writeAndReadTextFile().test_read_appLoginResult()
                    zfjItem = loginItem['zfj']
                    if zfjItem['message']== 'success':
                        zfjUser = zfjItem['user']
                        zfj_userId = zfjUser['id']
                        zfj_username = zfjUser['name']
                        zfj_deptId = zfjUser['deptid']
                    cl_url = getConstant.IP_WEB_180+"/dcms/PwasAdmin/MobileCase-deal.action"
                    cl_data = {
                        "operatingComments":"处理完成",
                        "username":zfj_username,
                        "stateId":zfj_stateId,
                        "isFh":zfj_isFh,                               
                        "deptid":zfj_deptId,
                        "deptname":zfj_dealDeptName,
                        "caseid":zfj_id,
                        "resultprocess":"案件回访",
                        "userid":zfj_userId,
                        "taskprocess":zfj_taskID
                    }
                    zfjcl_res = requests.post(cl_url,cl_data).text
                    zfjclres = json.loads(zfjcl_res)
                    if 'message' in zfjclres and zfjclres['message'] == 'success':
                        print("案卷处理(执法局apk)：处理成功")
                        return True
                    else:
                        print("XXXXXXXXXX案卷处理(执法局apk)：处理案卷出现错误XXXXXXXXXX")
                        return False



# if __name__=="__main__": 
#     # 权属单位案卷处理
#     fileFandling().test_app_qsdw_handlingDetailsAndHandling()
#     # test_app_zfj_handlingDetailsAndHandling()