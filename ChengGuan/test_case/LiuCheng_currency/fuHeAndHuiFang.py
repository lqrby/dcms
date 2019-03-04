# -*- coding: utf-8 -*-
import requests
import json,re  
import sys
sys.path.append("E:/test/dcms/ChengGuan")
import time
from bs4 import BeautifulSoup
from config.Log import logging
from common.constant_all import getConstant
from common.writeAndReadText import writeAndReadTextFile
from common.appReportPicture import test_app_ReportPicture

class reviewAndReturnVisit():
    def __init__(self,hfItem):
        self.hfItem = hfItem
        if '180' in getConstant.IP:
            self.ip = getConstant.IP+getConstant.PORT_7897
        else:
            self.ip = getConstant.IP
        self.app_header = {
            "User-Agent": "Android/8.0",
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
    # WEB端案卷回访
    #查询待回访案卷列表    
    def test_returnVisitList(self):
        dhf_url = self.ip+"/dcms/cwsCase/Case-hflist.action?casestate=55&menuId=2c94ccad37c600e30137c607846b0003&keywords=402880ea2f6bd924012f6c521e8c0034"
        respons = requests.get(url = dhf_url,headers=self.header,timeout=20)
        respons.connection.close()
        return respons.text

    #进入待回访案卷详情并回访
    def test_returnDetailsAndVisit(self):
        # 获取待回访列表
        res = self.test_returnVisitList()
        number= re.compile('<span id="pagemsg" style="(.*?)"><label>总共(.*?)页,(.*?)条记录</label></span>').search(res).group(3)
        if int(number)>0:
            result = BeautifulSoup(res,'html.parser')
            divObj = result.find('div', attrs={'class':'mainContentTableContainer'})
            obj_tr = divObj.findAll('table')[1].findAll('tr')[1]
            dhfobj = re.compile(r'<tr[\s\S]*id="(.*?)"[\s\S]*onclick="casedo[\(](.*?),(.*?),(.*?),(.*?),this[\)]">')
            dhfid = dhfobj.search(str(obj_tr)).group(1)
            dhf_menuid = dhfobj.search(str(obj_tr)).group(2).strip("'")
            dhf_taskprocess = dhfobj.search(str(obj_tr)).group(5).strip("'")
            # 待回访详情url
            dclxq_url = self.ip+"/dcms/cwsCase/Case-hf.action?id="+dhfid+"&menuId="+dhf_menuid+"&taskprocess="+dhf_taskprocess
            dclxqrespons = requests.get(url = dclxq_url,headers=self.header,timeout = 20)
            dclxq_res = dclxqrespons.text
            dclxqrespons.connection.close()
            hf_taskcasestateid = re.compile('<input type="hidden" id="taskcasestateid" name="taskcasestateid" value="(.*?)"/>').search(dclxq_res).group(1)
            hf_casestate = re.compile('<input type="hidden" id="casestate" name="casestate" value="(.*?)" />').search(dclxq_res).group(1)
            hf_taskprocess = re.compile('<input type="hidden" id="taskprocess" name="taskprocess" value="(.*?)" />').search(dclxq_res).group(1)
            # 回访案卷url
            hf_url = self.ip+"/dcms/cwsCase/Case-check.action"
            hf_data = {
                "taskcasestateid":hf_taskcasestateid,
                "menuId":dhf_menuid,
                "casestate":hf_casestate,
                "id":dhfid,
                "taskprocess":hf_taskprocess,
                "resultprocess":self.hfItem['resultprocess'],
                "isFaction":"",
                "myd":"on",
                "operatingComments":self.hfItem['operatingComments'],
                "sentence":""
            }
            
            hfresult = requests.post(hf_url,hf_data,headers = self.header,timeout = 20)
            hf_result = hfresult.text
            hfresult.connection.close()
            if hf_result==0:
                print("回访：回访完成",hf_result)
                return True
            elif hf_result==1:
                print("回访：重复回访",hf_result)
                return False
            return hf_result
        else:
            print("待回访列表暂无数据！！！")
            return False

    # ==================================================================================================
    #网格员apk查询案卷列表    
    def test_app_returnVisitList(self):
        dhf_url = self.ip+"/dcms/pwasCase/Case-checkList.action"
        wgglydfh_data = {
            "page.pageSize":"20",
            "bgadminid.id":self.hfItem['id'],
            "page.pageNo":"1"
        }
        wggly_respons = requests.post(dhf_url,wgglydfh_data,headers = self.app_header,timeout = 20)
        wgglyrespons = wggly_respons.text
        wggly_respons.connection.close()
        if 'count' in wgglyrespons:
            # print("案卷列表查询成功")
            return wgglyrespons
        elif 'errorCode' in wgglyrespons and wgglyrespons['errorCode']=='2':
            print("************对不起请您先登录网格管理员apk*************")
            return False
        else:
            print("XXXXXXXXXX意想不到的错误XXXXXXXXXX")
            return False

    #进入案卷详情并复核
    def test_app_returnDetailsAndVisit(self):
        # 获取列表
        dfh_list = self.test_app_returnVisitList()
        if dfh_list != False:
            dcl_count = re.compile('<caseCheckList count="(.*?)"').search(dfh_list).group(1)
            if int(dcl_count)>0:
                wgglydclId = re.compile('<id>(.*?)</id>').search(dfh_list).group(1)
                cl_url = self.ip+"/dcms/pwasCase/Case-pdacheckCase.action"
                cl_data = {
                    "id":wgglydclId,
                    "checkdesc":self.hfItem['checkdesc'],
                    "casestateid.id":"402880822f3eca29012f3ed146b30006", #状态
                    "checkid.id":self.hfItem['id'],
                    "taskprocess":""
                }
                clres = requests.post(cl_url,cl_data,headers = self.app_header,timeout = 20)
                cl_res = clres.text
                result_data= re.compile('<caseInputInfo><issuc>(.*?)</issuc><caseprochisid>(.*?)</caseprochisid><idcase>(.*?)</idcase></caseInputInfo>').search(cl_res)
                issuc = result_data.group(1)
                caseprochisid = result_data.group(2)
                idcase = result_data.group(3)
                if issuc:
                    # print("案卷复核成功")
                    if 'imgPath' in self.hfItem:
                        # 上传图片地址
                        imgUrl = self.ip+"/dcms/PwasAdmin/PwasAdmin-imageup.action?imagetype=image&idcase="+idcase+"&prochisid="+caseprochisid
                        picpath = self.hfItem['imgPath']
                        test_app_ReportPicture(imgUrl,picpath)
                    else:
                        print("复核案卷未上传图片")
                    return True
                else:
                    print("XXXXXXXXXX上报失败XXXXXXXXXX")
                    return False
                clres.connection.close()
            else:
                print("待复核列表暂时为空")
                return False
        
        else:
            return False


# if __name__=="__main__": 
#     test_reviewAndReturnVisit().test_returnDetailsAndVisit()