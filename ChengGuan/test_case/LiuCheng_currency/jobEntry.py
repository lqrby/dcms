# -*- coding: utf-8 -*-
import requests
import json
import sys,re
sys.path.append("E:/test/dcms/ChengGuan")
import time
import datetime
from config.Log import logging
from common.writeAndReadText import writeAndReadTextFile
from common.constant_all import getConstant
from requests_toolbelt import MultipartEncoder
from common.appReportPicture import test_app_ReportPicture

class submitOrder():   
    def __init__(self,orderData):
        # self.submiturl = submiturl
        self.orderData = orderData 
        # self.cookies = cookies
        if '180' in getConstant.IP:
            self.ip = getConstant.IP+getConstant.PORT_7897
        else:
            self.ip = getConstant.IP
        self.app_header = {
            "User-Agent": "Android/8.0",
            "Connection":"Keep-Alive",
            "Accept-Encoding":"gzip"
        }

    #web提交工单录入表单gongdanluru_2.txt_无需核实需要复核   
    def test_web_submitOrder(self):
        submiturl = self.ip+'/dcms/ccsCase/Case-callToCaseStart.action'
        if 'upload' in self.orderData:
            upload = self.orderData['upload']
        else:
            upload = "" 
        m = MultipartEncoder(
            fields = {
                "mposl":self.orderData['mposl'],
                "mposb":self.orderData['mposb'],
                "menuId":self.orderData['menuId'],
                "removeFileId":"",	
                "updateCaseGetUrl":"",	
                "casecallId":"",	
                "imageid":"",
                "px":"",	
                "py":"",	
                "deptId":"",
                "isFh":self.orderData['isFh'],
                "casesource":"",
                "dispatchDeptname":"",
                "street":self.orderData['street'],
                "p_name":self.orderData['p_name'],
                "p_sex":self.orderData['p_sex'],
                "p_job":self.orderData['p_job'],
                "p_phone":self.orderData['p_phone'],
                "other_phone":self.orderData['other_phone'],
                "feedback":self.orderData['feedback'],
                "source.id":self.orderData['source'],
                "id":"",
                "eorc.id":self.orderData['eorc'],
                "eventtypeone.id":self.orderData['eventtypeone'],
                "eventtypetwo.id":self.orderData['eventtypetwo'],
                "startConditionId":"", #立案条件
                "regioncode.id":self.orderData['regioncode'],
                "bgcode.id":self.orderData['bgcode'],
                "objcode":"",
                "bgadminid.id":self.orderData['bgadminid'],
                "bgadminid2":self.orderData['bgadminid2'],
                "gridid":self.orderData['gridid'],
                "needconfirm":self.orderData['needconfirm'],
                "description":self.orderData['description'],
                "dealWay":self.orderData['dealWay'],
                "fieldintro":self.orderData['fieldintro'],
                "upload":upload

            }
        )
        
        header = {
            "Content-Type":m.content_type,
            "Cookie":writeAndReadTextFile().test_readCookies(),
            "Connection":"keep-alive",
            "User-Agent":"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36",
            "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
            "Accept-Encoding":"gzip, deflate",
            "Accept-Language":"zh-CN,zh;q=0.9,en;q=0.8"
        }
        #重定向没有返回值
        webres = requests.post(url = submiturl, data=m, headers=header,allow_redirects=False)
        webres.connection.close()
        web_res = webres.text
        # print("结果",web_res)
        mystr = web_res.find("errorCode")
        if mystr != -1:
            print("XXXXXXXXXXweb工单录入失败XXXXXXXXXX")
        elif ('Set-Cookie' in webres.headers):
            print("xxxxxxxxx对不起您未登录，请登录后再上报工单xxxxxxxx")
        else:
            print("web工单录入成功")  
            return True

   
    ####=====这里开始===========================================================================================================

    #移动端上报案卷
    def test_app_submitOrder(self):
        submiturl = self.ip+"/dcms/pwasCase/pwasCase-pdasave.action"
        shangbao_data = {
            "eorc.id":self.orderData['eorcid'],#事部件类型 
            "fieldintro":self.orderData['fieldintro'],
            "deptId":"",
            "mposl":self.orderData['mposl'],
            "description":self.orderData['description'],
            "objcode":"",
            "eventtypeone.id":self.orderData['eventtypeoneId'], #大类  市容环境
            "gridid":self.orderData['gridid'],
            "bgadminid.id":self.orderData['id'], #上报人id
            "eventtypetwo.id":self.orderData['eventtypetwoId'], #小类   道路不洁
            "mposb":self.orderData['mposb']
        }
        #提交app案卷上报
        sb_res = requests.post(submiturl,shangbao_data,headers = self.app_header,timeout = 20)
        sb_respon = sb_res.text
        result_data= re.compile('<caseInputInfo><issuc>(.*?)</issuc><caseprochisid>(.*?)</caseprochisid><idcase>(.*?)</idcase></caseInputInfo>').search(sb_respon)
        issuc = result_data.group(1)
        caseprochisid = result_data.group(2)
        idcase = result_data.group(3)
        if issuc:
            if 'imgPath' in self.orderData:
                        # 上传图片地址
                imgUrl = self.ip+"/dcms/PwasAdmin/PwasAdmin-imageup.action?imagetype=image&idcase="+idcase+"&prochisid="+caseprochisid
                picpath = self.orderData['imgPath']
                test_app_ReportPicture(imgUrl,picpath)
                sb_res.connection.close()
            else:
                print("复核案卷未上传图片")
            return True
        else:
            print("XXXXXXXXXX上报失败XXXXXXXXXX")
            return False

    #####################################################################################################################
    #市民app上报案卷，表单数据gongdanluru_app_sm.txt_需核实复核  
    def test_app_sm_submitOrder(self):
        if '180' in getConstant.IP:
            ip = getConstant.IP+getConstant.PORT_7880
            print("爱吉林",ip)
        else:
            ip = getConstant.IP
        smsubmiturl = ip+"/publicworkstation/complaint/saveComplaint.action"
        print(smsubmiturl)
        sm_data = {
            "is_login":self.orderData['is_login'],
            "token":self.orderData['token'],
            "name":self.orderData['name'],
            "phone":self.orderData['phoneNumber'],#手机
            "longitude":self.orderData['longitude'],
            "latitude":self.orderData['latitude'],
            "complaincontent":self.orderData['complaincontent'],  #描述
            "bgcode":self.orderData['bgcode'], #网格
            "bgcodename":self.orderData['bgcodename'], #地址
            "gridid":self.orderData['gridid'],
            "wxsource":self.orderData['wxsource'],#ok
            "imgurl":self.orderData['imgurl'],#ok
            "userid":self.orderData['id'],  #id
            "eorcid":self.orderData['eorcid'],
            "eventoneid":self.orderData['eventoneid'],#大
            "eventtwoid":self.orderData['eventtwoid']
        }
        sb_respons = requests.post(smsubmiturl,sm_data,headers = self.app_header,timeout = 20)
        res = sb_respons.text
        sb_respons.connection.close()
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
    
    #***********************************************#
    #    执法局抽查巡检                              #
    #***********************************************#
    #进入执法局抽查巡检模块
    def test_app_EnterInspection(self):
        if '180' in getConstant.IP:
            ip = getConstant.IP+getConstant.PORT_7890
        else:
            ip = getConstant.IP
        zfjxjsb_url = ip+"/dcmsmobile/PwasAdmin/Patrol-pdalist.action?userId="+self.orderData['id']+"&page.pageSize=3&page.pageNo=1"
        zfjxj_res = requests.get(zfjxjsb_url,headers = self.app_header,timeout = 20)
        zfjxj_res.connection.close()
        if '"message":"success"' in zfjxj_res.text:
            return zfjxj_res.text
        else:
            print("XXXXXXXXX执法局巡检：进入抽查巡检模块出现问题XXXXXXXXX")
            return False

    #选择巡检路线
    def test_inspectionRoutei(self):
        xjlx_res = self.test_app_EnterInspection()
        if xjlx_res != False:
            starttime =time.strftime('%Y-%m-%d %H:%M:%S',time.localtime())
            time.sleep(3)
            endtime =time.strftime('%Y-%m-%d %H:%M:%S',time.localtime())
            bgcode ="220000003"
            bgcodename ="线路C组"
            username = self.orderData['name']
            remark = "李琦"
            userid = self.orderData['id']
            if '180' in getConstant.IP:
                ip = getConstant.IP+getConstant.PORT_7890
            else:
                ip = getConstant.IP
            xjlx_url = ip+"/dcmsmobile/PwasAdmin/Patrol-savePatrol.action?bgcode="+bgcode+"&bgcodename="+bgcodename+"&username="+username+"&remark="+remark+"&endtime="+endtime+"&starttime="+starttime+"&userid="+userid
            xjlx_res = requests.get(xjlx_url,headers = self.app_header,timeout = 20)
            xjlx_res.connection.close()
            if 'message":"保存成功' in xjlx_res.text:
                return xjlx_res.text
            else:
                return False
        else:
            return False


    #执法局巡检上报案卷
    def test_app_reportInspection(self):
        xjlx_result = self.test_inspectionRoutei()
        if xjlx_result != False:
            if '180' in getConstant.IP:
                ip = getConstant.IP+getConstant.PORT_7890
            else:
                ip = getConstant.IP
            sbaj_url = ip+"/dcmsmobile/pwasCase/Case-saveCaseByPatrol.action" 
            xjlxResult = json.loads(xjlx_result)
            sbaj_data = {
                "patrolId":xjlxResult["data"],#线路F
                "fieldintro":self.orderData['fieldintro'],
                "gridid":self.orderData['gridid'],
                "bgadminid.id":self.orderData['id'],
                "description":self.orderData['description'],
                "mposl":self.orderData['mposl'],
                "username":self.orderData['name'],
                "mposb":self.orderData['mposb']
            }
            sbaj_result = requests.post(sbaj_url,sbaj_data,headers = self.app_header,timeout = 20)

            if '"message":"true"' in sbaj_result.text:
                xjsbResult = json.loads(sbaj_result.text)
                if '180' in getConstant.IP:
                    ip = getConstant.IP+getConstant.PORT_7884
                    print("巡检上报图片",ip)
                else:
                    ip = getConstant.IP
                #上传巡检图片
                xjsbImgUrl = ip+"/dcmsmobile//PwasAdmin/PwasAdmin-imageup.action"
                xjsbpicpath = "E:/test/dcms/ChengGuan/testFile/img/5.png"
                xjsbimg_value = ('5.png', open(xjsbpicpath,'rb'),'multipart/form-data')
                mm = MultipartEncoder(
                    fields = {
                        "imagetype":"image",
                        "idcase": xjsbResult['data']['caseid'],
                        "prochisid": xjsbResult["data"]["taskId"],
                        "upload":xjsbimg_value
                    }
                )
                head = {
                    "User-Agent": "Android/8.0.0",
                    "Content-Type":"application/x-www-form-urlencoded",
                    "Connection":"Keep-Alive",
                    "Accept-Encoding":"gzip",
                    "Content-Type":mm.content_type
                }
                sbresponse = requests.post(url = xjsbImgUrl,data=mm, headers=head)
                sbresponse.connection.close()
                if '<issuc>true</issuc>' in sbresponse.text:
                    return True
                else:
                    print("XXXXXXXXXX巡检上报案卷图片上传失败XXXXXXXXXX")
                    return False
            else:
                print("返回空")
                return False
                




# if __name__=="__main__": 
#     results = writeAndReadTextFile().test_read_appLoginResult()
#     markPath = getConstant.PROJECT_PATH+"/common/numberMark.txt"
#     mark = writeAndReadTextFile().test_read_txt(markPath)
#     dict_mark = json.loads(mark)
#     number = int(dict_mark['zfj_sb'])+1
#     sb_dataObject = {}
#     sb_dataObject['bgadminId'] = results['zfj']['user']['id']
#     sb_dataObject['eorcId'] = getConstant.EORCID_BJ #案件类型
#     sb_dataObject['eventtypeoneId'] = getConstant.BJ_GGSS #大类
#     sb_dataObject['eventtypetwoId'] = getConstant.BJ_GGSS_RLJG #小类
#     sb_dataObject['description'] = "热力井盖损坏"+str(number)
#     sb_dataObject['fieldintro'] = "吉林市 高新开发区 高新开发区街道 恒厦社区 恒厦社区第九网格"
#     sb_dataObject['gridid'] = "22020600100109"
#     sb_dataObject['mposl'] = "14088524.212997204"
#     sb_dataObject['mposb'] = "5437559.658689937"
#     sb_dataObject['needconfirm'] = getConstant.NEEDCONFIRM_YES #是否核实
#     sb_dataObject['isFh'] = getConstant.ISFH_NO #是否复核 
    
#     dict_mark["zfj_sb"] = str(number)
#     print(dict_mark["zfj_sb"])
#     writeAndReadTextFile().test_write_txt(markPath,json.dumps(dict_mark))
#     submitOrder(sb_dataObject).test_app_submitOrder()