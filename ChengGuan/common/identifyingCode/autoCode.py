#coding=utf-8  
  
  
from selenium import webdriver  
from selenium.webdriver.common.keys import Keys  
# from pytesser import *  
import pytesseract
from PIL import Image,ImageEnhance,ImageFilter  
from selenium.common.exceptions import NoSuchElementException,TimeoutException  
import os,time  
  
  
  
  
def before():  
  
  
    driver.get(src)  
  
  
    time.sleep(1)  
  
  
    driver.maximize_window() # 浏览器全屏显示  
  
  
    print ('\n浏览器全屏显示 ...')  
  
  
  
  
  
  
def Convertimg():  
      
    imglocation = ("//*[@id='loginForm']/div[4]/div[2]/img[1]")  
      
    #下载验证码图片保存到本地  
    driver.save_screenshot('E:\\pythonScript\\Codeimages\\code.png')  
      
    #打开本地图片  
    im = Image.open('E:\\pythonScript\\Codeimages\\code.png')  
  
  
    left = driver.find_element_by_xpath(imglocation).location['x']  
    top = driver.find_element_by_xpath(imglocation).location['y']  
    right = driver.find_element_by_xpath(imglocation).location['x'] + driver.find_element_by_xpath(imglocation).size['width']  
    bottom = driver.find_element_by_xpath(imglocation).location['y'] + driver.find_element_by_xpath(imglocation).size['height']  
  
  
    im = im.crop((left, top, right, bottom))  
  
  
    im.save('E:\\pythonScript\\Codeimages\\screenshot.png')  
  
  
    print (u"\n保存验证码图片完成")  
  
  
    #移除截屏的图片  
  
  
    os.remove('E:\\pythonScript\\Codeimages\\code.png')  
  
  
    print (u"\n删除截屏图片完成")  
  
  
    #处理验证码图片  
    src = ('E:\\pythonScript\\Codeimages\\screenshot.png')  
  
  
    #调用裁剪图片方法  
    Cutedge(src)  
  
  
    #移除截屏的图片  
    os.remove('E:\\pythonScript\\Codeimages\\screenshot.png')  
    #灰化图片处理  
    im = Image.open('E:\\pythonScript\\Codeimages\\CutedgeImage.png')  
      
    imgry = im.convert('L')  
    #二值化处理  
  
  
    threshold = 100  
    table = []  
    for i in range(256):  
        if i < threshold:  
            table.append(0)  
        else:  
            table.append(1)  
    out = imgry.point(table, '1')  
  
  
    out.save('E:\\pythonScript\\Codeimages\\rgb.png')  
  
  
    #vcode = pytesseract.image_to_string(out)  
  
    #print (vcode)  
  
    txtcode = pytesseract.image_to_string(out)  
  
  
    print (u"\n识别出验证码文字为：",txtcode)  
  
  
    print (len(txtcode.strip()))  
  
  
    if len(txtcode.strip()) == 4:  
  
  
            print(u"长度相等")  
                               
    else:  
            print (u"长度不相等，退出")  
              
            driver.quit()  
  
  
    #输入用户名和密码  
    driver.find_element_by_id("username").send_keys("123456")  
  
  
    driver.find_element_by_id("password").send_keys("123456")  
  
  
    time.sleep(2)  
  
  
    #对文本框输入验证码值  
    driver.find_element_by_id("verifyCode").send_keys(txtcode.strip())  
  
  
    time.sleep(3)  
    #点击登录     
    driver.find_element_by_xpath("//*[@id='loginForm']/div[5]/div/img").click()  
    #driver.find_element_by_class_name('loginbtn').click()  
    time.sleep(7)  
      
      
#针对有黑色边框的验证码图片的裁剪边缘      
def Cutedge(src):  
      
    #设置要裁剪的区域  
    im = Image.open(src)  
      
    w, h = im.size  
      
    print (u"\n验证码原图宽、高尺寸为：",w,h ) 
      
    box = (2,2,110,30)  
      
    im.crop(box).save('E:\\pythonScript\\Codeimages\\CutedgeImage.png')  
  
  
    print (u"\n保存裁剪的图片 CutedgeImage.png")  
  
  
#http://hos.sf-express.com      
src = ("https://cas.sf-express.com/cas/login?service=http%3A%2F%2Fhos.sf-express.com%2Findex.html&apptiket=dbe979f1b41f6ea2c1cbc710a33ca5ec18cf829000ed010c")  
  
  
driver = webdriver.Chrome() #Firefox()#  
  
  
def method_2(src):  
       
    before()  
  
  
    #调用图片裁剪方法  
    Convertimg()  
  
  
      
def clickInput():  
  
  
    driver.find_element_by_id("inputButton").click()  
  
  
    print ("\nInput Click Finish")  
  
  
def clickOutput():  
  
  
    print (u"\n开始执行点击事件")  
  
  
    #开始执行点击事件           inputButton  
    driver.find_element_by_id("outputButton").click()  
  
  
    time.sleep(2)  
  
  
    print (u'\n开始执行任务,执行间隔时间为10分钟 ...')  
  
  
  
  
  
  
    for i in range(1,4):  
  
  
        ISOTIMEFORMAT="%Y-%m-%d %X"  
      
        strTime = time.strftime( ISOTIMEFORMAT, time.localtime())  
  
  
        driver.refresh()  
  
  
        print (u"\n正在执行第 ",i,"次...",strTime ) 
      
        time.sleep(5)  
      
        driver.find_element_by_id("outputButton").click()  
      
        time.sleep(30)  
      
        print  
        #刷新浏览器  
        print (u"\n刷新当前页面 ...")  
      
        driver.refresh()  
      
        print (u'\n等待间隔时间为9分钟 ...')  
      
        time.sleep(505)  
      
        print (u"\n已执行完第 ",i,u"次，",u"已等待",i*10,u"分钟" ) 
        
    print (u'\n已执行完成...At The End OF,'+strTime)  
      
    driver.quit()  
  
  
def isPass():  
    try:            
        #driver.find_element_by_id("username").is_displayed() == True  
      
        driver.find_element_by_id('status').text == (u"验证码不正确！")  
          
        print (u"\n****校验提示信息_验证码输入不正确****")  
  
  
        driver.quit()  
  
  
        print(u"\n关闭浏览器，执行外层循环...")  
      
    except Exception:  
        print(u"\n****校验提示信息_验证码输入正确****")  
  
  
        clickOutput()  #------   click Output  
      
method_2(src) #进入工作页面  
  
  
isPass()  
  
  
#clickInput()  #------   click Input  
  
  
#clickOutput()  #------   click Output  
  
  
  
  
for i in range(1,6):  
  
  
    driver = webdriver.Chrome()  
      
    src = ("https://cas.sf-express.com/cas/login?service=http%3A%2F%2Fhos.sf-express.com%2Findex.html&apptiket=dbe979f1b41f6ea2c1cbc710a33ca5ec18cf829000ed010c")  
  
  
    method_2(src)  
  
  
    isPass()  
      
    #clickOutput()  
  
  