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

class reviewAndReturnVisit():
    def __init__(self,hfItem):
        self.hfItem = hfItem
    # WEB端案卷回访
    #查询待回访案卷列表    
    def test_returnVisitList(self):
        cookies = writeAndReadTextFile().test_readCookies()
        dhf_url = getConstant.IP_WEB_91+"/dcms/cwsCase/Case-hflist.action?casestate=55&menuId=2c94ccad37c600e30137c607846b0003&keywords=402880ea2f6bd924012f6c521e8c0034"
        header = {
            "Cookie":cookies
        }
        respons = requests.get(url = dhf_url,headers=header).text
        return respons

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
            dclxq_url = getConstant.IP_WEB_91+"/dcms/cwsCase/Case-hf.action?id="+dhfid+"&menuId="+dhf_menuid+"&taskprocess="+dhf_taskprocess
            dclxq_cookies = writeAndReadTextFile().test_readCookies()
            header = {
            "Cookie":dclxq_cookies
            }
            dclxq_res = requests.get(url = dclxq_url,headers=header).text
            # hflist = writeAndReadTextFile().test_read_txt('E:/test/dcms/ChengGuan/testFile/huiFang/anjuanhuifang.txt')
            # hf_list = hflist.split(',')
            hf_taskcasestateid = re.compile('<input type="hidden" id="taskcasestateid" name="taskcasestateid" value="(.*?)"/>').search(dclxq_res).group(1)
            hf_casestate = re.compile('<input type="hidden" id="casestate" name="casestate" value="(.*?)" />').search(dclxq_res).group(1)
            hf_taskprocess = re.compile('<input type="hidden" id="taskprocess" name="taskprocess" value="(.*?)" />').search(dclxq_res).group(1)
            # 回访案卷url
            hf_url = getConstant.IP_WEB_91+"/dcms/cwsCase/Case-check.action"
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
            hf_header = {
                "Cookie":dclxq_cookies
            }
            hf_result = requests.post(hf_url,hf_data,headers = hf_header).text
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
        dhf_url = getConstant.IP_WEB_91+"/dcms/pwasCase/Case-checkList.action"
        wgglydfh_data = {
            "page.pageSize":"20",
            "bgadminid.id":self.hfItem['id'],
            "page.pageNo":"1"
        }
        wgglyrespons = requests.post(dhf_url,wgglydfh_data).text
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
                cl_url = getConstant.IP_WEB_91+"/dcms/pwasCase/Case-pdacheckCase.action"
                cl_data = {
                    "id":wgglydclId,
                    "checkdesc":self.hfItem['checkdesc'],
                    "casestateid.id":"402880822f3eca29012f3ed146b30006", #状态
                    "checkid.id":self.hfItem['id'],
                    "taskprocess":""
                }
                cl_res = requests.post(cl_url,cl_data).text
                if '<issuc>true</issuc>' in cl_res:
                    print("复核：复核完毕")
                    return True
                else:
                    print("复核：复核失败")
                    return False
            else:
                print("待处理列表暂时为空")
                return False
        
        else:
            return False


# if __name__=="__main__": 
#     test_reviewAndReturnVisit().test_returnDetailsAndVisit()