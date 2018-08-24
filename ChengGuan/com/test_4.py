#-*- coding:utf-8 -*-
import requests,os,re,smtplib,time
import pytesseract
from bs4 import BeautifulSoup
from email.mime.text import MIMEText
from PIL import Image
# from email.MIMEMultipart import MIMEMultipart



myRequests = requests.Session()
headers = {'User-agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:47.0) Gecko/20100101 Firefox/47.0'}
myRequests.headers.update(headers)

webSite = ''
webUser = ''
webPass = ''


CodesImg = os.path.join(os.getcwd(), 'E:/test/dcms/ChengGuan/result/yzm2.png')

def _transcoding(data):
    if not data:
        return data
    result = None
    # if type(data) == unicode:
    #     result = data
    if type(data) == str:
        result = data.encode('utf-8')
    return result

    
sender = _transcoding('电信短信平台余额')
receiver = ['']
#receiver = ['']
subject = '电信短信平台余额'
smtpserver = ''
username = ''
password = ''

# def send_mail(balance):
#     msg = MIMEMultipart('alternative')
#     msg['Subject'] = subject
#     html = """
#     <h4>短信剩余余额：</h4>

#     <h2><b>%s</b> ￥</h2>
#     """ % balance
#     part = MIMEText(html,'html','utf-8')
#     msg.attach(part)

#     smtp = smtplib.SMTP()
#     smtp.connect('smtp.exmail.qq.com')
#     smtp.login(username,password)
#     smtp.sendmail(sender,receiver,msg.as_string())
#     smtp.quit()




class IMG(object):

    def __init__(self):
        self.codeImg = 'E:/test/dcms/ChengGuan/result/yzm2.png'
        self.iMg = self._openImg(self.codeImg)
        self.Im = self._openImg(self.codeImg.capitalize())
        self.w,self.h = self.Im.size
        self.cookies = ''

    def _bs4(self,soup):
        list = []
        Soup = BeautifulSoup(soup,"html.parser")
        for i in Soup.find_all('td'):
             list.append(i)
        return list


    def _openImg(self,name):
        try:
            im = Image.open(name)
            return im
        except:
            print('[!] Open %s failed' % name)
            exit()

    def _processImg(self,name):
        threshold = 140
        table = []
        for i in range(256):
            if i < threshold:
                table.append(0)
                print("11111111111111111111111")
            else:
                table.append(1)
                print("22222222222222222222222222222222222222222222")
        img = self._openImg(name)
        imgry = img.convert('L')
        out = imgry.point(table,'1')
        filename = self.codeImg.capitalize()
        out.save(filename)


    def getCodes(self):
        self.Cookies =[]
        url = "http://219.149.226.180:7897/dcms/bms/login.jsp"
        r = myRequests.get(url=url)
        if r.cookies:
            self.Cookies = str(r.cookies).split(' ')[1]
        f = open(CodesImg,'wb')
        f.write(r.content)
        f.close()


    def pIx(self):
        data = self.Im
        w = self.w
        h = self.h
        try:
            for x in range(1,w-1):
                if x > 1 and x != w-2:
                    left = x - 1
                    right = x + 1

                for y in range(1,h-1):
                    up = y - 1
                    down = y + 1

                    if x <= 2 or x >= (w - 2):
                        data.putpixel((x,y),255)

                    elif y <= 2 or y >= (h - 2):
                        data.putpixel((x,y),255)

                    elif data.getpixel((x,y)) == 0:
                        if y > 1 and y != h-1:
                            up_color = data.getpixel((x,up))
                            down_color = data.getpixel((x,down))
                            left_color = data.getpixel((left,y))
                            left_down_color = data.getpixel((left,down))
                            right_color = data.getpixel((right,y))
                            right_up_color = data.getpixel((right,up))
                            right_down_color = data.getpixel((right,down))

                            if down_color == 0:
                                if left_color == 255 and left_down_color == 255 and \
                                    right_color == 255 and right_down_color == 255:
                                    data.putpixel((x,y),255)
                                    data.save("text2.png","png")

                            elif right_color == 0:
                                if down_color == 255 and right_down_color == 255 and \
                                    up_color == 255 and right_up_color == 255:
                                    data.putpixel((x,y),255)
                                    data.save("text3.png","png")



                        if left_color == 255 and right_color == 255 \
                                and up_color == 255 and down_color == 255:
                            data.putpixel((x,y),255)
                    else:
                        pass
                    data.save("E:/test/dcms/ChengGuan/result/yzm8.png","png")
        except:
            return False


    def Pytess(self,name):
        threshold = 140
        table = []

        for i in range(256):
            if i < threshold:
                table.append(0)
            else:
                table.append(1)

        rep = {'O':'0',
            'I':'1',
            'L':'1',
            'Z':'2',
            'S':'8',
            'Q':'0',
            '}':'7',
            '*':'',
            'E':'6',
            ']':'0',
            '`':'',
            'B':'8',
            '\\':'',
            ' ':''
        }

        data = self._openImg(name)
        imgry = data.convert('L')
        out = imgry.point(table,'1')
        try:
            text = pytesseract.image_to_string(out)
            text = text.strip()
            text = text.upper()
        except :
            text = 0

        for r in rep:

            text = text.replace(r,rep[r])

        return text

    def loginSite(self,loginname,passwd,randnum,cookies):
        url = ''
        params = {
            'loginname':loginname,
            'password':passwd,
            'randnum':randnum,
          #  'returnUrl':'/admin/index/index.action'
        }
        r = myRequests.post(url=url,data=params)
        r.encoding = 'utf-8'
        loginUrl = ''
        r2 = myRequests.get(url=loginUrl)
        html = r2.text.encode('utf-8')
        return html









if __name__ == '__main__':
    i = 0
    while True:
        time.sleep(5)

        i += 1
        print ("[!]第%d次尝试发送"%i)

        I = IMG() #类实例化


        #获取验证码
        I.getCodes()

        #验证码图片处理
        I._processImg(I.codeImg)

        #去除干扰线
        I.pIx()

        #获取验证码
        codes = I.Pytess('test.png')

        #cookies
        cookies = I.cookies

        #登陆
        htmlSoup = I.loginSite(webUser,webPass,codes,cookies)


        List = I._bs4(htmlSoup)

        if List:
            st = List[3]
            text = re.search("\d{1,}",str(st))
            Balance = text.group(0)
            print ('[!]短信余额为：%s,正在发送!' % Balance)
            # send_mail(Balance)
            print ('[!]发送成功，正在退出程序...')
            time.sleep(2)
            exit()