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
        self.orderData = orderData 
#web提交工单录入表单gongdanluru_2.txt_无需核实需要复核   
    def test_web_submitOrder(self):
        cookies = writeAndReadTextFile().test_readCookies()
        submiturl = getConstant.IP_WEB_91+"/dcms/ccsCase/Case-callToCaseStart.action"
        # webdata = writeAndReadTextFile().test_read_txt('E:/test/dcms/ChengGuan/testFile/shangBao/gongdanluru_web_4ny.txt')
        picpath = "E:/test/dcms/ChengGuan/testFile/img/1.png"
        img_value = ('1.png', open(picpath,'rb'),'multipart/form-data')
        # webdata_list = webdata.split(",")
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
                "startConditionId":self.orderData['startConditionId'],
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

   
    ####=====这里开始===========================================================================================================

    #移动端上报案卷
    def test_app_submitOrder(self):
        
        submiturl = getConstant.IP_WEB_91+"/dcms/pwasCase/pwasCase-pdasave.action"
        # sb_data = writeAndReadTextFile().test_read_txt('E:/test/dcms/ChengGuan/testFile/shangBao/gongdanluru_app_zfj.txt')
        # objlist = sb_data.split(",")
        shangbao_data = {
            "eorc.id":self.orderData['eorcId'],#事部件类型 
            "fieldintro":self.orderData['fieldintro'],
            "deptId":"",
            "mposl":self.orderData['mposl'],
            "description":self.orderData['description'],
            "objcode":"",
            "eventtypeone.id":self.orderData['eventtypeoneId'], #大类  市容环境
            "gridid":self.orderData['gridid'],
            "bgadminid.id":self.orderData['bgadminId'], #上报人id
            "eventtypetwo.id":self.orderData['eventtypetwoId'], #小类   道路不洁
            "mposb":self.orderData['mposb']
        }
        #提交app案卷上报
        sb_respon = requests.post(submiturl,shangbao_data).text
        result_data= re.compile('<caseInputInfo><issuc>(.*?)</issuc><caseprochisid>(.*?)</caseprochisid><idcase>(.*?)</idcase></caseInputInfo>').search(sb_respon)
        issuc = result_data.group(1)
        caseprochisid = result_data.group(2)
        idcase = result_data.group(3)
        if issuc:
            print("案卷上报成功")
            # 上传图片地址
            imgUrl = getConstant.IP_WEB_91+"/dcms/PwasAdmin/PwasAdmin-imageup.action?imagetype=image&idcase="+idcase+"&prochisid="+caseprochisid
            picpath = "E:/test/dcms/ChengGuan/testFile/img/1.jpg"
            test_app_ReportPicture(imgUrl,picpath)
            return True
        else:
            print("XXXXXXXXXX上报失败XXXXXXXXXX")
            return False





            
    #####################################################################################################################
    #市民app上报案卷，表单数据gongdanluru_app_sm.txt_需核实复核  
    def test_app_sm_submitOrder(self,smOrderData):
        # results_sm = writeAndReadTextFile().test_read_appLoginResult()
        # smUser = results_sm['sm']['result']
        smsubmiturl = getConstant.IP_WEB_91+"/publicworkstation/complaint/saveComplaint.action"
        # sm_sb_data = writeAndReadTextFile().test_read_txt('E:/test/dcms/ChengGuan/testFile/shangBao/gongdanluru_app_sm.txt')
        # smList = sm_sb_data.split(",")
        sm_data = {
            "is_login":smOrderData['is_login'],
            "token":smOrderData['token'],
            "name":smOrderData['name'],
            "phone":smOrderData['phone'],
            "longitude":smOrderData['longitude'],
            "latitude":smOrderData['latitude'],
            "complaincontent":smOrderData['complaincontent'],
            "bgcode":smOrderData['bgcode'],
            "bgcodename":smOrderData['bgcodename'],
            "gridid":smOrderData['gridid'],
            "wxsource":smOrderData['wxsource'],
            "imgurl":smOrderData['imgurl'],
            "userid":smOrderData['userid'],
            "eorcid":smOrderData['eorcid'],
            "eventoneid":smOrderData['eventoneid'],
            "eventtwoid":smOrderData['eventtwoid'],
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
    #***********************************************#
    #    执法局抽查巡检                              #
    #***********************************************#
    #进入执法局抽查巡检模块
    def test_app_EnterInspection(self):
        results = writeAndReadTextFile().test_read_appLoginResult()
        self.zfjUser = results['zfj']['user']
        zfjxjsb_url = getConstant.IP_WEB_91+"/dcmsmobile/PwasAdmin/Patrol-pdalist.action?userId="+self.zfjUser['id']+"&page.pageSize=3&page.pageNo=1"
        zfjxj_res = requests.get(zfjxjsb_url).text
        if '"message":"success"' in zfjxj_res:
            return zfjxj_res
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
            username = self.zfjUser['name']
            remark = "李琦"
            userid = self.zfjUser['id']
            xjlx_url = getConstant.IP_WEB_91+"/dcmsmobile/PwasAdmin/Patrol-savePatrol.action?bgcode="+bgcode+"&bgcodename="+bgcodename+"&username="+username+"&remark="+remark+"&endtime="+endtime+"&starttime="+starttime+"&userid="+userid
            xjlx_res = requests.get(xjlx_url).text
            if '"message":"保存成功"' in xjlx_res:
                return xjlx_res
            else:
                return False


    #执法局巡检上报案卷
    def test_app_reportInspection(self):
        xjlx_result = self.test_inspectionRoutei()
        if xjlx_result != False:
            sbaj_url = getConstant.IP_WEB_91+"/dcmsmobile/pwasCase/Case-saveCaseByPatrol.action" 
            xjlxResult = json.loads(xjlx_result)
            # print(xjlxResult["data"])
            sbaj_data = {
                "patrolId":xjlxResult["data"],#线路F
                "fieldintro":"吉林市",
                "gridid":"220202",
                "bgadminid.id":self.zfjUser['id'],
                "description":"建筑垃圾,渣土管理",
                "mposl":"1.2963401385063786E7",
                "username":self.zfjUser['name'],
                "mposb":"4853394.362829968"
            }
            sbaj_result = requests.post(sbaj_url,sbaj_data).text
            if '"message":"true"' in sbaj_result:
                xjsbResult = json.loads(sbaj_result)
                xjsbImgUrl = getConstant.IP_WEB_91+"/dcmsmobile//PwasAdmin/PwasAdmin-imageup.action"
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
                    "Content-Type":mm.content_type
                }
                sbresponse = requests.post(url = xjsbImgUrl,data=mm, headers=head).text
                if '<issuc>true</issuc>' in sbresponse:
                    return True
                else:
                    print("XXXXXXXXXX巡检上报案卷图片上传失败XXXXXXXXXX")
                    return False
                




if __name__=="__main__": 
    results = writeAndReadTextFile().test_read_appLoginResult()
    markPath = getConstant.PROJECT_PATH+"/common/numberMark.txt"
    mark = writeAndReadTextFile().test_read_txt(markPath)
    dict_mark = json.loads(mark)
    number = int(dict_mark['zfj_sb'])+1
    sb_dataObject = {}
    sb_dataObject['bgadminId'] = results['zfj']['user']['id']
    sb_dataObject['eorcId'] = getConstant.EORCID_BJ #案件类型
    sb_dataObject['eventtypeoneId'] = getConstant.BJ_GGSS #大类
    sb_dataObject['eventtypetwoId'] = getConstant.BJ_GGSS_RLJG #小类
    sb_dataObject['description'] = "热力井盖损坏"+str(number)
    sb_dataObject['fieldintro'] = "吉林市 高新开发区 高新开发区街道 恒厦社区 恒厦社区第九网格"
    sb_dataObject['gridid'] = "22020600100109"
    sb_dataObject['mposl'] = "14088524.212997204"
    sb_dataObject['mposb'] = "5437559.658689937"
    sb_dataObject['needconfirm'] = getConstant.NEEDCONFIRM_YES #是否核实
    sb_dataObject['isFh'] = getConstant.ISFH_NO #是否复核 
    
    dict_mark["zfj_sb"] = str(number)
    print(dict_mark["zfj_sb"])
    writeAndReadTextFile().test_write_txt(markPath,json.dumps(dict_mark))
    submitOrder(sb_dataObject).test_app_submitOrder()