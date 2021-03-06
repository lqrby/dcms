import sys,re
sys.path.append("E:/test/dcms/ChengGuan")
import time
import requests
import openpyxl
from bs4 import BeautifulSoup
from bs4 import SoupStrainer
from common.constant_all import getConstant
from common.writeAndReadText import writeAndReadTextFile


#用户权限配置
class PermissionConfiguration():

    def __init__(self,qxszitems):

        self.qxszitems = qxszitems
        self.header = {
            "User-Agent":"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36",
            "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
            "Accept-Encoding":"gzip, deflate",
            "Accept-Language":"zh-CN,zh;q=0.9,en;q=0.8",
            "Cookie":writeAndReadTextFile().test_readCookies()
            }

        if '180' in getConstant.IP:
            self.ip = getConstant.IP+getConstant.PORT_7897
        else:
            self.ip = getConstant.IP



    #模糊查询用户并返回员用户列表id
    def selectUserListId(self):
        allUserArr = []
        # for username in self.userNames: 
        selecturl = self.ip+"/dcms/bmsAdmin/Admin-searchUser.action"
        selectdata = {
            "name":"", 
            "photo":"",
            "logonname":self.uname,
            "email":"", 
            "phone":"", 
            "mobilephone":"" 
        }
        users = requests.post(selecturl,selectdata,headers = self.header,allow_redirects=False,timeout = 20)
        allUsers = users.text
        if "无人员" in allUsers:
            print('未查询到',self.uname)
        elif 'Location' in users.headers and '/dcms/bms/login' in users.headers['Location']:
            print("对不起！请您先登录")
        else:
            all_users = BeautifulSoup(allUsers,'html.parser')
            divObj = all_users.find('div', attrs={'class':'org_RfB'})
            dcl_li = divObj.findAll('li')
            for li in dcl_li:
                #获取用户id
                li_userid = re.compile("delAdmin(.*?);").search(str(li)).group(1)
                li_userid = li_userid[2:-2]
                allUserArr.append(li_userid)
        return allUserArr

    #查看用户详情，确定并返回哪个id是自己想想修改权限
    def userDetail(self):
        uId = ""
        users_Id = self.selectUserListId() #获取用户id列表
        detailUrl = self.ip+"/dcms/bmsAdmin/Admin-input.action"
        if users_Id:
            for uid in users_Id:
                params = {
                    "id":uid,
                    "action":"modify",
                    "tempJumpUrl":"Admin-getDeptUser.action?deptId=undefined"
                }
                user_detail = requests.get(detailUrl,params = params,headers = self.header,timeout = 20)
                userDetailRes = user_detail.text
                only_logonname = SoupStrainer(id="logonname")
                # this_user = BeautifulSoup(userDetailRes,'html.parser',parse_only=only_logonname).prettify()
                this_user = BeautifulSoup(userDetailRes,'html.parser')
                inputValue = this_user.find(id="logonname")["value"]
                if inputValue == self.uname: #这个用户登录名等于检索的登录名就跳出循环
                    uId = uid
                    break
        return uId
                

    # #权限设置 用户保存、取消配置模块权限
    def authorityAllocation(self):
        #权限设置 用户保存、取消配置模块权限 
        qxsz_uid = self.userDetail()   
        print("uid是：",qxsz_uid)
        qxszurl = self.ip+"/dcms/bmsAdmin/UserRole!saveUserRole.action"
        roleIds = ""
        # if 'Allocation' in qxszitems:
        #     roleIds = ','.join(qxszitems['Allocation'])
        qxszdata = {
            "userId":qxsz_uid,
            "roleIds":roleIds,
            "tempJumpUrl":"Admin-getDeptUser.action?deptId=undefined",
        }
        qxsz_res = requests.post(url = qxszurl,data = qxszdata,headers = self.header,allow_redirects=False,timeout = 20)
        if 'Location' in qxsz_res.headers and '/dcms/bmsAdmin/Admin-getDeptUser.action' in qxsz_res.headers['Location']:
            if roleIds:
                print('领导权限配置成功')
            else:
                print('普通职员权限配置成功')
        else:
            print('XXXXXXXXXX权限配置失败XXXXXXXXXX')
        qxsz_res.connection.close()   


    def allUsersConfiguration(self):
        for uname in qxszitems['userNames']:
            self.uname = uname
            self.authorityAllocation()


        
if __name__ == "__main__":
    qxszitems = {}
    #['gly','hbj','zfj','jdy',]
    userNames = ['gly','hbj','zfj']
    Allocation =[getConstant.authority_LT,getConstant.authority_XJCC,getConstant.authority_YYWR,getConstant.authority_DCKH,getConstant.authority_JTJT,getConstant.authority_DBZD,getConstant.authority_WFJJ,getConstant.authority_LD]
    qxszitems['userNames'] = userNames
    qxszitems['Allocation'] = Allocation
    PermissionConfiguration(qxszitems).allUsersConfiguration()
    
    
    




















