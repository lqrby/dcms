import requests
import json ,re,random 
import sys,os
import chardet
sys.path.append("E:/test/dcms/ChengGuan")
import time
import cairosvg
from bs4 import BeautifulSoup
from common.writeAndReadText import writeAndReadTextFile
from common.constant_all import getConstant
from requests_toolbelt import MultipartEncoder
# from svgTrunPng import export


class XQD():
    def __init__(self,):
        # self.itemData = itemData
        if '180' in getConstant.IP:
            self.ip = getConstant.IP+getConstant.PORT_7884
        else:
            self.ip = getConstant.IP
        self.header = {
            "Cookie":writeAndReadTextFile().test_readCookies(),
            "Accept":"application/json, text/javascript, */*; q=0.01",
            "X-Requested-With":"XMLHttpRequest",
            "User-Agent":"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36",
            "Accept-Encoding":"gzip, deflate",
            "Accept-Language":"zh-CN,zh;q=0.9,en;q=0.8"
        }
        self.timeout = 20

    #把svg的图标转换为png格式
    def export(self,fromDir,colers, targetDir, exportType):
        # print("开始执行转换命令...")
        # files = os.listdir(fromDir)
        num = 0
        newPathArr = []
        i = 1
        for (filePath,coler) in zip (fromDir,colers):
            # path = os.path.join(fromDir,fileName)
            if os.path.isfile(filePath) and filePath[-3:] == "svg":
                num += 1
                fileHandle = open(filePath,encoding='UTF-8')  #<_io.TextIOWrapper name='E:/test/tubiao1/010105.svg' mode='r' encoding='cp936'> <class '_io.TextIOWrapper'>
                svg = fileHandle.read()
                svg = svg.replace('<path','<path style="fill:'+coler+'"')
                svg = svg.replace('<line','<line style="fill:'+coler+'"')
                svg = svg.replace('<polygon','<polygon style="fill:'+coler+'"')
                svg = svg.replace('<rect','<rect style="fill:'+coler+'"')
                svg = svg.replace('<circle','<circle style="fill:'+coler+'"')
                svg = svg.replace('<ellipse','<ellipse style="fill:'+coler+'"')
                svg = svg.replace('<polyline','<polyline style="fill:'+coler+'"')
                svg = svg.replace('<svg ','<svg width="28px" height = "36px" ')
                print("svg:",svg)
                fileHandle.close()
                # exportPath = os.path.join("", fileNames[:-4]+str(i)+"."+ exportType)
                exportPath = os.path.join(targetDir, str(i)+"."+ exportType)
                i+=1
                exportFileHandle = open(exportPath,'w',encoding='UTF-8')
                if exportType == "png":
                    cairosvg.svg2png(bytestring=svg, write_to=exportPath)
                    newPathArr.append(exportPath)
                exportFileHandle.close()
            else:
                print("XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX图标不是svg格式XXXXXXXXXXXXXXXXXXXXXXXXXXXXX")
                return fromDir
        # print("已导出 ", num, "个文件")
        # print("路径是",newPathArr)
        return newPathArr
    

    def test_ReportPicture(self,fromDir,colers,targetDir,exportType):
        imgUrl = self.ip+'/partselection/common/uploadImage.do'
        imgArr = []
        imagepath = self.export(fromDir,colers,targetDir,exportType)
        # files = os.listdir(imagepath)
        for img in imagepath:
            millis = int(round(time.time() * 1000)) 
            img_url = self.ip+'/filemanager/filePathServlet?num=1&type=image&suffix=png&_='+str(millis)
            img_rel_res = requests.get(img_url,headers = self.header,allow_redirects = False,timeout = 20)
            img_rel_res.connection.close()
            imgrelres = img_rel_res.text
            mystr = imgrelres[2:-2]
            m = MultipartEncoder(
                fields = {
                    'file':('icon.png', open(img,'rb'),'multipart/form-data'),
                    'type':'image',
                    'path':mystr
                }
            )
            header = {
                "Content-Type":m.content_type,
                "Cookie":writeAndReadTextFile().test_readCookies(),
                "Accept":"application/json, text/javascript, */*; q=0.01",
                "X-Requested-With":"XMLHttpRequest",
                "User-Agent":"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36",
                "Accept-Encoding":"gzip, deflate",
                "Accept-Language":"zh-CN,zh;q=0.9,en;q=0.8"
            }
            objsbres = requests.post(imgUrl,data = m,headers = header,allow_redirects = False,timeout = 20)
            objsbres.connection.close()
            if '服务调用成功' in objsbres.text:
                obj_result = json.loads(objsbres.text)
                imgres = json.loads(obj_result['result'])
                imgpaths = imgres["filePath"]
                # print("图片地址：",imgpaths)
                imgArr.append(imgpaths)
            else:
                print("XXXXXXXXXX图片出现问题XXXXXXXXXX")
                
                return False
            
        return imgArr
    
    #兴趣点详情
    def XQDdetails(self,weiyimaid):
        xqddetail_url = self.ip+'/partselection/poilyrs/getListSanjiByPage.do?curPage=1&pageSize=100&classid='+weiyimaid+'&_='+str(round(time.time()*1000))
        threeItem = requests.get(xqddetail_url,headers = self.header,allow_redirects = False,timeout = 20)
        threeItem.connection.close()
        if '服务调用成功' in threeItem.text:
            # time.sleep(5)
            threeResult = json.loads(threeItem.text)
            return threeResult['result']['list']
        else:
            print("XXXXXXXXXXXXXXXXXXXXX精确获取兴趣点失败XXXXXXXXXXXXXXXXXXXX")
            return False
        
    def XQDDetailsAndUpdeit(self,threeItem):
        objimg = []
        fuben = u'副本'
        listIcon = "E:/UI/list/"+threeItem["classid3"]+".svg"
        pointIcon = "E:/UI/point/"+threeItem["classid3"]+fuben+".svg"
        if os.path.isfile(listIcon) and os.path.isfile(pointIcon):
            locn_blue = '#3d99fc'
            locn_red = '#ff0000'
            yanse1 = locn_blue
            yanse2 = locn_red
            yanse3 = locn_blue
            yanse4 = locn_red
            hs_picpath1 = listIcon
            hs_picpath2 = listIcon
            hs_picpath3 = pointIcon
            hs_picpath4 = pointIcon
            fromDir = [hs_picpath1,hs_picpath2,hs_picpath3,hs_picpath4]
            colers =  [yanse1,yanse2,yanse3,yanse4]
            targetDir = 'E:/test/tubiao/'
            exportType = 'png'
            # print(fromDir)
            editUrl = self.ip+'/partselection/poilyrs/saveOrUpdate.do'
            imageArr = self.test_ReportPicture(fromDir,colers,targetDir,exportType)
            if imageArr:
                label = imageArr[0]
                labelred = imageArr[1]
                local = imageArr[2]
                localred = imageArr[3]
            else:
                label = threeItem['label']    
                labelred = threeItem['labelred']    
                local = threeItem['local']    
                localred = threeItem['localred']  
            
            if colers:
                for imgcoler in colers:
                    coler = imgcoler[1:]
                    objimg.append(coler)
                labelcolor = objimg[0]
                labelredcolor = objimg[1]
                localcolor = objimg[2]
                localredcolor = objimg[3]
            else:
                labelcolor = threeItem['labelcolor']    
                labelredcolor = threeItem['labelredcolor']    
                localcolor = threeItem['localcolor']    
                localredcolor = threeItem['localredcolor']  
            editData = {
                "uid":threeItem['uid'],
                "lyrurl":threeItem['lyrurl'],
                "lyrtype":threeItem['lyrtype'],
                "label":label,
                "labelred":labelred,
                "local":local,
                "localred":localred,
                "labelcolor": labelcolor,
                "labelredcolor":labelredcolor,
                "localcolor":localcolor,
                "localredcolor":localredcolor,
                "wfsurl":threeItem['wfsurl'],
                "issign":threeItem['issign'],
                "precistandard":threeItem['precistandard'],
            }
            res = requests.post(editUrl,editData,headers = self.header,allow_redirects = False,timeout = 20)
            res.connection.close()
            time.sleep(random.randint(2,4))
            if '服务调用成功' in res.text:
                print("兴趣点图标{}上传成功".format(threeItem["classid3"]))
                # return True
            else:
                print("XXXXXXXXXXXXXXXXXXXXX兴趣点图标{}上传失败XXXXXXXXXXXXXXXXXX".format(threeItem["classid3"]))
                # return False
        else:
            print(listIcon+"或"+pointIcon+"路径下的文件不存在XXXXXXXXXXXXXXXX")
            # return False

    # def BatchUpload(self):
    #     # oneArr = self.XQDOneList()  #所有一级分类
    #     one_arr = writeAndReadTextFile().test_read_txt('E:/UI/xqd.txt')
    #     oneArr = one_arr.split('\n\n')
    #     # print(type(oneArr),oneArr)
    #     # oneArr = ['01']
    #     for oneid in oneArr:
    #         twoArr = self.XQDTwoList(oneid) 
    #         twoArr = ['0101']
    #         for twoid in twoArr:
    #             threeItems = self.XQDThreeList(oneid,twoid)
    #             threeItems1 = [threeItems[4]]  #990000
    #             print("111111111111111111",threeItems1)
    #             threeItems = threeItems1
    #             for three_item in threeItems:
                    
    #                 self.XQDDetailsAndUpdeit(three_item)
    #                 print("结束")

    def BatchUpload(self):

        # allXQDurl = self.ip+"/partselection/poilyrs/getListSanjiByPage.do?curPage=1&pageSize=10000&_="+str(round(time.time()*1000))
        # allres = requests.get(allXQDurl,headers = self.header,timeout = 20)
        # if allres.status_code == 200:
        #     AllRES = json.loads(allres.text)
        #     arrres = []
        #     for item in AllRES['result']['list']:
        #         arrres.append(item['classid3'])
        #     strres  = ','.join(arrres)
        #     writeAndReadTextFile().test_write_txt('E:/UI/xqd.txt',strres)
                # print(item['classid3'])

        weiYiMa_arr = writeAndReadTextFile().test_read_txt('E:/UI/xqd.txt')
        weiYiMaArr = []
        weiYiMaArr = weiYiMa_arr.split(',')
        for weiYiMa in weiYiMaArr:
            ######### oneid = weiYiMa[0:2]
            ######### twoid = weiYiMa[2:4]
            ######### threeid = weiYiMa[4:6]
            time.sleep(5)
            # print("888",weiYiMa)
            threeItem = self.XQDdetails(weiYiMa)
            # print(threeItem)
            time.sleep(2)
            self.XQDDetailsAndUpdeit(threeItem[0])
            

if __name__=="__main__":

    xqd = XQD()
    xqd.BatchUpload()