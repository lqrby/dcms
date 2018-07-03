# from http.cookiejar import CookieJar
# from urllib.request import build_opener, HTTPCookieProcessor, Request
# from urllib.parse import urlencode
# from PIL import Image
# #import pytesseract
 
# #请求
# login = "http://acm.cup.edu.cn/login.php"
# header={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
 
# vcode = "http://acm.cup.edu.cn/vcode.php"
 
# cj = CookieJar()
# opener = build_opener(HTTPCookieProcessor(cj))
 
# #打开图片并写入
# imgb = opener.open(vcode)
# local = open('vv.jpg','wb')
# local.write(imgb.read())
# local.close()
 
# #vcode
# image = Image.open('vv.jpg')
# #vv = pytesseract.image_to_string(image)#成功几率20%左右吧
 
# data = urlencode({
# 'user_id':'python',
# 'password':'python',
# #'vcode':''+vv,
# 'submit':'Submit'
# }).encode('utf-8')
# req = Request(login,data,header)
# opener.open(req)
 
# link = "http://acm.cup.edu.cn/modifypage.php"
 
# print(opener.open(link).read().decode('utf-8'))
# #print(vv)#一般来说验证码对基本没问题，成功的话可以在html页面中找到两个自己的用户名
