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
        self.header = {
            "User-Agent":"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36",
            "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
            "Accept-Encoding":"gzip, deflate",
            "Accept-Language":"zh-CN,zh;q=0.9,en;q=0.8",
            "Cookie":writeAndReadTextFile().test_readCookies()
        }

        

    #待调整批示列表
    def adjustmentApprovalList(self):
        item = {}
        dtz_url = self.ip+'/dcms/cwsCase/Case-chiefadjustlist.action?casestate=36&menuId=402880e72fd3b938012fd3c0e0f50076&keywords='+self.keywords
        dtzres = requests.get(dtz_url,headers = self.header,allow_redirects = False, timeout = 20)
        dtz_res = dtzres.text 
        if '<span id="pagemsg"' in dtz_res:
            dtznumber = re.compile('<label>总共(.*?)页,(.*?)条记录</label>').search(dtz_res).group(2)
            if dtznumber > "0":
                dtzps_result = BeautifulSoup(dtz_res,'html.parser')
                dtzps_result.find('div', attrs={'class':'mainContentTableContainer'})
                dtzps_table = dtzps_result.findAll('table')[1]
                dtzps_table.findAll('tr')[0].extract()
                for tr in dtzps_table.findAll('tr'):
                    tdvalue = tr.findAll('td')[-3].get_text()
                    if 'oderNumber' in self.dataItem and tdvalue == self.dataItem['oderNumber']:
                        menuId = re.compile('<input type="hidden" id="menuId" name="menuId" value="(.*?)" />').search(dtz_res).group(1)
                        tr['menuId'] = menuId
                        item =  tr
                        break
                return item
            else:
                print("调整批示列表暂时为空！！！")  
        elif '<title>登录</title>' in dtz_res:
            print("对不起，请您先登录web端！！！")
        else:
            print("XXXXXXXXXXXXXXXXXXXXXXXX获取调整批示列表出错XXXXXXXXXXXXXXXXXXXXXXXX")


    def adjustmentApprovalDetail(self):
        dtzpsObj = self.adjustmentApprovalList()
        print("待调整批示案卷详情：",dtzpsObj)
        if dtzpsObj:
            dtzps_list = re.compile(r'<tr id="(.*?)"[\s\S]*onclick="casedo[\(](.*?),(.*?),(.*?),(.*?),this[\)]">').search(str(dtzpsObj))
            dtzid = dtzps_list.group(1)
            taskprocess = dtzps_list.group(5).strip("'")
            xqurl = self.ip+"/dcms/cwsCase/Case-chiefadjustview.action?id="+dtzid+"&menuId="+dtzpsObj['menuId']+"&taskprocess="+taskprocess
            res = requests.get(xqurl,headers = self.header)
            detalres = res.text
            res.connection.close()
            if '<title>调整批示案卷</title>' in detalres:
                taskcasestateid = re.compile('<input type="hidden" id="taskcasestateid" name="taskcasestateid" value="(.*?)"/>').search(detalres).group(1)
                tzps_url = self.ip+"/dcms/cwsCase/Case-chiefadjust.action"
                tzps_data = {
                    "taskcasestateid":taskcasestateid,
                    "menuId":dtzpsObj['menuId'],
                    "listPageUrl":"",	
                    "taskprocess":taskprocess,
                    "resultprocess":self.dataItem['resultprocess'],	#批准
                    "casestate":"",	
                    "id":dtzid,
                    "leaderComments":self.dataItem['leaderComments'],  #批准了
                    "sentence":	""
                }
                tz_res = requests.post(tzps_url,data = tzps_data,headers = self.header,timeout = 20)
                tzres = tz_res.text
                tz_res.connection.close()
                if tzres == "0":
                    print("******调整批示完成(%s)******"%self.dataItem['resultprocess'])
                    return True
                elif tzres == "1":
                    print("___________________对不起，不可以重复调整_________________")
                else:
                    print("XXXXXXXXXXXXXXXXXXX调整批示出错(%s)XXXXXXXXXXXXXXXXXX"%self.dataItem['resultprocess'])
            else:
                print("XXXXXXXXXXXXXXXXXXX进入调整批示案卷详情出错XXXXXXXXXXXXXXXXXXX")
        else:
            print("待调整批示列表中不存在该工单号{}".format(self.dataItem['oderNumber']))




# if __name__ == "__main__":
#     print("6666666666666666666666666666666666666666666666666666666666666666666666666")
#     dataItem = {}
#     dataItem['resultprocess'] = "批准"
#     dataItem['leaderComments'] = "批准了"
#     adjustmentApproval(dataItem).adjustmentApprovalList()

        


