# -*- coding: utf-8 -*-
import requests
import json
import sys,re
sys.path.append("E:/test/dcms/ChengGuan")
import time
from config.Log import logging
from common.writeAndReadText import writeAndReadTextFile
from common.constant_all import getConstant
from requests_toolbelt import MultipartEncoder
from common.appReportPicture import test_app_ReportPicture

class test_submitOrder():       
#web提交工单录入表单gongdanluru_2.txt_无需核实需要复核   
    def test_web_submitOrder(self):
        cookies = writeAndReadTextFile().test_readCookies()
        submiturl = getConstant.IP_WEB_180+"/dcms/ccsCase/Case-callToCaseStart.action"
        webdata = writeAndReadTextFile().test_read_txt('E:/test/dcms/ChengGuan/testFile/shangBao/gongdanluru_web_4ny.txt')
        picpath = "E:/test/dcms/ChengGuan/testFile/img/1.png"
        img_value = ('1.png', open(picpath,'rb'),'multipart/form-data')
        webdata_list = webdata.split(",")
        m = MultipartEncoder(
            fields = {
                "mposl":webdata_list[0],
                "mposb":webdata_list[1],
                "menuId":webdata_list[2],
                "removeFileId":"",	
                "updateCaseGetUrl":"",	
                "casecallId":"",	
                "imageid":"",
                "px":"",	
                "py":"",	
                "deptId":"",
                "isFh":webdata_list[3],
                "casesource":"",
                "dispatchDeptname":"",
                "street":webdata_list[4],
                "p_name":webdata_list[5],
                "p_sex":webdata_list[6],
                "p_job":webdata_list[7],
                "p_phone":webdata_list[8],
                "other_phone":webdata_list[9],
                "feedback":webdata_list[10],
                "source.id":webdata_list[11],
                "id":"",
                "eorc.id":webdata_list[12],
                "eventtypeone.id":webdata_list[13],
                "eventtypetwo.id":webdata_list[14],
                "startConditionId":webdata_list[15],
                "regioncode.id":webdata_list[16],
                "bgcode.id":webdata_list[17],
                "objcode":"",
                "bgadminid.id":webdata_list[18],
                "bgadminid2":webdata_list[19],
                "gridid":webdata_list[20],
                "needconfirm":webdata_list[21],
                "description":webdata_list[22],
                "dealWay":webdata_list[23],
                "fieldintro":webdata_list[24],
                "upload":img_value
            }
        )
        
        header = {
            "Content-Type":m.content_type,
            "Cookie":cookies
        }
        #重定向没有返回值
        webres = requests.post(url = submiturl, data=m, headers=header,allow_redirects=False)
        web_res = webres.text
        mystr = web_res.find("errorCode")
        if mystr != -1:
            print("XXXXXXXXXXweb工单录入失败XXXXXXXXXX")
            return False
        elif ('Set-Cookie' in webres.headers):
            print("====================对不起您未登录，请登录后再上报工单=====================")
            return False
        else:
            print("web工单录入成功")  
            return True

    #========移动端案卷上报==========================================================================================================
    #网格管理员app上报案卷，表单数据gongdanluru_app_wggly.txt无需核实需要复核   
    def test_app_wggly_submitOrder(self):
        login_results = writeAndReadTextFile().test_read_appLoginResult()
        wgglyUser = login_results['wggly']['user']
        wgglysubmiturl = getConstant.IP_WEB_180+"/dcms/pwasCase/pwasCase-pdasave.action"
        wggly_sb_data = writeAndReadTextFile().test_read_txt('E:/test/dcms/ChengGuan/testFile/shangBao/gongdanluru_app_wggly.txt')
        wgglyList = wggly_sb_data.split(",")
        wggly_shangbao_data = {
            "eorc.id":wgglyList[0],
            "fieldintro":wgglyList[1],
            "deptId":"",
            "mposl":wgglyList[2],
            "description":wgglyList[3],
            "objcode":"",
            "eventtypeone.id":wgglyList[4],
            "gridid":wgglyList[5],
            "bgadminid.id":wgglyUser['id'],
            "eventtypetwo.id":wgglyList[6],
            "mposb":wgglyList[7]
        }
        #网格管理员提交app案卷上报
        wggly_respon = requests.post(wgglysubmiturl,wggly_shangbao_data).text
        resultData= re.compile('<caseInputInfo><issuc>(.*?)</issuc><caseprochisid>(.*?)</caseprochisid><idcase>(.*?)</idcase></caseInputInfo>').search(wggly_respon)
        wgglydhs_issuc = resultData.group(1)
        wgglydhs_caseprochisid = resultData.group(2)
        wgglydhs_idcase = resultData.group(3)
        if wgglydhs_issuc:
            print("网格管理员：案卷上报成功")
            # 上传图片地址
            wgglyimgUrl = getConstant.IP_WEB_180+"/dcms/PwasAdmin/PwasAdmin-imageup.action?imagetype=image&idcase="+wgglydhs_idcase+"&prochisid="+wgglydhs_caseprochisid
            imgpicpath = "E:/test/dcms/ChengGuan/testFile/img/10.jpg"
            test_app_ReportPicture(wgglyimgUrl,imgpicpath)
            return True
        else:
            print("XXXXXXXXXX网格管理员：案卷上报失败XXXXXXXXXX")
            return False
    #=====================================================================================================================
    #执法局app上报案卷，表单数据gongdanluru_app_zfj.txt无需核实复核   
    def test_app_zfj_submitOrder(self):
        results = writeAndReadTextFile().test_read_appLoginResult()
        zfjUser = results['zfj']['user']
        zfjsubmiturl = getConstant.IP_WEB_180+"/dcms/pwasCase/pwasCase-pdasave.action"
        zfj_sb_data = writeAndReadTextFile().test_read_txt('E:/test/dcms/ChengGuan/testFile/shangBao/gongdanluru_app_zfj.txt')
        zfjList = zfj_sb_data.split(",")
        zfj_shangbao_data = {
            "eorc.id":zfjList[0],
            "fieldintro":zfjList[1],
            "deptId":"",
            "mposl":zfjList[2],
            "description":zfjList[3],
            "objcode":"",
            "eventtypeone.id":zfjList[4],
            "gridid":zfjList[5],
            "bgadminid.id":zfjUser['id'],
            "eventtypetwo.id":zfjList[6],
            "mposb":zfjList[7]
        }
        #提交app案卷上报
        zfj_respon = requests.post(zfjsubmiturl,zfj_shangbao_data).text
        result_data= re.compile('<caseInputInfo><issuc>(.*?)</issuc><caseprochisid>(.*?)</caseprochisid><idcase>(.*?)</idcase></caseInputInfo>').search(zfj_respon)
        issuc = result_data.group(1)
        caseprochisid = result_data.group(2)
        idcase = result_data.group(3)
        if issuc:
            print("执法局：案卷上报成功")
            # 上传图片地址
            imgUrl = getConstant.IP_WEB_180+"/dcms/PwasAdmin/PwasAdmin-imageup.action?imagetype=image&idcase="+idcase+"&prochisid="+caseprochisid
            picpath = "E:/test/dcms/ChengGuan/testFile/img/1.jpg"
            test_app_ReportPicture(imgUrl,picpath)
            return True
        else:
            print("XXXXXXXXXX执法局：上报失败XXXXXXXXXX")
            return False
        

    #####################################################################################################################
    #市民app上报案卷，表单数据gongdanluru_app_sm.txt_需核实复核  
    def test_app_sm_submitOrder(self):
        results_sm = writeAndReadTextFile().test_read_appLoginResult()
        smUser = results_sm['sm']['result']
        smsubmiturl = getConstant.IP_APP_180+"/publicworkstation/complaint/saveComplaint.action"
        sm_sb_data = writeAndReadTextFile().test_read_txt('E:/test/dcms/ChengGuan/testFile/shangBao/gongdanluru_app_sm.txt')
        smList = sm_sb_data.split(",")
        sm_data = {
            "is_login":smUser['is_login'],
            "token":smUser['token'],
            "name":smUser['name'],
            "phone":smUser['phoneNumber'],
            "longitude":smList[0],
            "latitude":smList[1],
            "complaincontent":smList[2],
            "bgcode":smList[3],
            "bgcodename":smList[4],
            "gridid":smList[5],
            "wxsource":smList[6],
            "imgurl":smList[7],
            "userid":smUser['id'],
            "eorcid":smList[8],
            "eventoneid":smList[9],
            "eventtwoid":smList[10],
        }
        res = requests.post(smsubmiturl,sm_data).text
        smsb_list = json.loads(res)
        if 'message' in smsb_list:
            print("市民-案卷上报成功")
            return True
        elif ('errCode' in smsb_list) and (smsb_list['errCode'] == '2'):
            print("市民apk未登录")
            return False
        else:
            print("市民-上报案卷失败！！！")
            return False



# if __name__=="__main__": 
#     test_submitOrder().test_web_submitOrder()