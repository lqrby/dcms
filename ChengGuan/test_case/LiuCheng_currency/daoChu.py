# -*- coding: utf-8 -*-

import requests
import json,random 
import sys,re
sys.path.append("E:/test/dcms/ChengGuan")
import time
from bs4 import BeautifulSoup
from config.Log import logging
from common.writeAndReadText import writeAndReadTextFile
from common.constant_all import getConstant
from requests_toolbelt import MultipartEncoder
from common.appReportPicture import test_app_ReportPicture

class colligateQuery():
    def __init__(self,loginUser):
        self.loginUser = loginUser
        if '180' in getConstant.IP:
            self.ip = getConstant.IP+getConstant.PORT_7897
        else:
            self.ip = getConstant.IP
        self.header = {
            "User-Agent": "Android/8.0.0",
            "Content-Type":"application/x-www-form-urlencoded",
            "Connection":"Keep-Alive",
            "Accept-Encoding":"gzip"
        }
    # 综合查询列表列表（默认查询当天的案卷）
    def test_web_zongHeList(self):
        zhcxurl = self.ip+"/dcms/bmsUniversal/UniversalCaseQuery-list.action?menuId=4028838358b7f73b0158b9e7f3480c59&keywords=402880ea2f6bd924012f6c521e8c0034"
        zhcx_res = requests.get(zhcxurl,headers = self.header, allow_redirects=False ,timeout = 20)
        # zhcx_res.connection.close()
        if zhcx_res.status_code == 200:
            print("***************综合查询列表成功***************")
            return zhcx_res.text
        elif zhcx_res.status_code == 302:
            print("XXXXXXXXXXXXXXXXXXX您还未登录XXXXXXXXXXXXXXXXXXX")
            return False
        else:
            print("XXXXXXXXXXXXXXXXX综合查询列表出错XXXXXXXXXXXXXXXXXX")
            return False
        
    
    #查看综合查询案卷详情
    def test_web_zongHeDetail(self):
        zonghe_res = self.test_web_zongHeList()
        if zonghe_res:
            zhcx_count = re.compile('<label>总共(.*?)页,(.*?)条记录</label>').search(zonghe_res).group(2)
            if zhcx_count > "0":
                zhcx_list = re.compile('<tr  id="(.*?)"').findall(zonghe_res)
                if len(zhcx_list) > 5:
                    zhcx_list = random.sample(zhcx_list, 5)  #从list中随机获取5个元素，作为一个片断返回  
                for itemId in zhcx_list:
                    #查看详情
                    detail_url = self.ip+"/dcms/cwsCase/Case-caseinfo.action?id={}&menuId=4028838358b7f73b0158b9e7f3480c59".format(itemId)
                    detailres = requests.get(detail_url,headers = self.header, allow_redirects=False,timeout = 20)
                    if detailres.status_code == 200 and '案卷编号' in detailres.text and '办理操作' in detailres.text:
                        print("综合查询》查看案卷详情成功，",detailres.status_code)
                    else:
                        print("综合查询》查看案卷详情失败，",detailres.status_code)

                    #查看
                    # detailres.connection.close()
                    time.sleep(random.randint(2.3))
            else:
                print("综合查询列表暂无数据！！！")

                
                

if __name__=="__main__": 
    loginUser = {}
    colligateQuery(loginUser).test_web_zongHeDetail()