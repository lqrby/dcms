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

#调整控制
class adjustControl():
    def __init__(self,dataItem):
        self.dataItem = dataItem
        if '180' in getConstant.IP:
            self.ip = getConstant.IP+getConstant.PORT_7897
        else:
            self.ip = getConstant.IP
        self.keywords = writeAndReadTextFile().test_read_systemId('协调系统')
        self.header = {
            "Cookie":writeAndReadTextFile().test_readCookies(),
            "User-Agent":"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36",
            "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
            "Accept-Encoding":"gzip, deflate",
            "Accept-Language":"zh-CN,zh;q=0.9,en;q=0.8"
            }
        

    #待调整控制列表
    def adjustControlList(self):
        dtzkz_url = self.ip+'/dcms/cwsCase/Case-controlAdjustmentlist.action?menuId=2c94bc953241df11013241e097840012&keywords='+self.keywords
        dtzkz_res = requests.get(dtzkz_url,headers = self.header,allow_redirects=False,timeout = 20)
        dtzkz_res.connection.close()
        if '<span id="pagemsg"' in dtzkz_res.text:
            dtzkznumber = re.compile('<label>总共(.*?)页,(.*?)条记录</label>').search(dtzkz_res.text).group(2)
            if dtzkznumber > "0":
                return dtzkz_res.text
            else:
                print("待调整批示列表暂时为空！！！")
                return False
        elif 'location' in dtzkz_res.headers and '/dcms/bms/login.jsp' in dtzkz_res.headers['location']:
            print("对不起，请您先登录web端！！！")
            return False
        else:
            print("XXXXXXXXXXXXXXXXXXXXXXXX获取列表出错XXXXXXXXXXXXXXXXXXXXXXXX")
            return False



    def adjustControlDetail(self):
        dtzkz_list = self.adjustControlList()
        if dtzkz_list != False:
            mysoup = BeautifulSoup(dtzkz_list,'html.parser')
            table = mysoup.findAll('table')[1]
            table.findAll('tr')[0].extract()
            ids = ""
            if self.dataItem['id']:
                for tr_item in table.findAll('tr'):
                    nyrid = tr_item.findAll('td')[1].get_text()
                    if nyrid == self.dataItem['id']:
                        ids = re.compile('<tr id="(.*?)"').search(str(tr_item)).group(1)
                        a_text = tr_item.find('a').get_text()
            else:
                tr_item = table.findAll('tr')[0]
                ids = re.compile('<tr id="(.*?)"').search(str(tr_item)).group(1)
                a_text = tr_item.find('a').get_text()
            
            if ids:
                if a_text == "关闭":
                    kzUrl = self.ip+"/dcms/cwsCase/Case-batchCloseAjust.action" 
                else:
                    kzUrl = self.ip+"/dcms/cwsCase/Case-batchOpenAjust.action" 
                kzData = {"ids":ids}
                kzRes = requests.post(kzUrl,kzData,headers =self.header,allow_redirects = False,timeout = 20)
                kzRes.connection.close()
                if kzRes.status_code == 302:
                    print("{}成功！！！！！！！！！".format(a_text))
            else:
                print("XXXXXXXXXX对不起，您输入的工单号有误XXXXXXXXXX")
            
           

if __name__ == "__main__":
    dataItem = {}
    dataItem['id'] = ""
    adjustControl(dataItem).adjustControlDetail()
    # adjustControl(dataItem).adjustControlList()

        


