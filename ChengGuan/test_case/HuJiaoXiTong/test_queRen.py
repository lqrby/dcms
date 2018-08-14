# -*- coding: utf-8 -*-

import requests
from selenium import webdriver
import json,ast 
import unittest
import urllib, sys, io,re
sys.path.append("E:/test/dcms/ChengGuan")
import time
# import config
from bs4 import BeautifulSoup
from config.Log import logging
sys.stdout = io.TextIOWrapper(sys.stdout.buffer,encoding='utf-8')
from test_2web_chengguan_login import test_cg_login
from common.writeAndReadText import writeAndReadTextFile
from common.constant_all import getConstant
from requests_toolbelt import MultipartEncoder

# 进入待确认列表页面
def test_web_UnconfirmedList():
    hjxt_id = writeAndReadTextFile().test_read_systemId('呼叫系统')
    dqr_url = getConstant.IP+"/dcms/bmsAdmin/PlCaseUpdateAndDel-toMakesurelist.action?menuId=4028338158eb8df90158ebfbdd7c002b&keywords="+hjxt_id
    dqr_header = {
        "Cookie":writeAndReadTextFile().test_readCookies()
    }
    dqr_res = requests.get(dqr_url,headers=dqr_header,allow_redirects=False)
    return dqr_res

def test_web_UnconfirmedDetail():
    dqrresObj = test_web_UnconfirmedList()
    dqrres = dqrresObj.text
    login_url = getConstant.IP_WEB_180+"/dcms/bms/login.jsp"
    t = '<span id="pagemsg"'
    if t in dqrres:
        # print("待确认：查询列表成功")
        dqrNumber = re.compile('<label>总共(.*?)页,(.*?)条记录</label>').search(dqrres).group(2)
        
        if int(dqrNumber)>0:
            dqr_menuId = re.compile('<input type="hidden" name="menuId" id="menuId" value="(.*?)"/>').search(dqrres).group(1)
            dqrId = re.compile('<input name="ids" id="ids" type="checkbox" value="(.*?)" />').search(dqrres).group(1)
            dqr_updateCaseGetUrl = re.compile('updateCaseGetUrl=(.*?)"').search(dqrres).group(1)
            dqrDetail_url = getConstant.IP+"/dcms/ccsCase/Case-callinput.action?id="+dqrId+"&menuId="+dqr_menuId+"&keyword=&updateCaseGetUrl="+dqr_updateCaseGetUrl
            dqrDetail_header = {
                "Cookie":writeAndReadTextFile().test_readCookies()
            }
            dqrDetail_res = requests.get(dqrDetail_url,headers = dqrDetail_header).text
            if '<title>事件录入</title>' in dqrDetail_res:

                # ===========================================================================
                dqr_casecallId = re.compile('<input type="hidden" id="casecallId" name="casecallId" value="(.*?)"/>').search(dqrDetail_res).group(1)
                dqr_isFh = re.compile('<input type="hidden" name="isFh" id="isFh" value="(.*?)"/>').search(dqrDetail_res).group(1)
                dqr_casesource = re.compile('<input type="hidden" name="casesource" id="casesource" value="(.*?)"/>').search(dqrDetail_res).group(1)
                dqr_street = re.compile('<input type="hidden"  id="street" name="street" value="(.*?)"/>').search(dqrDetail_res).group(1) 
                dqr_p_name = re.compile('<input type="text" id="p_name" name="p_name" value="(.*?)"').search(dqrDetail_res).group(1)
                
                dqr_result = BeautifulSoup(dqrDetail_res,'html.parser')
                dqr_select_sex = dqr_result.find('select', attrs={'id': 'p_sex'})
                dqr_select_sourceid = dqr_result.find('select', attrs={'id': 'sourceid'})
                dqr_select_eorcId = dqr_result.find('select', attrs={'id': 'eorcid'})
                dqr_select_eventtypeoneid = dqr_result.find('select', attrs={'id': 'eventtypeoneid'})
                dqr_select_eventtypetwoid = dqr_result.find('select', attrs={'id': 'eventtypetwoid'})
                dqr_select_needconfirm = dqr_result.find('select', attrs={'id': 'needconfirm'})

                # 上报人性别
                dqr_p_sex = re.compile('<option selected="(.*?)" value="(.*?)">(.*?)</option>').search(str(dqr_select_sex)).group(3)
                # 案卷来源
                dqr_sourceid = re.compile('<option selected="selected" value="(.*?)">(.*?)</option>').search(str(dqr_select_sourceid)).group(1)
                # 手机号
                dqr_other_phone = re.compile(r'<input type="text" id="other_phone" name="other_phone"[\s\S]*value="(.*?)" class="text_sustb">').search(dqrDetail_res).group(1)
                # 案卷id
                dqr_id = re.compile('<input type="hidden" id="id" name="id" value="(.*?)"/>').search(dqrDetail_res).group(1)
                # 案卷类型
                dqr_eorcId = re.compile('<option selected="selected" value="(.*?)">(.*?)</option>').search(str(dqr_select_eorcId)).group(1)
                # 大类
                dqr_eventtypeoneid = re.compile('<option selected="selected" value="(.*?)">(.*?)</option>').search(str(dqr_select_eventtypeoneid)).group(1)
                # 小类
                dqr_eventtypetwoid = re.compile('<option selected="selected" value="(.*?)">(.*?)</option>').search(str(dqr_select_eventtypetwoid)).group(1)

                # 执法局
                loginItems = writeAndReadTextFile().test_read_appLoginResult()
                zfjItem = loginItems['zfj']['user']
                zfj_id = zfjItem['id']
                zfj_name = zfjItem['name']
                #万米网格
                dqr_gridid = re.compile('<input type="text" id="gridid" readonly name="gridid" value="(.*?)"').search(dqrDetail_res).group(1)    
                #是否核实
                dqr_needconfirm = re.compile('<option checked="" value="(.*?)">(.*?)</option>').search(str(dqr_select_needconfirm)).group(1)
                #描述
                dqr_description = re.compile(r'<textarea id="description" cols="30" rows="2" name="description"[\s\S]*class="(.*?)">(.*?)</textarea>').search(dqrDetail_res).group(2)
                #处理方式
                dqr_dealWay = re.compile('<input type="radio" id="(.*?)" name="dealWay" checked>(.*?)</input>').search(dqrDetail_res).group(1)
                #位置描述
                dqr_fieldintro = re.compile('<textarea id="fieldintro" cols="30" rows="2" name="fieldintro" oninput="(.*?)">(.*?)</textarea>').search(dqrDetail_res).group(2)
                qr_url = getConstant.IP_WEB_180+"/dcms/ccsCase/Case-callToCaseStart.action"
                webdata = writeAndReadTextFile().test_read_txt('E:/test/dcms/ChengGuan/testFile/queRen/querenanjuan_web.txt')
                picpath = "E:/test/dcms/ChengGuan/testFile/img/8.png"
                dqr_img_value = ('8.png', open(picpath,'rb'),'multipart/form-data')
                webdata_list = webdata.split(",")
                m = MultipartEncoder(
                    fields = {
                        "mposl":webdata_list[0],
                        "mposb":webdata_list[1],
                        "menuId":dqr_menuId,
                        "removeFileId":"",	
                        "updateCaseGetUrl":dqr_updateCaseGetUrl,	
                        "casecallId":dqr_casecallId,	
                        "imageid":"",
                        "px":"",	
                        "py":"",	
                        "deptId":"",
                        "isFh":dqr_isFh,
                        "casesource":dqr_casesource,
                        "dispatchDeptname":"",
                        "street":dqr_street,
                        "p_name":dqr_p_name,
                        "p_sex":dqr_p_sex,
                        "p_job":"",
                        "p_phone":"",
                        "other_phone":dqr_other_phone,
                        "feedback":"",
                        "source.id":dqr_sourceid,
                        "id":dqr_id,
                        "eorc.id":dqr_eorcId,
                        "eventtypeone.id":dqr_eventtypeoneid,
                        "eventtypetwo.id":dqr_eventtypetwoid,
                        "startConditionId":"", #这里是立案条件
                        "regioncode.id":webdata_list[2],
                        "bgcode.id":webdata_list[3],
                        "objcode":"",
                        "bgadminid.id":zfj_id,
                        "bgadminid2":zfj_name,#管理员名称
                        "gridid":dqr_gridid,
                        "needconfirm":dqr_needconfirm,
                        "description":dqr_description,
                        "dealWay":dqr_dealWay,
                        "fieldintro":dqr_fieldintro,
                        "upload":dqr_img_value
                    }
                )
                
                header = {
                    "Content-Type":m.content_type,
                    "Cookie":writeAndReadTextFile().test_readCookies()
                }
                #重定向没有返回值
                webres = requests.post(url = qr_url, data=m, headers=header,allow_redirects=False)
                web_res = webres.text
                mystr = web_res.find("errorCode")
                if mystr != -1:
                    print("XXXXXXXXXXweb工单确认失败XXXXXXXXXX")
                    return False
                elif ('Set-Cookie' in webres.headers):
                    print("====================对不起您未登录，请登录后再上报工单=====================")
                    return False
                else:
                    print("移动端执法局工单确认完毕")  
                    return True
                # ============================================================================
            else:
                print("XXXXXXXXXXX待确认：进入详情出错XXXXXXXXXX")
                return False
        else:
            print("待确认：列表暂无数据")
            return False
    elif 'Location' in dqrresObj.headers and dqrresObj.headers['Location'] == login_url:
        print("***************待确认：对不起请您先登录***********")
        return False
    else:
        print("XXXXXXXXXX待确认：意想不到的错误XXXXXXXXXX")
        return False



# if __name__=="__main__": 
#     test_web_UnconfirmedDetail()