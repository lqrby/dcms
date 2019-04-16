# -*- coding: utf-8 -*-

import requests
import json 
import sys,re
sys.path.append("E:/test/dcms/ChengGuan")
import time
from bs4 import BeautifulSoup
from config.Log import logging
from common.writeAndReadText import writeAndReadTextFile
from common.constant_all import getConstant
from requests_toolbelt import MultipartEncoder
from common.appReportPicture import test_app_ReportPicture

class verify():
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
    # 网格员进入待核实列表
    def test_app_heShiList(self):
        dhsItem = {}
        dhsurl = self.ip+"/dcms/pwasCase/Case-confirmList.action"
        dhs_data = {
            "page.pageSize":"20",
            "bgadminid.id":self.loginUser['id'],
            "page.pageNo":"1"
        }
        dhsListRes = requests.get(dhsurl,dhs_data,headers = self.app_header,allow_redirects=False,timeout = 20)
        dhsListRsult = dhsListRes.text
        dhsListRes.connection.close()
        if 'count' in dhsListRsult:
            count = re.compile('<caseCheckList count="(.*?)"').search(dhsListRsult).group(1)
            if count > '0':
                dhsList_soup = BeautifulSoup(dhsListRsult,'lxml')
                for casecheckrecord in dhsList_soup.findAll('casecheckrecord'):
                    caseid = casecheckrecord.find('caseid').get_text()
                    if caseid == self.loginUser['oderId']:
                        dhsItem = casecheckrecord
                        break
                return dhsItem
            else:
                print("待核实列表暂时为空！！！")
                return count
        elif 'Location' in dhsListRes.headers and '/dcms/bms/login' in dhsListRes.headers['Location']:
            print("对不起，请您先登录")
        else:
            print("XXXXXXXXXXXXXXXX待确认列表出错XXXXXXXXXXXXXXX")
            
            
        # else:
        #     print("待核实列表查询失败")
    # 网格员核实(有效/无效)
    def test_app_daiHeShiDetail(self):
        dhsResult = self.test_app_heShiList()
        if dhsResult:
            hs_url = self.ip+"/dcms/pwasCase/Case-pdaconfirmCase.action"
            hs_data = {
                "eorc.id":dhsResult.find('eorc').get_text(),
                "fieldintro":dhsResult.find('fieldintro').get_text(),
                "confirmid.id":self.loginUser['id'],#核实人id
                "mposl":dhsResult.find('mposl').get_text(),
                "description":dhsResult.find('description').get_text(),
                "id":dhsResult.find('id').get_text(),
                "eventtypeone.id":dhsResult.find('eventtypeone').get_text(),
                "casestateid.id":self.loginUser['casestateid'],#核实有效/核实无效
                "gridid":dhsResult.find('gridid').get_text(),
                "eventtypetwo.id":dhsResult.find('eventtypetwo').get_text(),
                "mposb":dhsResult.find('mposb').get_text()
            }
            hs_result = requests.post(hs_url,hs_data,headers = self.app_header,timeout = 20)
            hs_result.connection.close()
            if '<caseprochisid>' in hs_result.text:
                print("案卷核实成功")
                result_data= re.compile('<caseInputInfo><issuc>(.*?)</issuc><caseprochisid>(.*?)</caseprochisid><idcase>(.*?)</idcase></caseInputInfo>').search(hs_result.text)
                caseprochisid = result_data.group(2)
                idcase = result_data.group(3)
                if 'imgPath' in self.loginUser:
                    # 上传图片地址
                    imgUrl = self.ip+"/dcms/PwasAdmin/PwasAdmin-imageup.action?imagetype=image&idcase="+idcase+"&prochisid="+caseprochisid
                    picpath = self.loginUser['imgPath']
                    test_app_ReportPicture(imgUrl,picpath)
                    return True
                else:
                    print("核实案卷未上传图片")
            else:
                print("XXXXXXXXXXXXXXXXXXXXXXXXXXXX核实失败XXXXXXXXXXXXXXXXXXXXXXXXXXX")
    
        else:
            print("待核实列表中没有该工单号:{}".format(self.loginUser['oderNumber']))
            return dhsResult
                

# if __name__=="__main__": 
#     #test_app_wggly_daiHeShiDetail()
#     test_app_zfj_daiHeShiDetail()