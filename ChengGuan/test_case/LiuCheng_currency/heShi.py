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
        dhsurl = self.ip+"/dcms/pwasCase/Case-confirmList.action"
        # results = writeAndReadTextFile().test_read_appLoginResult()
        # wgglyUser = results['wggly']['user']
        dhs_data = {
            "page.pageSize":"20",
            "bgadminid.id":self.loginUser['id'],
            "page.pageNo":"1"
        }
        dqr_res = requests.get(dhsurl,dhs_data,headers = self.app_header,allow_redirects=False,timeout = 20)
        dprres = dqr_res.text
        dqr_res.connection.close()
        print(dprres,"22222222222222222222")
        if 'count' in dprres:
            return dprres
        else:
            print("待核实列表查询失败")
    # 网格员核实(有效/无效)
    def test_app_daiHeShiDetail(self):
        dhsResult = self.test_app_heShiList()
        if dhsResult:
            count = re.compile('<caseCheckList count="(.*?)"').search(dhsResult).group(1)
            if count>'0':
                dhs_id = re.compile('<id>(.*?)</id>').search(dhsResult).group(1)
                dhs_description = re.compile('<description>(.*?)</description>').search(dhsResult).group(1)
                dhs_eorc = re.compile('<eorc>(.*?)</eorc>').search(dhsResult).group(1)
                dhs_eventtypeone = re.compile('<eventtypeone>(.*?)</eventtypeone>').search(dhsResult).group(1)
                dhs_eventtypetwo = re.compile('<eventtypetwo>(.*?)</eventtypetwo>').search(dhsResult).group(1)
                dhs_fieldintro = re.compile('<fieldintro>(.*?)</fieldintro>').search(dhsResult).group(1)
                dhs_gridid = re.compile('<gridid>(.*?)</gridid>').search(dhsResult).group(1)
                dhs_mposl = re.compile('<mposl>(.*?)</mposl>').search(dhsResult).group(1)
                dhs_mposb = re.compile('<mposb>(.*?)</mposb>').search(dhsResult).group(1)
                hs_url = self.ip+"/dcms/pwasCase/Case-pdaconfirmCase.action"
                # results = writeAndReadTextFile().test_read_appLoginResult()
                # wgglyUser = results['wggly']['user']
                hs_data = {
                    "eorc.id":dhs_eorc,
                    "fieldintro":dhs_fieldintro,
                    "confirmid.id":self.loginUser['id'],#核实人id
                    "mposl":dhs_mposl,
                    "description":dhs_description,
                    "id":dhs_id,
                    "eventtypeone.id":dhs_eventtypeone,
                    "casestateid.id":self.loginUser['casestateid'],#核实有效/核实无效
                    "gridid":dhs_gridid,
                    "eventtypetwo.id":dhs_eventtypetwo,
                    "mposb":dhs_mposb
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
                    else:
                        print("核实案卷未上传图片")
                    return True
                else:
                    print("XXXXXXXXXXXXXXXXXXXXXXXXXXXX核实失败XXXXXXXXXXXXXXXXXXXXXXXXXXX")
                    return False
            else:
                print("待核实列表暂时为空")
    
    
                
                

# if __name__=="__main__": 
#     #test_app_wggly_daiHeShiDetail()
#     test_app_zfj_daiHeShiDetail()