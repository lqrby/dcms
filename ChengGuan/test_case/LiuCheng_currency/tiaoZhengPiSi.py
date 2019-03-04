import requests
import json
import re
import ast
import sys
sys.path.append("E:/test/dcms/ChengGuan")
import time
from bs4 import BeautifulSoup
from config.Log import logging
from common.constant_all import getConstant
from common.writeAndReadText import writeAndReadTextFile
from requests_toolbelt import MultipartEncoder
from common.appReportPicture import test_app_ReportPicture

#调整批示
class adjustmentApproval():
    def __init__(self,dataItem):
        self.dataItem = dataItem
        if '180' in getConstant.IP:
            self.ip = getConstant.IP+getConstant.PORT_7897
        else:
            self.ip = getConstant.IP
        self.keywords = writeAndReadTextFile().test_read_systemId('协调系统')
        self.header = {"Cookie":writeAndReadTextFile().test_readCookies()}
        

    #待调整批示列表
    def adjustmentApprovalList(self):
        dtz_url = self.ip+'/dcms/cwsCase/Case-chiefadjustlist.action?casestate=36&menuId=402880e72fd3b938012fd3c0e0f50076&keywords='+self.keywords
        dtz_res = requests.get(dtz_url,headers = self.header).text
        if '<span id="pagemsg"' in dtz_res:
            dtznumber = re.compile('<label>总共(.*?)页,(.*?)条记录</label>').search(dtz_res).group(2)
            if dtznumber > "0":
                return dtz_res
            else:
                print("待调整批示列表暂时为空！！！")
                return False
        elif '<title>登录</title>' in dtz_res:
            print("对不起，请您先登录web端！！！")
            return False
        else:
            print("XXXXXXXXXXXXXXXXXXXXXXXX获取列表出错XXXXXXXXXXXXXXXXXXXXXXXX")
            return False



    def adjustmentApprovalDetail(self):
        dtzps_list = self.adjustmentApprovalList()
        # print("待调整列表：",dtzps_list)
        if dtzps_list != False:
            dtzps_result = BeautifulSoup(dtzps_list,'html.parser')
            dtzps_result.find('div', attrs={'class':'mainContentTableContainer'})
            dtzps_tr = dtzps_result.findAll('table')[1].findAll('tr')[1]
            menuId = re.compile('<input type="hidden" id="menuId" name="menuId" value="(.*?)" />').search(dtzps_list).group(1)
            dtzps_list = re.compile(r'<tr id="(.*?)"[\s\S]*onclick="casedo[\(](.*?),(.*?),(.*?),(.*?),this[\)]">').search(str(dtzps_tr))
            id = dtzps_list.group(1)
            taskprocess = dtzps_list.group(5).strip("'")
            xqurl = self.ip+"/dcms/cwsCase/Case-chiefadjustview.action?id="+id+"&menuId="+menuId+"&taskprocess="+taskprocess
            res = requests.get(xqurl,headers = self.header).text
            if '<title>调整批示案卷</title>' in res:
                taskcasestateid = re.compile('<input type="hidden" id="taskcasestateid" name="taskcasestateid" value="(.*?)"/>').search(res).group(1)
                tzps_url = self.ip+"/dcms/cwsCase/Case-chiefadjust.action"
                tzps_data = {
                    "taskcasestateid":taskcasestateid,
                    "menuId":menuId,
                    "listPageUrl":"",	
                    "taskprocess":taskprocess,
                    "resultprocess":self.dataItem['resultprocess'],	#批准
                    "casestate":"",	
                    "id":id,
                    "leaderComments":self.dataItem['leaderComments'],  #批准了
                    "sentence":	""
                }
                tz_res = requests.post(tzps_url,data = tzps_data,headers = self.header,timeout = 20)
                if tz_res.text == "0":
                    print("******调整批示完成(%s)******"%self.dataItem['resultprocess'])
                    return tz_res.text
                else:
                    print("XXXXXXXXXXXXXXXXXXX调整批示出错(%s)XXXXXXXXXXXXXXXXXX"%self.dataItem['resultprocess'])
                    return False
            else:
                print("XXXXXXXXXXXXXXXXXXX进入调整批示案卷详情出错XXXXXXXXXXXXXXXXXXX")
                return False


# if __name__ == "__main__":
#     dataItem = {}
#     dataItem['resultprocess'] = "批准"
#     dataItem['leaderComments'] = "批准了"
#     adjustmentApproval(dataItem).adjustmentApprovalDetail()

        


