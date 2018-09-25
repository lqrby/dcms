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

class verify():
    def __init__(self,loginUser):
        self.loginUser = loginUser
    # 网格管理员进入待核实列表
    def test_app_heShiList(self):
        dhsurl = getConstant.IP_WEB_91+"/dcms/pwasCase/Case-confirmList.action"
        # results = writeAndReadTextFile().test_read_appLoginResult()
        # wgglyUser = results['wggly']['user']
        dhs_data = {
            "page.pageSize":"20",
            "bgadminid.id":self.loginUser['id'],
            "page.pageNo":"1"
        }
        dqr_res = requests.get(dhsurl,dhs_data,allow_redirects=False).text
        if 'count' in dqr_res:
            # print("待核实列表查询成功")
            return dqr_res
        else:
            print("待核实列表查询失败")
    # 网格员核实
    def test_app_daiHeShiDetail(self):
        dhsResult = self.test_app_heShiList()
        if dhsResult != None:
            count = re.compile('<caseCheckList count="(.*?)">').search(dhsResult).group(1)
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
                
                hs_url = getConstant.IP_WEB_91+"/dcms/pwasCase/Case-pdaconfirmCase.action"
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
                    "casestateid.id":"402880822f3eca29012f3ed0218c0002",#核实有效:402880822f3eca29012f3ed0218c0002   核实无效:402880822f3eca29012f3ecf72020001
                    "gridid":dhs_gridid,
                    "eventtypetwo.id":dhs_eventtypetwo,
                    "mposb":dhs_mposb
                }
                hs_result = requests.post(hs_url,hs_data).text
                if '<issuc>true</issuc>' in hs_result:
                    print("核实完毕")
                    return True
                else:
                    print("核实失败")
                    return False
                

# if __name__=="__main__": 
#     #test_app_wggly_daiHeShiDetail()
#     test_app_zfj_daiHeShiDetail()