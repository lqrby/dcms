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
    def __init__(self,dataObject):
        self.dataObject = dataObject
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
        self.keywords = writeAndReadTextFile().test_read_systemId('呼叫系统')


    # 待确认流程
    def test_UnconfirmedDetal(self):
        #进入待确认列表
        dqrdetalurl = self.ip+"/dcms/bmsAdmin/PlCaseUpdateAndDel-toMakesurelist.action"
        dqrdetaldata = {
            "menuId":"4028338158eb8df90158ebfbdd7c002b",
            "keywords":self.keywords
        }
        dqrRes = requests.get(dqrdetalurl,params=dqrdetaldata,headers = self.header,allow_redirects=False,timeout = 20)
        dqrRespon = dqrRes.text
        dqrRes.connection.close()
        dqrItem = {}
        if '<span id="pagemsg"' in dqrRespon:
            dqrNumber = re.compile('<label>总共(.*?)页,(.*?)条记录</label>').search(dqrRespon).group(2)
            if dqrNumber > "0":
                dqr_menuId = re.compile('<input type="hidden" name="menuId" id="menuId" value="(.*?)"/>').search(dqrRespon).group(1)
                dqr_updateCaseGetUrl = re.compile('updateCaseGetUrl=(.*?)"').search(dqrRespon).group(1)
                dqrRespons = BeautifulSoup(dqrRespon,'html.parser')
                dqrTable = dqrRespons.find('table', attrs={'class':'ixtablokt'})
                dqrTable.findAll('tr')[0].extract()
                for tr in dqrTable.findAll('tr'):
                    dqrnumber = tr.findAll('td')[1].get_text()
                    dqrnumber = dqrnumber.strip()
                    oder_Number = self.dataObject['oderNumber']
                    if oder_Number == dqrnumber:
                        dqrItem['menuId'] = dqr_menuId
                        dqrItem['updateCaseGetUrl'] = dqr_updateCaseGetUrl
                        dqrItem['oderNumber'] = dqrnumber
                        oderid_td = tr.findAll('td')[0].find("input")['value']
                        dqrItem['oderid'] = oderid_td
                        break
                return dqrItem
            else:
                print("待确认列表暂时为空！！！")
                return dqrNumber
        elif 'Location' in dqrRes.headers and '/dcms/bms/login' in dqrRes.headers['Location']:
            print("对不起，请您先登录")
        else:
            print("XXXXXXXXXXXXXXXX待确认列表出错XXXXXXXXXXXXXXX")

    #进入确认案卷详情并确认案卷
    def test_web_UnconfirmedDetail(self):
        dqrObj = self.test_UnconfirmedDetal()
        if dqrObj:
            print("工单对象:",dqrObj)
            dqrDetail_url = self.ip+"/dcms/ccsCase/Case-callinput.action"
            dqrData = {
                "id" : dqrObj['oderid'],
                "menuId" : dqrObj['menuId'],
                "keyword" : dqrObj['updateCaseGetUrl']
            }
            dqrDetail_result = requests.get(dqrDetail_url, params = dqrData, headers = self.header, timeout = 20)
            dqrDetail_res = dqrDetail_result.text
            if '<title>事件录入</title>' in dqrDetail_res:
                dqr_result = BeautifulSoup(dqrDetail_res,'html.parser')
                dqr_sex = dqr_result.find('select', attrs={'id': 'p_sex'})
                dqr_select_sourceid = dqr_result.find('select', attrs={'id': 'sourceid'})
                dqr_select_needconfirm = dqr_result.find('select', attrs={'id': 'needconfirm'})
                if self.dataObject != {}:
                    dqr_needconfirm = self.dataObject['needconfirm']
                    dqr_isFh = self.dataObject['isFh']
                else:
                    loginItems = writeAndReadTextFile().test_read_appLoginResult()
                    #是否核实
                    dqr_needconfirm = re.compile('<option checked="" value="(.*?)">(.*?)</option>').search(str(dqr_select_needconfirm)).group(1)
                    #处理方式
                    dqr_isFh = re.compile('<input type="hidden" name="isFh" id="isFh" value="(.*?)"/>').search(dqrDetail_res).group(1)
                dqr_casecallId = re.compile('<input type="hidden" id="casecallId" name="casecallId" value="(.*?)"/>').search(dqrDetail_res).group(1)
                dqr_casesource = re.compile('<input type="hidden" name="casesource" id="casesource" value="(.*?)"/>').search(dqrDetail_res).group(1)
                dqr_street = re.compile('<input type="hidden"  id="street" name="street" value="(.*?)"/>').search(dqrDetail_res).group(1) 
                dqr_p_name = re.compile('<input type="text" id="p_name" name="p_name" value="(.*?)"').search(dqrDetail_res).group(1)
                # 上报人性别
                p_sex = re.compile('<option selected="(.*?)" value="(.*?)">(.*?)</option>').search(str(dqr_sex))
                if p_sex != None:
                    dqr_p_sex = p_sex.group(3)
                else:
                    dqr_p_sex = ""
                # 案卷来源
                dqr_sourceid = re.compile('<option selected="selected" value="(.*?)">(.*?)</option>').search(str(dqr_select_sourceid)).group(1)
                # 手机号
                dqr_other_phone = re.compile(r'<input type="text" id="other_phone" name="other_phone"[\s\S]*value="(.*?)" class="text_sustb">').search(dqrDetail_res).group(1)
                # 案卷id
                # dqr_id = re.compile('<input type="hidden" id="id" name="id" value="(.*?)"/>').search(dqrDetail_res).group(1)
                # # 案卷类型
                
                #万米网格
                dqr_gridid = re.compile('<input type="text" id="gridid" readonly name="gridid" value="(.*?)"').search(dqrDetail_res).group(1)    
                #描述
                dqr_description = re.compile(r'<textarea id="description" cols="30" rows="2" name="description"[\s\S]*class="(.*?)">(.*?)</textarea>').search(dqrDetail_res).group(2)
                # dqr_dealWay = re.compile('<input type="radio" id="(.*?)" name="dealWay" checked>(.*?)</input>').search(dqrDetail_res).group(1)
                #位置描述
                dqr_fieldintro = re.compile('<textarea id="fieldintro" cols="30" rows="2" name="fieldintro" oninput="(.*?)">(.*?)</textarea>').search(dqrDetail_res).group(2)
                qr_url = self.ip+"/dcms/ccsCase/Case-callToCaseStart.action"
                webdata = writeAndReadTextFile().test_read_txt('E:/test/dcms/ChengGuan/testFile/queRen/querenanjuan_web.txt')
                if 'upload' in self.dataObject:
                    upload = self.dataObject['upload']
                else:
                    upload = ""
                webdata_list = webdata.split(",")
                m = MultipartEncoder(
                    fields = {
                        "mposl":self.dataObject['mposl'], #经度
                        "mposb":self.dataObject['mposb'], #纬度
                        "menuId":dqrObj['menuId'], #菜单id
                        "removeFileId":"",	
                        "updateCaseGetUrl":dqrObj['updateCaseGetUrl'],	
                        "casecallId":dqr_casecallId,	#上报人相关，可为空
                        "imageid":"",
                        "px":"",	
                        "py":"",	
                        "deptId":"",
                        "isFh":self.dataObject['isFh'], #是否复核
                        "casesource":dqr_casesource,  #案卷来源
                        "dispatchDeptname":"",
                        "street":dqr_street,  #街道编码
                        "p_name":dqr_p_name,  #上报人名字
                        "p_sex":dqr_p_sex,  #性别
                        "p_job":"",
                        "p_phone":"",
                        "other_phone":dqr_other_phone,  #上报人手机号
                        "feedback":"",
                        "source.id":dqr_sourceid,  #来源统计
                        "id":dqrObj['oderid'],   #工单id
                        "eorc.id":self.dataObject['eorcid'],
                        "eventtypeone.id":self.dataObject['eventtypeone'],  #大类
                        "eventtypetwo.id":self.dataObject['eventtypetwo'],  #小类
                        "startConditionId":"", #这里是立案条件
                        "regioncode.id":self.dataObject['regioncodeId'],
                        "bgcode.id":self.dataObject['bgcodeId'],
                        "objcode":"",
                        "bgadminid.id":self.dataObject['id'],  #管理员id
                        "bgadminid2":self.dataObject['name'],#管理员名称
                        "gridid":dqr_gridid,   #万米网格
                        "needconfirm":self.dataObject['needconfirm'],  #是否核实
                        "description":dqr_description,   #描述
                        "dealWay":self.dataObject['isFh'],    
                        "fieldintro":dqr_fieldintro,   #位置描述
                        "upload":upload   #图片
                    }
                )
                
                header = {
                    "User-Agent":"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36",
                    "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
                    "Accept-Encoding":"gzip, deflate",
                    "Accept-Language":"zh-CN,zh;q=0.9,en;q=0.8",
                    "Content-Type":m.content_type,
                    "Cookie":writeAndReadTextFile().test_readCookies()
                }
                #重定向没有返回值
                webres = requests.post(url = qr_url, data=m, headers=header,allow_redirects=False,timeout = 20)
                web_res = webres.text
                webres.connection.close()
                mystr = web_res.find("errorCode")
                if mystr != -1:
                    print("XXXXXXXXXXweb工单确认失败XXXXXXXXXX")
                    return False
                elif ('Set-Cookie' in webres.headers):
                    print("对不起请您先登录")
                    return False
                else:
                    print("web端工单确认完毕")  
                    return True
        elif dqrObj == {}:
            print("待确认列表中不存在该工单:{}",format(self.dataObject['oderNumber']))
            return dqrObj
        else:
            print("XXXXXXXXXXX特么异常了XXXXXXXXXX")
          
        
            



# if __name__=="__main__": 
#     dataObject = writeAndReadTextFile().test_read_appLoginResult()


#     # loginUser = loginItems['wggly']['user']#核实人
#     # dataObject = {}
#     dataObject['oderNumber'] = '201903010036'
#     # dataObject['loginUser'] = loginUser
#     # dataObject['needconfirm'] = getConstant.NEEDCONFIRM_YES #核实
#     # dataObject['isFh'] = getConstant.ISFH_NO #回访
#     confirm(dataObject).test_web_UnconfirmedDetail()