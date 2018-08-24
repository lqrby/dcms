# import requests
import requests
import time
def downloads_pic(i):
    url = 'http://219.149.226.180:7897/dcms/bmsAdmin/Code-getCode.action'
    res = requests.get(url, stream=True)
    with open('E:/test/dcms/ChengGuan/com/img/'+str(i)+'yzm.png', 'wb') as f:
        for chunk in res.iter_content(chunk_size=1024):
            if chunk:  # filter out keep-alive new chunks
                f.write(chunk)
                f.flush()
        f.close()
#循环执行N次，即可保存N张验证素材了。
def downloads_img(i):
    url = 'http://219.149.226.180:7897/dcms/bmsAdmin/Code-getCode.action'
    img = requests.get(url, stream=True).content
    with open('E:/test/dcms/ChengGuan/com/img/'+str(i)+'xyzm.png', 'wb') as f:
        f.write(img)

 
def downimage(i):
    # 构建session
    sess = requests.Session()
    # 建立请求头
    headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.75 Safari/537.36",
             "Connection": "keep-alive"}
    # 这个url是联合航空公司验证码，根据访问时间戳返回图片
    url="https://account.flycua.com/sso/chineseVerifyCode.images"
    # 获取响应图片内容
    image=sess.get(url,headers=headers).content
    # 保存到本地
    with open(str(i)+"img.jpg","wb") as f:
        f.write(image)
        f.close()
if __name__=="__main__":
    # 获取10张图片
    for i in range(2999,3001):
        
        time.sleep(1)
        downloads_pic(i)
        # downloads_img(i)
        # time.sleep(1)