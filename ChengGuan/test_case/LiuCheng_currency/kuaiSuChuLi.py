# -*- coding: utf-8 -*-

import requests
import json
import re
import ast
import sys,random
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
            "User-Agent": "Android/8.0.0",
            "Content-Type":"application/x-www-form-urlencoded",
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
    #快速上报案卷    
    def test_quickReport(self):
        kssb_url = self.ip+'/dcms/PwasAdmin/CaseLaw-saveCase.action'
        kssb_data = {
            "describe":loginUser['describe'],
            "adminid.id":loginUser['id'],
            "field":""
        }
        kssb_res = requests.post(kssb_url,kssb_data,headers = self.app_header,timeout = 20)
        if 'success' in kssb_res.text:
            print("************快速上报案卷成功*************")
            return kssb_res.text
        else:
            print("XXXXXXXXXXXXXXXXXXXXXXXXXXXXX快速上报案卷失败XXXXXXXXXXXXXXXXXXXXXXXXXXXX")
            return False

    #快速处理列表
    def test_quickProcessingList(self):
        dclList_url = self.ip+'/dcms/PwasAdmin/CaseLaw-searchCase.action'
        dclList_data={
            "page.pageSize":"20",
            "startTime":loginUser['startTimes'],
            "endTime":loginUser['endTime'],
            "userid":loginUser['id'],
            "page.pageNo":"1"
        }
        dclList_res = requests.post(dclList_url,dclList_data,headers = self.app_header,timeout = 20)
        if 'success' in dclList_res.text:
            return dclList_res.text
        else:
            print("**************获取快速处理列表出错***********")
            return False

    #处理快速案卷
    def test_fastProcessing(self):
        dcl_list =  self.test_quickProcessingList()
        if dcl_list != False:
            dclList = json.loads(dcl_list)
            if dclList['count'] > 0:
                caseid = dclList['data'][0]['id']
                bgadminid = dclList['data'][0]['adminname']
                description = dclList['data'][0]['describe']
                ksclurl = self.ip+"/dcms/pwasCase/pwasCase-dealCase.action"
                kscldata = {
                    "eorc.id":loginUser['eorc'],
                    "fieldintro":loginUser['fieldintro'],
                    "deptId":"", 
                    "mposl":loginUser['mposl'],                               
                    "description":description,   
                    "objcode":"", 
                    "eventtypeone.id":loginUser['eventtypeone'],                
                    "gridid":loginUser['gridid'],
                    "bgadminid.id":bgadminid,
                    "eventtypetwo.id":loginUser['eventtypetwo'],               
                    "caseid":caseid,
                    "mposb":loginUser['mposb'],                             
                }
                ksclRespons = requests.post(ksclurl,kscldata,headers = self.app_header,timeout = 20)
                ksclres = ksclRespons.text
                if 'true' in ksclres:
                    if 'imgPath' in self.loginUser:
                        print("正在上传处理图片...")
                        # 上传图片地址
                        ksclRes = json.loads(ksclres)
                        print(ksclRes)
                        imgUrl = self.ip+"/dcms/PwasAdmin/PwasAdmin-imageup.action?imagetype=image&idcase="+ksclRes['data']['caseid']+"&prochisid="+ksclRes['data']['taskId']
                        picpath = self.loginUser['imgPath']
                        test_app_ReportPicture(imgUrl,picpath)
                    else:
                        print("快速案卷处理时未上传图片")
                    return True
                else:
                    print("XXXXXXXXXXXXXXXXXXX快速处理案卷失败XXXXXXXXXXXXXXXXXXX")
                    return False
            else:
                print("00000000000000待处理快速案卷列表暂时为空0000000000000")
                return False
        


if __name__=="__main__": 
    # 快速处理案卷
    time.sleep(random.randint(2,4))
    markPath = getConstant.PROJECT_PATH+"/common/numberMark.txt"
    mark = writeAndReadTextFile().test_read_txt(markPath)
    dict_mark = json.loads(mark)
    number = int(dict_mark['zfj_sb'])+1
    loginitems = writeAndReadTextFile().test_read_appLoginResult()
    loginUser = loginitems['zfj']['user']
    
    millis = int(round(time.time() * 1000))
    loginUser['startTimes'] = millis-24*60*60*1000
    loginUser['endTime'] = millis
    loginUser['describe'] = '快速上报案卷'+str(number)
    loginUser['eorc'] = getConstant.EORCID_SJ
    loginUser['fieldintro'] = '吉林市 高新开发区 高新开发区街道 长江社区 长江社区第八网格'
    loginUser['mposl'] = '14089442.42203088'
    loginUser['eventtypeone'] = getConstant.SJ_SRHJ
    loginUser['eventtypetwo'] = getConstant.SJ_SRHJ_DLBJ
    loginUser['mposb'] = '5436678.363948615'
    loginUser['gridid'] = '22020600100408'
    cl_picpath1 = "E:/test/dcms/ChengGuan/testFile/img/22.png"
    cl_picpath2 = "E:/test/dcms/ChengGuan/testFile/img/23.png"
    loginUser['imgPath'] = [cl_picpath1,cl_picpath2]
    kssb_res = fileFandling(loginUser).test_quickReport()
    
    if kssb_res:
        print("ok")
        dict_mark["zfj_sb"] = str(number)
        writeAndReadTextFile().test_write_txt(markPath,json.dumps(dict_mark))
        kscl_res = fileFandling(loginUser).test_fastProcessing()  
        if kscl_res:
            print("**********快速处理案卷成功*********")
        else:
            print("xxxxxxxxxxxxxxxx快速处理案卷失败xxxxxxxxxxxxxxxxxxx")
    else:
        print("xxxxxxxxxxxxxxxxxxxxxxxx快速案卷上报失败xxxxxxxxxxxxxxxxxxxxxxxxxxx")     