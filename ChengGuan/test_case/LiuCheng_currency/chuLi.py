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
from requests_toolbelt import MultipartEncoder
from common.appReportPicture import test_app_ReportPicture


class fileFandling():

    def __init__(self,loginUser):
        self.loginUser = loginUser
        if '180' in getConstant.IP:
            self.ip = getConstant.IP+getConstant.PORT_7897
        else:
            self.ip = getConstant.IP

        self.app_header = {
            "User-Agent":"Android/8.0",
            "Connection":"Keep-Alive",
            "Accept-Encoding":"gzip"
        }
        
        self.header = {
            "User-Agent":"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36",
            "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
            "Accept-Encoding":"gzip, deflate",
            "Accept-Language":"zh-CN,zh;q=0.9,en;q=0.8",
            "Cookie":writeAndReadTextFile().test_readCookies()
        }
        self.keywords = writeAndReadTextFile().test_read_systemId('协调系统')


    #web查询待处理案卷列表  
    # web端处理 headers=self.header必须是处理人的cookie,所有必须先登录处理人
    #   
    def test_web_PendingList(self):
        trItem = ""
        dcl_url = self.ip+"/dcms//cwsCase/Case-deallist.action?casestate=30&menuId=402880822f9490ad012f949be0e80053&keywords="+self.keywords
        respons = requests.get(url = dcl_url,headers=self.header,timeout = 15)
        dclItem = respons.text
        respons.connection.close()
        if '<span id="pagemsg"' in dclItem:
            number= re.compile('<span id="pagemsg" style="(.*?)"><label>总共(.*?)页,(.*?)条记录</label></span>').search(dclItem).group(3)
            if number > '0':
                result = BeautifulSoup(dclItem,'html.parser')
                divObj = result.find('div', attrs={'class':'mainContentTableContainer'})
                table = divObj.findAll('table')[1]
                table.findAll('tr')[0].extract()
                for tr in table.findAll('tr'):
                    td_number = tr.findAll('td')[-1]
                    if td_number == self.loginUser['oderNumber']:
                        trItem = tr
                        break
                return trItem
            else:
                print("web端待处理列表暂时为空！！！")
        elif '<title>登录</title>' in dclItem:
            print("对不起请您先登录！！！")
        else:
            print("XXXXXXXXXXXXXXXX查询待处理列表出错XXXXXXXXXXXXXXXXX")
        # print("待处理列表",respons)
        return respons

    #web进入待处理案卷详情并处理
    def test_web_handlingDetailsAndHandling(self):
        # 获取待处理列表
        clres = self.test_web_PendingList()
        if clres:
            pattern = re.compile(r'<tr[\s\S]*id="(.*?)"[\s\S]*onclick="casedo[\(](.*?),(.*?),(.*?),(.*?),this[\)]">')
            dclid = pattern.search(clres).group(1)
            dcl_menuid = pattern.search(clres).group(2).strip("'")
            dcl_taskprocess = pattern.search(clres).group(5).strip("'")
            # 待处理详情url
            dclxq_url = self.ip+"/dcms/cwsCase/Case-dealview.action?id="+dclid+"&menuId="+dcl_menuid+"&taskprocess="+dcl_taskprocess
            dclxq_cookies = writeAndReadTextFile().test_readCookies()
            dclxqres = requests.get(url = dclxq_url,headers=self.header)
            dclxq_res = dclxqres.text
            dclxqres.connection.close()
            cl_taskcasestateid = re.compile('<input type="hidden" id="taskcasestateid" name="taskcasestateid" value="(.*?)"/>').search(dclxq_res).group(1)
            cl_casestate = re.compile('<input type="hidden" id="casestate" name="casestate" value="(.*?)" />').search(dclxq_res).group(1)
            cl_taskDeptID = re.compile('<input type="hidden" id="taskDeptID" name="taskDeptID" value="(.*?)" />').search(dclxq_res).group(1)
            cl_applyreturnlist = re.compile('<input type="hidden" id="applyreturnlist" name="applyreturnlist" value="(.*?)" />').search(dclxq_res).group(1)
            if 'upload' in self.loginUser:
                upload = self.loginUser['upload']
            else:
                upload = ""
            # 处理案卷url
            cl_url = self.ip+"/dcms/cwsCase/Case-deal.action"
            m = MultipartEncoder(
                fields = {
                    "taskcasestateid":cl_taskcasestateid,
                    "menuId":dcl_menuid,
                    "casestate":cl_casestate,
                    "id":dclid,
                    "taskprocess":dcl_taskprocess,
                    "taskDeptID":cl_taskDeptID,
                    "resultprocess":self.loginUser['resultprocess'],
                    "applyreturnlist":cl_applyreturnlist,
                    "operatingComments":self.loginUser['operatingComments'],
                    "upload":upload,
                    "dispatchDeptid":"",
                    "dispatchDeptname":"",
                    "limittime": "",
                    "operatingComments_dis": "",
                    "sentence": ""
                }
            )
            cl_header = {
                "Content-Type":m.content_type,
                "User-Agent":"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36",
                "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
                "Accept-Encoding":"gzip, deflate",
                "Accept-Language":"zh-CN,zh;q=0.9,en;q=0.8",
                "Cookie":writeAndReadTextFile().test_readCookies()
            }
            clresult = requests.post(cl_url,data = m ,headers = cl_header)
            cl_result = clresult.text
            clresult.connection.close()
            return cl_result
        else:
            print("待处理列表暂无数据！！！")
            return False


#移动端案卷处理==================================================================================
#查询app待处理案卷列表
    def test_app_PendingList(self):
        dclitem = {}
        app_dcl_url = self.ip+"/dcms/PwasAdmin/MobileCase-deallist.action"
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
        apprespons = requests.post(app_dcl_url,app_dcl_data,headers = self.app_header,timeout = 20)
        app_respons = apprespons.text
        apprespons.connection.close()
        if 'success' in app_respons:
            result = json.loads(app_respons)
            for item in result['data']:
                if item['caseid'] == self.loginUser['oderNumber']:
                    dclitem = item
                    break
            return dclitem
        else:
            print("XXXXXXXXXXXXXXXXX获取待处理列表失败XXXXXXXXXXXXXXXXX")
    
       
    #进入待处理案卷详情并处理
    def test_app_handlingDetailsAndHandling(self):
        # 获取待处理列表
        dclResult = self.test_app_PendingList()
        if dclResult:
            cl_url = self.ip+"/dcms/PwasAdmin/MobileCase-deal.action"
            cl_data = {
                "operatingComments":self.loginUser['operatingComments'],
                "username":self.loginUser['name'],
                "stateId":dclResult['stateId'],
                "isFh":dclResult['isFh'],                               
                "deptid":self.loginUser['deptid'],
                "deptname":dclResult['dealDeptName'],
                "caseid":dclResult['id'],
                "resultprocess":"案件回访",
                "userid":self.loginUser['id'],
                "taskprocess":dclResult['taskID']
            }
            cl_res = requests.post(cl_url,cl_data,headers = self.app_header,timeout = 20)
            clres = json.loads(cl_res.text)
            if 'message' in clres and clres['message'] == 'success':
                print("案卷处理成功")
                if 'imgPath' in self.loginUser:
                    print("正在上传处理图片......")
                    # 上传图片地址
                    imgUrl = self.ip+"/dcms/PwasAdmin/PwasAdmin-imageup.action?imagetype=image&idcase="+clres['id']+"&prochisid="+clres['taskid']
                    picpath = self.loginUser['imgPath']
                    test_app_ReportPicture(imgUrl,picpath)
                else:
                    print("处理案卷未上传图片")
                return True
            else:
                print("XXXXXXXXXX处理案卷时出现错误XXXXXXXXXX")
            cl_res.connection.close()
        else:
            print("00000待处理列表暂时为空00000")
        
    
    #移动端案卷处理>申请调整==================================================================================
    def test_requestAdjustment(self):
        dclResult = self.test_app_PendingList()
        if dclResult:
            sqtz_url = self.ip+"/dcms/PwasAdmin/MobileCase-applyadjust.action"
            sqtz_data = {
                "operatingComments":self.loginUser['operatingComments'],
                "username":self.loginUser['name'],
                "stateId":dclResult['stateId'],
                "deptid":self.loginUser['deptid'],
                "deptname":dclResult['dealDeptName'],
                "caseid":dclResult['id'],
                "resultprocess":self.loginUser['resultprocess'],
                "applyReason":self.loginUser['applyReason'],
                "userid":self.loginUser['id'],
                "taskprocess":dclResult['taskID']
            }
            sqtz_res = requests.post(sqtz_url,sqtz_data,headers = self.app_header,timeout = 20)
            sqtzres = json.loads(sqtz_res.text)
            sqtz_res.connection.close()
            if 'message' in sqtzres and sqtzres['message'] == 'success':
                print("***************申请调整成功*************")
                return True
        else:
            print("待处理列表中没有该工单号:{}".format(self.loginUser['oderNumber']))
 




                        

                    
   

# if __name__=="__main__": 
#     # 权属单位案卷处理
#     loginitems = writeAndReadTextFile().test_read_appLoginResult()
#     loginUser = loginitems['qsdw']['user']
#     loginUser['resultprocess'] = '申请调整'   #不可更改
#     loginUser['operatingComments'] = '请求调整'  #
#     loginUser['applyReason'] = '非我辖区'  #调整原因
#     loginUser = fileFandling(loginUser).test_requestAdjustment()
    