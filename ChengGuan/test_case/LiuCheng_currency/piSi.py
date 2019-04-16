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

#批示
class Approval():
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
        

    #待批示列表
    def stayApprovalList(self):
        item = {}
        dps_url = self.ip+'/dcms/cwsCase/Case-chiefapprovelist.action?casestate=35&menuId=402880822f9490ad012f949b44980045&keywords='+self.keywords
        dpsRespons = requests.get(dps_url,headers = self.header,timeout = 20)
        dps_res = dpsRespons.text
        dpsRespons.connection.close()
        if '<span id="pagemsg"' in dps_res:
            dtznumber = re.compile('<label>总共(.*?)页,(.*?)条记录</label>').search(dps_res).group(2)
            if dtznumber > "0":
                dps_result = BeautifulSoup(dps_res,'html.parser')
                dps_result.find('div', attrs={'class':'mainContentTableContainer'})
                dps_table = dps_result.findAll('table')[1]
                dps_table.findAll('tr')[0].extract()
                for tr in dps_table.findAll('tr'):
                    tdvalue = tr.findAll('td')[-3].get_text()
                    if 'oderNumber' in self.dataItem and tdvalue == self.dataItem['oderNumber']:
                        menuId = re.compile('<input type="hidden" id="menuId" name="menuId" value="(.*?)" />').search(dps_res).group(1)
                        tr['menuId'] = menuId
                        item =  tr
                        break
                return item
            else:
                print("待批示列表暂时为空！！！")
                return False
        elif '<title>登录</title>' in dps_res:
            print("对不起，请您先登录web端！！！")
            return False
        else:
            print("XXXXXXXXXXXXXXXXXXXXXXXX获取列表出错XXXXXXXXXXXXXXXXXXXXXXXX")
            return False


    # 批示案卷
    def stayApprovalDetail(self):
        dpsObj = self.stayApprovalList()
        if dpsObj:
            dpsList = re.compile(r'<tr id="(.*?)"[\s\S]*onclick="casedo[\(](.*?),(.*?),(.*?),(.*?),this[\)]">').search(str(dpsObj))
            id = dpsList.group(1)
            taskprocess = dpsList.group(5).strip("'")
            xqurl = self.ip+"/dcms/cwsCase/Case-chiefapproveview.action?id="+id+"&menuId="+dpsObj['menuId']+"&taskprocess="+taskprocess
            ps_Respons = requests.get(xqurl,headers = self.header,timeout = 20)
            res = ps_Respons.text
            ps_Respons.connection.close()
            if '<title>非正常结案待批示案卷</title>' in res:
                taskcasestateid = re.compile('<input type="hidden" id="taskcasestateid" name="taskcasestateid" value="(.*?)"/>').search(res).group(1)
                ps_url = self.ip+"/dcms/cwsCase/Case-chiefapprove.action"
                ps_data = {
                    "taskcasestateid":taskcasestateid,
                    "menuId":dpsObj['menuId'],
                    "taskprocess":taskprocess,
                    "casestate":"",	
                    "resultprocess":self.dataItem['resultprocess'],	#批准
                    "id":id,
                    "leaderComments":self.dataItem['leaderComments'],  #批准了
                    "sentence":	""
                }
                pishi_res = requests.post(ps_url,data = ps_data,headers = self.header,timeout = 20)
                ps_res = pishi_res.text
                pishi_res.connection.close()
                if ps_res == "0":
                    print("******批示完成(%s)******"%self.dataItem['resultprocess'])
                    return True
                elif ps_res == "1":
                    print("___________________对不起，不可以重复批示_________________")
                else:
                    print("XXXXXXXXXXXXXXXXXXX批示出错(%s)XXXXXXXXXXXXXXXXXX"%self.dataItem['resultprocess'])
            else:
                print("XXXXXXXXXXXXXXXXXXX进入批示案卷详情出错XXXXXXXXXXXXXXXXXXX")
        elif dpsObj == {}:
            print("待批示列表中没有该工单号:{}".format(self.dataItem['oderNumber']))
            return dpsObj

# if __name__ == "__main__":
#     dataItem = {}
#     dataItem['resultprocess'] = "批准"
#     dataItem['leaderComments'] = "批准了"
#     Approval(dataItem).stayApprovalDetail()

        


