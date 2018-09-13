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

    #查询待立案列表    
    def test_toBePutOnRecordList(self):
        cookies = writeAndReadTextFile().test_readCookies()
        list_url = getConstant.IP_WEB_91+"/dcms/cwsCase/Case-startlist.action?menuId=4028338158a414bd0158a4848a7f000d&keywords=402880ea2f6bd924012f6c521e8c0034"
        header = {
            "Cookie":cookies
        }
        respons = requests.get(url = list_url,headers=header,allow_redirects=False)
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
            if lian_count>"0":
                result = BeautifulSoup(lian_res,'html.parser')
                divObj = result.find('div', attrs={'class': 'mainContentTableContainer'})
                dcl_tr = divObj.findAll('table')[1].findAll('tr')[1]
                str_tr = str(dcl_tr)
                # 获取正则第一个匹配的对象
                orderId  = re.compile('<tr id="(.*?)"').search(str_tr).group(1)
                detail_url = getConstant.IP_WEB_91+"/dcms/cwsCase/Case-startview.action?id="+orderId+"&menuId=4028338158a414bd0158a4848a7f000d"
                cookie = writeAndReadTextFile().test_readCookies()
                header = { "Cookie" : cookie }
                #进入案卷详情并返回详情结果
                dla_res = requests.get(url=detail_url,headers=header).text
                # print("详情结果是：",dla_res)
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
                lian_textarea_description = lian_result.find('textarea', attrs={'id': 'description'})
                lian_fieldintro = lian_textarea_fieldintro.get_text()
                lian_description = lian_textarea_description.get_text()
                lian_url = getConstant.IP_WEB_91+"/dcms/cwsCase/Case-startupdate.action"
                # str_data = writeAndReadTextFile().test_read_txt("E:/test/dcms/ChengGuan/testFile/liAn/lian.txt")
                # li_list = str_data.split(',')
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
                    "startConditionId": self.lianData['startConditionId'],
                    "operatingComments":self.lianData['operatingComments'],
                    "sentence":""
                }
                lian_result = requests.post(lian_url,lian_data,headers=header).text
                if int(lian_result) == 0:
                    print("立案: 立案成功，返回值是：",lian_result)
                    return True
                elif int(lian_result) == 1:
                    print("XXXXXXXXXX立案: 对不起不可以重复立案，返回值是：",lian_result)
                    return False
                else:
                    print("立案: 立案失败，返回值是：",lian_result)

                    return False
            else:
                print("列表暂无数据！！！")
        else:
            return False




if __name__=="__main__": 
    lianData = {}
    lianData['resultprocess'] = '立案'
    lianData['startConditionId'] = '402881795961e05b01596212f3fb0068'
    lianData['operatingComments'] = '批准立案'
    setUpCase(lianData).test_detailsAndFiling()