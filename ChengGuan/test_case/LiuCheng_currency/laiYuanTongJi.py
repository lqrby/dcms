# -*- coding: utf-8 -*-
import requests
import json,random 
import sys,re
sys.path.append("E:/test/dcms/ChengGuan")
import time,datetime
from bs4 import BeautifulSoup
# from config.Log import logging
from common.writeAndReadText import writeAndReadTextFile
from common.constant_all import getConstant
from requests_toolbelt import MultipartEncoder
from common.appReportPicture import test_app_ReportPicture

#来源统计
class SourceStatistics():
    def __init__(self,loginUser):
        self.loginUser = loginUser
        if '180' in getConstant.IP:
            self.ip = getConstant.IP+getConstant.PORT_7897
        else:
            self.ip = getConstant.IP

        self.menuId = '8a8a8483666270630166627b02900087'
        self.keywords = '402880ea2f6bd924012f6c521e8c0034'

        self.header = {
            "Cookie":writeAndReadTextFile().test_readCookies(),
            "Upgrade-Insecure-Requests": "1",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
            "Accept-Encoding": "gzip, deflate",
            "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8"
        }
        
    # 来源统计
    def test_web_laiYuanTongJiList(self):
        lytj_url = self.ip+"/dcms/ccsCase/CaseAllScs-TjCase.action?menuId={}&keywords={}".format(self.menuId,self.keywords)
        lytj_res = requests.get(lytj_url,headers = self.header,allow_redirects=False,timeout = 20)
        lytj_res.connection.close()
        if lytj_res.status_code == 200 and '<span id="pagemsg"' in lytj_res.text:
            pageCount = re.compile('<label>总共(.*?)页,(.*?)条记录</label>').search(lytj_res.text).group(1)
            lytjUrl = self.ip+"/dcms/ccsCase/CaseAllScs-TjCase.action"
            for pageNum in range(1,int(pageCount)+1):
                lytjData = {
                    "isExport":"",
                    "start":"",	 
                    "end":"",
                    "source.id":"",
                    "id":"",	
                    "did":"",
                    "eorc.id":"",	
                    "eventtypeone.id":"",
                    "eventtypetwo.id":"",
                    "page.pageNo":pageNum,
                    "menuId":self.menuId,
                    "keywords":self.keywords	
                }
                lytjRes = requests.post(lytjUrl,lytjData,headers = self.header,allow_redirects=False,timeout = 20)
                lytjRes.connection.close()
                if lytjRes.status_code == 200 and '<span id="pagemsg"' in lytjRes.text:
                    lytjList = BeautifulSoup(lytjRes.text,'html.parser')
                    tbodyObj = lytjList.find('table', attrs={'class':'ixtablokt'})
                    tbodyObj.findAll('tr')[0].extract()
                    trList = tbodyObj.findAll('tr')
                    print("第{}页共{}条数据".format(pageNum,len(trList)))  #每页15条数据
                    for i,tr in enumerate(trList):
                        # print(tr.findAll('td')[3].get_text(),"****************")
                        # print(tr.findAll('td')[4].get_text(),"****************")
                        td3 = int(tr.findAll('td')[3].get_text())
                        td4 = int(tr.findAll('td')[4].get_text())
                        td5 = int(tr.findAll('td')[5].get_text())
                        td6 = int(tr.findAll('td')[6].get_text())
                        td7 = int(tr.findAll('td')[7].get_text())
                        if td3 == td4+td5+td6+td7:
                            print("===第{}页第{}条数据正常,立案总数:{}===".format(pageNum,i+1,td3))
                        else:
                            print("XXXXXXXXXXXXXXXXXXXXXX第{}页第{}条数据不正常XXXXXXXXXXXXXXXXXXXXXX".format(pageNum,i+1))
                            time.sleep(random.randint(2,3))
                else:
                    print("XXXXXXXXXXXXXXXXX来源统计列表出错XXXXXXXXXXXXXXXXXX")
                    return False
            print("来源统计查询成功")
            return lytj_res.text
        elif lytj_res.status_code == 302:
            print("XXXXXXXXXXXXXXXXXXX您还未登录XXXXXXXXXXXXXXXXXXX")
            return False
        else:
            print("XXXXXXXXXXXXXXXXX来源统计查询失败XXXXXXXXXXXXXX")
            return False



    #来源统计》全部导出/条件搜索
    def test_searchOrExport(self):
        lytjListUrl = self.ip+"/dcms/ccsCase/CaseAllScs-TjCase.action?menuId={}&keywords={}".format(self.menuId,self.keywords)
        lytjListRes = requests.get(lytjListUrl,headers = self.header,allow_redirects=False,timeout = 20)
        lytjListRes.connection.close()
        if lytjListRes.status_code == 200 and '<span id="pagemsg"' in lytjListRes.text:
            lytjRespont = BeautifulSoup(lytjListRes.text,'html.parser')
            divObj = lytjRespont.find('div', attrs={'class':'mainBT'})
            #案卷来源数组
            optionArr = divObj.find('select',attrs={'id':'source'}).findAll('option')
            #部门数组
            departmentArr = divObj.find('select',attrs={'id':'id'}).findAll('option')
            daochuURL = self.ip+"/dcms/ccsCase/CaseAllScs-TjCase.action"
            #开始时间/结束时间
            startAndNedTime = {}
            startAndNedTime2 = {}

            newTime = datetime.datetime.now()-datetime.timedelta(days=30)
            startAndNedTime['start'] = newTime.strftime("%Y-%m-%d %H:%M:%S")
            startAndNedTime['end'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            for option in optionArr:
                isExport = random.choice([1,0]) #是否导出
                if isExport != 1:
                    isExport = ""
                startAndNedTimeArr = random.choice([startAndNedTime,startAndNedTime2])
                #开始结束时间
                if startAndNedTimeArr:
                    start = startAndNedTime['start']
                    end = startAndNedTime['end']
                else:
                    start = ""
                    end = ""
                department = random.choice(departmentArr) #一级部门
                depaturl = self.ip+"/dcms/ccsCase/CaseAllScs-getDeptByParentId.action?parentid="+department['value']
                depatList = requests.get(depaturl,headers = self.header,allow_redirects = False,timeout = 20)
                depat_List = json.loads(depatList.text)
                #二级部门
                if len(depat_List) > 0 :
                    departId = random.choice(depat_List)
                else:
                    departId = ""   
                daochuData = {
                    "isExport":isExport,
                    "start":start,
                    "end":end, 
                    "source.id":option['value'], #来源
                    "id":department['value'], 
                    "did":departId, 
                    "eorc.id":"",	
                    "eventtypeone.id":"",	
                    "eventtypetwo.id":"",
                    "page.pageNo":"1",
                    "menuId":self.menuId,
                    "keywords":self.keywords
                }
                daochures = requests.post(daochuURL,daochuData,headers = self.header, allow_redirects=False,timeout = 20)
                export_obj = daochures.text
                daochures.connection.close()
                time.sleep(random.randint(1,2)) 
                if daochures.status_code == 200:
                    if "记录" in export_obj :
                        print("根据当前条件查询结果为空！！！")
                        print("来源统计》案卷来源:{},业务单位:{},根据当前条件查询结果为空！！！".format(option.get_text(),department.get_text()))
                    else:
                        print("来源统计》案卷来源:{},业务单位:{},并且全部导出成功".format(option.get_text(),department.get_text()))
                else:
                    print("XXXXXXXXXX来源统计》全部导出失败XXXXXXXXX",daochures.status_code)
                depatList.connection.close()
        

if __name__=="__main__": 
    loginUser = {}
    # loginUser1 = {}
    # loginUser2 = {}
    # loginUser3 = {}
    # lytjArr = []

    # loginUser1['isExport'] = 1
    # mytime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    # newTime = datetime.datetime.now()-datetime.timedelta(days=30)
    # loginUser1['start'] = newTime.strftime("%Y-%m-%d %H:%M:%S")
    # loginUser1['end'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    # loginUser1['source'] = "402880822f47692b012f4774e5710010"
    # loginUser1['id'] = "402881795947f3d801594810601f004e"
    # loginUser1['did'] = "8a8a84825d32dc69015d349c7e2f0519"
    # loginUser1['eorc'] = getConstant.EORCID_SJ
    # loginUser1['eventtypeone'] = getConstant.SJ_SRHJ
    # loginUser1['eventtypetwo'] = getConstant.SJ_SRHJ_DLBJ
    # loginUser1['pageNo'] = 1


    # lytjArr.append(loginUser1)
    # lytjArr.append(loginUser2)
    # lytjArr.append(loginUser3)






    SourceStatistics(loginUser).test_web_laiYuanTongJiList()
    SourceStatistics(loginUser).test_searchOrExport()