# -*- coding: utf-8 -*-

import requests
import json,random 
import sys,re
sys.path.append("E:/test/dcms/ChengGuan")
import time
# import xml.etree.ElementTree as ET
from bs4 import BeautifulSoup,SoupStrainer
from config.Log import logging
from common.writeAndReadText import writeAndReadTextFile
from common.constant_all import getConstant
from requests_toolbelt import MultipartEncoder
from common.appReportPicture import test_app_ReportPicture

class colligateQuery():
    def __init__(self,loginItems):
        self.loginItems = loginItems
        if '180' in getConstant.IP:
            self.ip = getConstant.IP+getConstant.PORT_7897
        else:
            self.ip = getConstant.IP

        self.menuId = '4028838358b7f73b0158b9e7f3480c59'
        self.keywords = '402880ea2f6bd924012f6c521e8c0034'

        self.header = {
            "Cookie":writeAndReadTextFile().test_readCookies(),
            "Upgrade-Insecure-Requests": "1",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
            "Accept-Encoding": "gzip, deflate",
            "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8"
        }
        self.app_header = {
            "User-Agent":"Android/8.0",
            "Content-Type":"application/x-www-form-urlencoded",
            "Connection":"Keep-Alive",
            "Accept-Encoding":"gzip"
        }
        
    # WEB端综合查询列表列表（默认查询当天的案卷）
    def test_web_zongHeList(self):
        zhcxurl = self.ip+"/dcms/bmsUniversal/UniversalCaseQuery-list.action?menuId={}&keywords={}".format(self.menuId,self.keywords)
        zhcx_res = requests.get(zhcxurl,headers = self.header, allow_redirects=False)
        zhcx_res.connection.close()
        if zhcx_res.status_code == 200:
            print("WEB端综合查询列表成功")
            return zhcx_res.text
        elif zhcx_res.status_code == 302:
            print("XXXXXXXXXXXXXXXXXXX您还未登录XXXXXXXXXXXXXXXXXXX")
            return False
        else:
            print("XXXXXXXXXXXXXXXXXWEB端综合查询列表出错XXXXXXXXXXXXXXXXXX")
            return False
        
    
    #WEB端查看综合查询案卷详情
    def test_web_zongHeDetail(self):
        zonghe_res = self.test_web_zongHeList()
        if zonghe_res:
            zhcx_count = re.compile('<label>总共(.*?)页,(.*?)条记录</label>').search(zonghe_res).group(2)
            if zhcx_count > "0":
                zhcx_list = re.compile('<tr  id="(.*?)"').findall(zonghe_res)
                # print(zhcx_list)
                if len(zhcx_list) > 5:
                    zhcx_list = random.sample(zhcx_list, 5)  #从list中随机获取5个元素，作为一个片断返回  
                for itemId in zhcx_list:
                    #查看详情
                    detail_url = self.ip+"/dcms/cwsCase/Case-caseinfo.action?id={}&menuId=4028838358b7f73b0158b9e7f3480c59".format(itemId)
                    detailres = requests.get(detail_url,headers = self.header, allow_redirects=False,timeout = 20)
                    detailres.connection.close()
                    time.sleep(random.randint(1,2)) 
                    if detailres.status_code == 200 and '案卷编号' in detailres.text:
                        result = BeautifulSoup(detailres.text,'html.parser')
                        divObj = result.find('div', attrs={'class': 'detailCaseInfo'})
                        detail_tr = divObj.find('table').findAll('tr')[0].findAll('td')[1]
                        bianhao = detail_tr.get_text()
                        print("综合查询》查看案卷({})详情成功".format(bianhao))
                    else:
                        print("XXXXXXXXXXXXXXXX综合查询》查看案卷({})详情失败XXXXXXXXXXXXXXXX".format(bianhao))
                    
                    #查看流转记录
                    liuzhuanURL = self.ip+"/dcms/cwsCase/Case-caseprochis.action?id=4028838467abbb930167c4442e7a0255&needImageInProchis=false"
                    liuzhuanRes = requests.get(liuzhuanURL,headers = self.header, allow_redirects=False,timeout = 20)
                    liuzhuanRes.connection.close()
                    if '办理操作' in liuzhuanRes.text:
                        print("WEB端综合查询》查看案卷详情》查看({})流转记录成功".format(bianhao))
                    else:
                        print("XXXXXXXXXXXXXXXXWEB端综合查询》查看案卷详情》查看({})流转记录失败XXXXXXXXXXXXXXX".format(bianhao))
            else:
                print("WEB端综合查询列表暂无数据！！！")

    #WEB端导出本页/导出全部
    def test_ExportThisPage(self):
        zonghelist = self.test_web_zongHeList()
        if zonghelist:
            zhcxcount = re.compile('<label>总共(.*?)页,(.*?)条记录</label>').search(zonghelist).group(2)
            if zhcxcount > "0":
                daochuURL = self.ip+"/dcms/bmsUniversal/UniversalCaseQuery-exportfileall.action"
                for mark_number in loginItems['markNum']:
                    daochuData = {
                        "isExport":mark_number,
                        "caseid":"",	
                        "casestateid.id":"",	
                        "pf":"",	
                        "source.id":"",	
                        "id":"",	
                        "description":"",
                        "fieldintro":"",	
                        "regioncode":"",
                        "bgadminid.id":"",	
                        "starttime":time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
                        "endstarttime":"",	
                        "chengbanbumenId":"",	
                        "eorc.id":"",	
                        "eventtypeone.id":"",	
                        "eventtypetwo.id":"",	
                        "deptid":"",	
                        "zxuserid":"",
                        "page.pageNo":"1",
                        "menuId":self.menuId,
                        "keywords":self.keywords
                    }
                    daochures = requests.post(daochuURL,daochuData,headers = self.header, allow_redirects=False,timeout = 20)
                    
                    if mark_number == 2:
                        if daochures.status_code == 200:
                            print("综合查询》导出本页成功")
                        else:
                            print("XXXXXXXXXX综合查询》导出本页失败XXXXXXXXX",daochures.status_code)
                    else:
                        if daochures.status_code == 200:
                            print("综合查询》全部导出成功")
                        else:
                            print("XXXXXXXXXX综合查询》全部导出失败XXXXXXXXX",daochures.status_code)
                    daochures.connection.close()
                    time.sleep(random.randint(2,5)) 

            else:
                print("导个毛线，综合查询列表暂无数据！！！")
    #==================================================================================================================
    #app移动端综合查询模块(综合查询列表)
    def test_app_zongHeList(self):
        appzhcxurl = self.ip+"/dcms/pwasCase/Case-pdacaseprochislist.action"
        appData = {
            "eorc.id":"", 
            "description":"", 
            "startdate":"", 
            "eventtypeone.id":"", 
            "page.pageSize":"20",
            "casestateid.id":"", 
            "bgadminid.id":self.loginItems['zfj']['user']['id'],
            "eventtypetwo.id":"",
            "bgcode.id":"", 
            "enddate":"", 
            "page.pageNo":"1"
        }
        appzhcx_res = requests.post(appzhcxurl,appData,headers = self.app_header, allow_redirects=False,timeout = 20)
        appzhcx_res.connection.close()
        if appzhcx_res.status_code == 200 and '<caseQueryList count=' in appzhcx_res.text:
            return appzhcx_res.text
        elif appzhcx_res.status_code == 302:
            print("XXXXXXXXXXXXXXXXXXX您还未登录XXXXXXXXXXXXXXXXXXX")
            return False
        else:
            print("XXXXXXXXXXXXXXXXX综合查询列表出错XXXXXXXXXXXXXXXXXX")
            return False

    #app移动端综合查询中的案卷详情     
    def test_app_anJuanDetail(self):
        zongHeList = self.test_app_zongHeList()
        count = re.compile('count="(.*?)"').search(zongHeList).group(1)
        if count > "0":
            print("综合查询列表成功")
            zongHe_List = BeautifulSoup(zongHeList,'xml')
            caseQueryRecordArr = zongHe_List.findAll('caseQueryRecord')
            for caseQueryRecord in caseQueryRecordArr:
                # print("编码是:",caseQueryRecord.idcase.string,
                #       "状态是:",caseQueryRecord.casestateid.string)
                detailUrl = self.ip+"/dcms/PwasAdmin/PwasAdmin-getImg.action"  
                detailData = {'caseId':caseQueryRecord.idcase.string}
                appDetailRes = requests.post(detailUrl,detailData,headers = self.app_header, allow_redirects=False,timeout = 20)
                appDetailRes.connection.close()
                if 'success' in appDetailRes.text:
                    detailObj = json.loads(appDetailRes.text)
                    if detailObj['data']:
                        print("案卷详情是：",detailObj['data'])
                    else:
                        print("XXXXXXXXXXXX案卷单号:{}该案卷详情中的流转记录有错误XXXXXXXXXXXXX".format(caseQueryRecord.caseid.string))

        else:
            print("综合查询列表为空！！！")
        
                

if __name__=="__main__": 
    loginItems = writeAndReadTextFile().test_read_appLoginResult()
    loginItems['markNum'] = [2,1]
    # colligateQuery(loginUser).test_web_zongHeList()  #综合查询列表
    colligateQuery(loginItems).test_web_zongHeDetail() #案卷详情
    # colligateQuery(loginItems).test_ExportThisPage()   #导出

    #app综合查询
    # a = colligateQuery(loginItems).test_app_zongHeList()
    # print(a)
    #案卷查询列表、案卷详情
    colligateQuery(loginItems).test_app_anJuanDetail()