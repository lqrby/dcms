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


class hangUp():

    def __init__(self,loginUser):
        self.loginUser = loginUser
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
           
            
    #web查询挂起案卷列表    
    def test_hangUpList(self):
        gzlist_url = self.ip+"/dcms/cwsCase/Case-losseslist.action?casestate=21&menuId=2c94d09f3087787d013087ea6943007b&keywords=402880eb2f90e905012f9138a5fb00a4"
        gzrespons = requests.get(url = gzlist_url,headers=self.header,timeout = 20)
        gz_respons = gzrespons.text
        gzrespons.connection.close()
        if '<title>挂账事件列表</title>' in gz_respons:
            return gz_respons
        else:
            print("XXXXXXXXXXXXXXXXXXXXXXX查询挂起列表出错XXXXXXXXXXXXXXXXXXXXXXX")
            return False

    #web进入挂起案卷详情并处理
    def test_hangUpDetail(self):
        gq_list = self.test_hangUpList() # 获取挂起列表
        if gq_list != False:
            gq_num = re.compile('<label>总共(.*?)页,(.*?)条记录</label>').search(gq_list).group(2)
            if gq_num > "0":
                gq_result = BeautifulSoup(gq_list,'html.parser')
                gqdiv = gq_result.find('div', attrs={'class':'mainContentTableContainer'})
                gq_tr = gqdiv.findAll('table')[1].findAll('tr')[1]
                pattern = re.compile(r'<tr[\s\S]*id="(.*?)"[\s\S]*onclick="casedo[\(](.*?),(.*?),(.*?),(.*?),this[\)]">').search(str(gq_tr))
                gqid = pattern.group(1)
                gq_menuid = pattern.group(2).strip("'")
                gq_taskprocess = pattern.group(5).strip("'")
                gqdetail_url = self.ip+'/dcms/cwsCase/Case-lossesview.action?id='+gqid+'&menuId='+gq_menuid+'&taskprocess='+gq_taskprocess
                gqres = requests.get(gqdetail_url,headers = self.header,timeout = 20)
                gq_res = gqres.text
                gqres.connection.close()
                if '<title>挂账案卷</title>' in gq_res:
                    taskcasestateid = re.compile('<input type="hidden" id="taskcasestateid" name="taskcasestateid" value="(.*?)"/>').search(gq_res).group(1)
                    if 'resultprocess' in self.loginUser:
                        resultprocess = self.loginUser['resultprocess']
                    else:
                        resultprocess = ""

                    if 'operatingComments' in self.loginUser:
                        operatingComments = self.loginUser['operatingComments']
                    else:
                        operatingComments = ""
                    gqdata = {
                        "taskcasestateid": taskcasestateid,
                        "menuId": gq_menuid,
                        "casestate": "",
                        "id": gqid,
                        "taskprocess": gq_taskprocess,
                        "resultprocess": resultprocess,
                        "operatingComments": operatingComments,
                        "sentence": ""
                    }
                    hf_url = self.ip+'/dcms/cwsCase/Case-losses.action'
                    hfres = requests.post(hf_url,gqdata,headers = self.header,allow_redirects=False,timeout = 20)
                    hfres.connection.close()
                    if 'location' in hfres.headers and '/Case-losseslist.action' in hfres.headers['location']:
                        print("************************恢复案卷成功************************")
                        return True
                    elif 'location' in hfres.headers and '/dcms/bms/login' in hfres.headers['location']:
                        print("XXXXXXXXXXXXXXXXXXXXXXXXXXXXX对不起，请您先登录XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX")
                        return False
                else:
                    print("XXXXXXXXXXXXXXXXXXXXXX进入挂账案卷详情出错XXXXXXXXXXXXXXXXXXXXXX")
                    return False
            else:
                print("00000000000000挂起列表暂时为空000000000000000")
                return False
        else:
            return False

        