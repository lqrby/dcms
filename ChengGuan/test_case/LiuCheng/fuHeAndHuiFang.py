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

class test_reviewAndReturnVisit():
    # WEB端案卷回访
    #查询待回访案卷列表    
    def test_returnVisitList(self):
        cookies = writeAndReadTextFile().test_readCookies()
        dhf_url = getConstant.IP_WEB_180+"/dcms/cwsCase/Case-hflist.action?casestate=55&menuId=2c94ccad37c600e30137c607846b0003&keywords=402880ea2f6bd924012f6c521e8c0034"
        header = {
            "Cookie":cookies
        }
        respons = requests.get(url = dhf_url,headers=header).text
        return respons

    #进入待回访案卷详情并回访
    def test_returnDetailsAndVisit(self):
        # 获取待回访列表
        res = self.test_returnVisitList()
        result = BeautifulSoup(res,'html.parser')
        divObj = result.find('div', attrs={'class':'mainContentTableContainer'})
        dcl_tr = divObj.findAll('table')[1].findAll('tr')[1]
        str_tr = str(dcl_tr)
        number= re.compile('<span id="pagemsg" style="(.*?)"><label>总共(.*?)页,(.*?)条记录</label></span>').search(res).group(3)
        if int(number)>0:
            dhfobj = re.compile(r'<tr[\s\S]*id="(.*?)"[\s\S]*onclick="casedo[\(](.*?),(.*?),(.*?),(.*?),this[\)]">')
            dhfid = dhfobj.search(str_tr).group(1)
            dhf_menuid = dhfobj.search(str_tr).group(2).strip("'")
            dhf_taskprocess = dhfobj.search(str_tr).group(5).strip("'")
            # 待回访详情url
            dclxq_url = getConstant.IP_WEB_180+"/dcms/cwsCase/Case-hf.action?id="+dhfid+"&menuId="+dhf_menuid+"&taskprocess="+dhf_taskprocess
            dclxq_cookies = writeAndReadTextFile().test_readCookies()
            header = {
            "Cookie":dclxq_cookies
            }
            dclxq_res = requests.get(url = dclxq_url,headers=header).text
            hflist = writeAndReadTextFile().test_read_txt('E:/test/dcms/ChengGuan/testFile/huiFang/anjuanhuifang.txt')
            hf_list = hflist.split(',')
            hf_taskcasestateid = re.compile('<input type="hidden" id="taskcasestateid" name="taskcasestateid" value="(.*?)"/>').search(dclxq_res).group(1)
            hf_casestate = re.compile('<input type="hidden" id="casestate" name="casestate" value="(.*?)" />').search(dclxq_res).group(1)
            hf_taskprocess = re.compile('<input type="hidden" id="taskprocess" name="taskprocess" value="(.*?)" />').search(dclxq_res).group(1)
            # 回访案卷url
            hf_url = getConstant.IP_WEB_180+"/dcms/cwsCase/Case-check.action"
            hf_data = {
                "taskcasestateid":hf_taskcasestateid,
                "menuId":dhf_menuid,
                "casestate":hf_casestate,
                "id":dhfid,
                "taskprocess":hf_taskprocess,
                "resultprocess":hf_list[0],
                "isFaction":"",
                "myd":"on",
                "operatingComments":hf_list[1],
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






#移动端apk案卷复核=================================================================================================
#执法局查询案卷列表    
    def test_app_zfj_returnVisitList(self):
        login_items = writeAndReadTextFile().test_read_appLoginResult()
        zfjItem = login_items['zfj']
        if zfjItem['message']== 'success':
            zfjUser = zfjItem['user']
            zfj_userId = zfjUser['id']
        dhf_url = getConstant.IP_WEB_180+"/dcms/pwasCase/Case-checkList.action"
        zfjdfh_data = {
            "page.pageSize":"20",
            "bgadminid.id":zfj_userId,
            "page.pageNo":"1"
        }
        respons = requests.post(dhf_url,zfjdfh_data).text
        return respons

    #执法局进入案卷详情并复核
    def test_app_zfj_returnDetailsAndVisit(self):
        # 获取列表
        zfjlist_res = self.test_app_zfj_returnVisitList()
        if zfjlist_res != None:
            if 'count' in zfjlist_res:
                dcl_count = re.compile('<caseCheckList count="(.*?)"').search(zfjlist_res).group(1)
                # print("执法局：列表查询成功")
                if int(dcl_count)>0:
                    login_items = writeAndReadTextFile().test_read_appLoginResult()
                    zfjItem = login_items['zfj']
                    if zfjItem['message']== 'success':
                        zfjUser = zfjItem['user']
                        zfj_userId = zfjUser['id']
                    dclId = re.compile('<id>(.*?)</id>').search(zfjlist_res).group(1)
                    zfj_cl_url = getConstant.IP_WEB_180+"/dcms/pwasCase/Case-pdacheckCase.action"
                    zfj_cl_data = {
                        "id":dclId,
                        "checkdesc":"经复核有效",
                        "casestateid.id":"402880822f3eca29012f3ed146b30006",
                        "checkid.id":zfj_userId,
                        "taskprocess":""
                    }
                    zfjcl_res = requests.post(zfj_cl_url,zfj_cl_data).text
                    if '<issuc>true</issuc>' in zfjcl_res:
                        print("执法局apk：复核完毕")
                        return True
                    else:
                        print("执法局apk：复核失败")
                        return False 
                else:
                    print("执法局:列表暂时为空")
                    return False
            elif 'errorCode' in zfjlist_res and zfjlist_res['errorCode']=='2':
                print("**********对不起请您先登录执法局apk**********")
                return False
        else:
            print("XXXXXXXXXX执法局：复核列表出错XXXXXXXXXX")
            return False

    # ==================================================================================================
    #网格管理员apk查询案卷列表    
    def test_app_wggly_returnVisitList(self):
        login_items_val = writeAndReadTextFile().test_read_appLoginResult()
        wgglyItem = login_items_val['wggly']
        if wgglyItem['message']== 'success':
            wgglyUser = wgglyItem['user']
            wggly_userId = wgglyUser['id']
        dhf_url = getConstant.IP_WEB_180+"/dcms/pwasCase/Case-checkList.action"
        wgglydfh_data = {
            "page.pageSize":"20",
            "bgadminid.id":wggly_userId,
            "page.pageNo":"1"
        }
        wgglyrespons = requests.post(dhf_url,wgglydfh_data).text
        if 'count' in wgglyrespons:
            # print("(网格管理员apk)：案卷列表查询成功")
            return wgglyrespons
        elif 'errorCode' in wgglyrespons and wgglyrespons['errorCode']=='2':
            print("************对不起请您先登录网格管理员apk*************")
            return False
        else:
            print("XXXXXXXXXX(网格管理员apk):意想不到的错误XXXXXXXXXX")
            return False

    #网格管理员进入案卷详情并复核
    def test_app_wggly_returnDetailsAndVisit(self):
        # 获取列表
        wgglylist_res = self.test_app_wggly_returnVisitList()
        if wgglylist_res != False:
            dcl_count = re.search('<caseCheckList count="(.*?)">',wgglylist_res).group(1)
            if int(dcl_count)>0:
                login_items = writeAndReadTextFile().test_read_appLoginResult()
                wgglyItem = login_items['wggly']
                if wgglyItem['message']== 'success':
                    wgglyUser = wgglyItem['user']
                    wggly_userId = wgglyUser['id']
                wgglydclId = re.compile('<id>(.*?)</id>').search(wgglylist_res).group(1)
                wggly_cl_url = getConstant.IP_WEB_180+"/dcms/pwasCase/Case-pdacheckCase.action"
                wggly_cl_data = {
                    "id":wgglydclId,
                    "checkdesc":"经复核有效",
                    "casestateid.id":"402880822f3eca29012f3ed146b30006",
                    "checkid.id":wggly_userId,
                    "taskprocess":""
                }
                wgglycl_res = requests.post(wggly_cl_url,wggly_cl_data).text
                if '<issuc>true</issuc>' in wgglycl_res:
                    print("复核(网格管理员apk)：复核完毕")
                    return True
                else:
                    print("复核(网格管理员apk)：复核失败")
                    return False
            else:
                print("(网格管理员apk):待处理列表暂时为空")
                return False
        
        else:
            return False


# if __name__=="__main__": 
#     test_reviewAndReturnVisit().test_app_zfj_returnDetailsAndVisit()