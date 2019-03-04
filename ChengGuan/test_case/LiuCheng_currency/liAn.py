# -*- coding: utf-8 -*-
import requests
import json,re  
import sys
sys.path.append("E:/test/dcms/ChengGuan")
import time
from bs4 import BeautifulSoup
from config.Log import logging
from common.writeAndReadText import writeAndReadTextFile
from common.constant_all import getConstant

class setUpCase():
    
    def __init__(self,lianData):
        self.lianData = lianData
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
            
    #查询待立案列表    
    def test_toBePutOnRecordList(self):
        list_url = self.ip+"/dcms/cwsCase/Case-startlist.action?menuId=4028338158a414bd0158a4848a7f000d&keywords=402880ea2f6bd924012f6c521e8c0034"
        respons = requests.get(url = list_url,headers=self.header,allow_redirects=False)
        respons.connection.close()
        if '<span id="pagemsg"' in respons.text:
            return respons.text
        elif ('Set-Cookie' in respons.headers):
            print("对不起，请您先登录web端")
            return False
        else:
            print("XXXXXXXXXX待立案列表查询出错XXXXXXXXXX")
            return False

    #进入详情并立案
    def test_detailsAndFiling(self):
        # 获取待立案列表
        lian_res = self.test_toBePutOnRecordList()
        if lian_res != False:
            lian_count = re.compile('<label>总共(.*?)页,(.*?)条记录</label>').search(lian_res).group(2)
            if lian_count > "0":
                result = BeautifulSoup(lian_res,'html.parser')
                divObj = result.find('div', attrs={'class': 'mainContentTableContainer'})
                dcl_tr = divObj.findAll('table')[1].findAll('tr')[1]
                str_tr = str(dcl_tr)
                # 获取正则第一个匹配的对象
                orderId  = re.compile('<tr id="(.*?)"').search(str_tr).group(1)
                detail_url = self.ip+"/dcms/cwsCase/Case-startview.action?id="+orderId+"&menuId=4028338158a414bd0158a4848a7f000d"
                #进入案卷详情并返回详情结果
                dla_respons = requests.get(url=detail_url,headers=self.header,timeout = 20)
                # print("详情结果是：",dla_res)
                dla_respons.connection.close()
                dla_res = dla_respons.text
                lian_result = BeautifulSoup(dla_res,'html.parser')
                lian_menuid = re.compile('<input type="hidden" name="menuId" id="menuId" value="(.*?)"/>').search(dla_res).group(1)
                lian_eorcdictname = re.compile('<input type="hidden" name="eorc.dictname" id="eorcdictname" value="(.*?)"/>').search(dla_res).group(1)
                lian_taskcasestateid = re.compile('<input type="hidden" id="taskcasestateid" name="taskcasestateid" value="(.*?)"/>').search(dla_res).group(1)
                lian_mposb = re.compile('<input type="hidden" id="mposb" name="mposb" value="(.*?)">').search(dla_res).group(1)
                lian_gridid = re.compile('<input type="hidden" id="gridid" name="gridid" value="(.*?)">').search(dla_res).group(1)
                lian_bgadminidid = re.compile('<input type="hidden" id="bgadminidid" name="bgadminid.id" value="(.*?)">').search(dla_res).group(1)
                lian_bgcodeid = re.compile('<input type="hidden" id="bgcodeid" name="bgcode.id" value="(.*?)">').search(dla_res).group(1)
                lian_casesource = re.compile('<input type="hidden" id="casesource" name="casesource" value="(.*?)">').search(dla_res).group(1)
                lian_eorc_id = re.compile('<input type="hidden" id="eorc.id" name="eorc.id" value="(.*?)"/>').search(dla_res).group(1)
                eorcdictname = re.compile('<input type="hidden" name="eorc.dictname" id="eorcdictname" value="(.*?)"/>').search(dla_res).group(1)
                if eorcdictname == "部件":
                    lian_eventtypeoneId = re.compile('<input type="hidden"  name="eventtypeone.id" value="(.*?)"/>').search(dla_res).group(1)
                    lian_eventtypetwoId = re.compile('<input type="hidden"  name="eventtypetwo.id" value="(.*?)"/>').search(dla_res).group(1)
                    detailCaseInfo = lian_result.find('div', attrs={'class': 'detailMainContainer'}).findAll('div', attrs={'class': 'detailCaseInfo'})[0]
                    lian_textarea_fieldintro = detailCaseInfo.findAll('table')[0].findAll('tr')[3].find('td',attrs={'class':'content'})
                else:
                    lian_select_eventtypeoneId = lian_result.find('select',attrs={'id':'eventtypeone.id'})
                    lian_select_eventtypetwoId = lian_result.find('select',attrs={'id':'eventtypetwo.id'})
                    lian_eventtypeoneId = re.compile('<option selected="selected" value="(.*?)">(.*?)</option>').search(str(lian_select_eventtypeoneId)).group(1)
                    lian_eventtypetwoId = re.compile('<option selected="selected" value="(.*?)">(.*?)</option>').search(str(lian_select_eventtypetwoId)).group(1)
                    lian_textarea_fieldintro = lian_result.find('textarea', attrs={'id': 'fieldintro'})
                #立案条件
                try:
                    select_startConditionId = lian_result.find('select',attrs={'id':'startConditionId'}).findAll('option')[1]
                    startConditionId = re.compile(r'<option value="(.*?)">(.*?)[\s\S]*</option>').search(str(select_startConditionId)).group(1)
                except:
                    print("XXXXXXXXXXXXXXXXXXXXXXXXXXXX立案条件为空XXXXXXXXXXXXXXXXXXXXXXXXXXXX")
                lian_textarea_description = lian_result.find('textarea', attrs={'id': 'description'})
                lian_fieldintro = lian_textarea_fieldintro.get_text()
                lian_description = lian_textarea_description.get_text()
                lian_url = self.ip+"/dcms/cwsCase/Case-startupdate.action"
                lian_data = {
                    "menuId": lian_menuid,
                    "eorc.dictname":lian_eorcdictname,
                    "id":orderId,
                    "taskcasestateid":lian_taskcasestateid,
                    "resultprocess":self.lianData['resultprocess'],
                    "px":"",
                    "py":"",
                    "deptId":"",
                    "mposb":lian_mposb,
                    "objcode":"",
                    "gridid":lian_gridid,
                    "bgadminid.id":lian_bgadminidid,
                    "imageid":"",
                    "bgcode.id":lian_bgcodeid,
                    "casesource":lian_casesource,
                    "eorc.id":lian_eorc_id,
                    "eventtypeone.id":lian_eventtypeoneId,
                    "eventtypetwo.id":lian_eventtypetwoId,
                    "fieldintro":lian_fieldintro,
                    "description":lian_description,
                    "startConditionId": startConditionId, #立案条件
                    "operatingComments":self.lianData['operatingComments'],
                    "sentence":""
                }
                lian_result = requests.post(lian_url,lian_data,headers=self.header,timeout = 20)
                lian_result.connection.close()
                if int(lian_result.text) == 0:
                    print("立案: 立案成功，返回值是：",lian_result.text)
                    return True
                elif int(lian_result.text) == 1:
                    print("XXXXXXXXXX立案: 对不起不可以重复立案，返回值是：",lian_result.text)
                    return False
                else:
                    print("立案: 立案失败，返回值是：",lian_result.text)

                    return False
            else:
                print("列表暂无数据！！！")
        else:
            return False




# if __name__=="__main__": 
#     lianData = {}
#     lianData['resultprocess'] = '立案'
#     lianData['operatingComments'] = '批准立案'
#     setUpCase(lianData).test_detailsAndFiling()