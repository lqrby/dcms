# coding:utf-8
# coding:cp936
from selenium import webdriver
from PIL import Image

broswer = webdriver.Chrome("D:/python/chromeDriverSever/chromedriver.exe")
broswer.maximize_window()  #将浏览器最大化
broswer.set_window_size(1920, 895)
broswer.implicitly_wait(30)#隐式等待
broswer.get("http://www.baidu.com")
broswer.save_screenshot('./result/yzm.png')
# broswer.get_screenshot_as_file("./result/yzm.png")
baidu = broswer.find_element_by_id('su')
left = baidu.location['x']
top = baidu.location['y']
elementWidth = baidu.location['x'] + baidu.size['width']
elementHeight = baidu.location['y'] + baidu.size['height']
picture = Image.open('./result/yzm.png')
print(picture.size)
rang = (left, top, elementWidth, elementHeight)
print(rang)
picture = picture.crop((left, top, elementWidth, elementHeight))
picture.save('./result/yzm.png')