# -*- coding: utf-8 -*-
import requests
import sys,re,time,json
sys.path.append("E:/test/dcms/ChengGuan")
from bs4 import BeautifulSoup
from config.Log import logging
from common.writeAndReadText import writeAndReadTextFile
from common.constant_all import getConstant
from requests_toolbelt import MultipartEncoder

class confirm():
    # 进入待确认列表页面
    def test_web_UnconfirmedList(self):
        hjxt_id = writeAndReadTextFile().test_read_systemId('呼叫系统')
        dqr_url = getConstant.IP+"/dcms/bmsAdmin/PlCaseUpdateAndDel-toMakesurelist.action?menuId=4028338158eb8df90158ebfbdd7c002b&keywords="+hjxt_id
        dqr_header = {
            "Cookie":writeAndReadTextFile().test_readCookies()
        }
        dqr_res = requests.get(dqr_url,headers=dqr_header,allow_redirects=False)
        return dqr_res

    def test_web_UnconfirmedDetail(self,dataObject):
        dqrresObj = self.test_web_UnconfirmedList()
        dqrres = dqrresObj.text
        login_url = getConstant.IP_WEB_180+"/dcms/bms/login.jsp"
        if '<span id="pagemsg"' in dqrres:
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
                    dqr_result = BeautifulSoup(dqrDetail_res,'html.parser')
                    dqr_select_sex = dqr_result.find('select', attrs={'id': 'p_sex'})
                    dqr_select_sourceid = dqr_result.find('select', attrs={'id': 'sourceid'})
                    dqr_select_eorcId = dqr_result.find('select', attrs={'id': 'eorcid'})
                    dqr_select_eventtypeoneid = dqr_result.find('select', attrs={'id': 'eventtypeoneid'})
                    dqr_select_eventtypetwoid = dqr_result.find('select', attrs={'id': 'eventtypetwoid'})
                    dqr_select_needconfirm = dqr_result.find('select', attrs={'id': 'needconfirm'})
                    if dataObject != {}:
                        loginUser = dataObject['loginUser']
                        dqr_needconfirm = dataObject['needconfirm']
                        dqr_isFh = dataObject['isFh']
                    else:
                        loginItems = writeAndReadTextFile().test_read_appLoginResult()
                        loginUser = loginItems['wggly']['user']#核实人
                        #是否核实
                        dqr_needconfirm = re.compile('<option checked="" value="(.*?)">(.*?)</option>').search(str(dqr_select_needconfirm)).group(1)
                        #处理方式
                        dqr_isFh = re.compile('<input type="hidden" name="isFh" id="isFh" value="(.*?)"/>').search(dqrDetail_res).group(1)
                    dqr_casecallId = re.compile('<input type="hidden" id="casecallId" name="casecallId" value="(.*?)"/>').search(dqrDetail_res).group(1)
                    dqr_casesource = re.compile('<input type="hidden" name="casesource" id="casesource" value="(.*?)"/>').search(dqrDetail_res).group(1)
                    dqr_street = re.compile('<input type="hidden"  id="street" name="street" value="(.*?)"/>').search(dqrDetail_res).group(1) 
                    dqr_p_name = re.compile('<input type="text" id="p_name" name="p_name" value="(.*?)"').search(dqrDetail_res).group(1)
                    # 上报人性别
                    p_sex = re.compile('<option selected="(.*?)" value="(.*?)">(.*?)</option>').search(str(dqr_select_sex))
                    if p_sex != None:
                        dqr_p_sex = p_sex.group(3)
                    else:
                        dqr_p_sex = ""
                    # 案卷来源
                    dqr_sourceid = re.compile('<option selected="selected" value="(.*?)">(.*?)</option>').search(str(dqr_select_sourceid)).group(1)
                    # 手机号
                    dqr_other_phone = re.compile(r'<input type="text" id="other_phone" name="other_phone"[\s\S]*value="(.*?)" class="text_sustb">').search(dqrDetail_res).group(1)
                    # 案卷id
                    dqr_id = re.compile('<input type="hidden" id="id" name="id" value="(.*?)"/>').search(dqrDetail_res).group(1)
                    # 案卷类型
                    dqr_eorcId = re.compile('<option selected="selected" value="(.*?)">(.*?)</option>').search(str(dqr_select_eorcId)).group(1)
                    # 大类
                    eventtypeoneid = re.compile('<option selected="selected" value="(.*?)">(.*?)</option>').search(str(dqr_select_eventtypeoneid))
                    # 小类
                    eventtypetwoid = re.compile('<option selected="selected" value="(.*?)">(.*?)</option>').search(str(dqr_select_eventtypetwoid))
                    
                    if dqr_eorcId == getConstant.EORCID_BJ:
                        if eventtypeoneid != None and eventtypetwoid != None:
                            dqr_eventtypeoneid = eventtypeoneid.group(1)
                            dqr_eventtypetwoid = eventtypetwoid.group(1)
                        else:
                            dqr_eventtypeoneid = getConstant.BJ_GGSS  #部件大类公共设施
                            dqr_eventtypetwoid = getConstant.BJ_GGSS_SSJG #部件小类上水井盖
                    else:
                        if eventtypeoneid != None and eventtypetwoid != None:
                            dqr_eventtypeoneid = eventtypeoneid.group(1)
                            dqr_eventtypetwoid = eventtypetwoid.group(1)
                        else:
                            dqr_eventtypeoneid = getConstant.SJ_SRHJ  #事件大类市容环境
                            dqr_eventtypetwoid = getConstant.SJ_SRHJ_YYWR #事件小类油烟污染

                    #万米网格
                    dqr_gridid = re.compile('<input type="text" id="gridid" readonly name="gridid" value="(.*?)"').search(dqrDetail_res).group(1)    
                    #描述
                    dqr_description = re.compile(r'<textarea id="description" cols="30" rows="2" name="description"[\s\S]*class="(.*?)">(.*?)</textarea>').search(dqrDetail_res).group(2)
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
                            "regioncode.id":dataObject['regioncodeId'],
                            "bgcode.id":dataObject['bgcodeId'],
                            "objcode":"",
                            "bgadminid.id":loginUser['id'],
                            "bgadminid2":loginUser['name'],#管理员名称
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
                        print("web端工单确认完毕")  
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
#     print("我进来了吗？")
#     loginItems = writeAndReadTextFile().test_read_appLoginResult()

#     loginUser = loginItems['wggly']['user']#核实人
#     dataObject = {}
#     dataObject['loginUser'] = loginUser
#     dataObject['needconfirm'] = getConstant.NEEDCONFIRM_YES #核实
#     dataObject['isFh'] = getConstant.ISFH_NO #回访
#     confirm().test_web_UnconfirmedDetail(dataObject)
#     print("我又执行了一遍666666666666666666666666666")