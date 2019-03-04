from locust import HttpLocust, TaskSet, task
from chengguan_authCode import test_login_authCode
from selenium import webdriver
class UserBehavior(TaskSet):

    @task(1)
    def webIndex(self):
        self.client.post("/")
            
    @task(1)
    def webLogin(self):
        driver = webdriver.Chrome("D:/python/chromeDriverSever/chromedriver.exe")
        url = 'http://219.149.226.180:7897'
        authCode = test_login_authCode(driver,url) #获取验证码
        while authCode == "" :
            authCode = test_login_authCode(driver,url) 
        reqBody = '{"logonname":"wangnannan","logonpassword":"123456", "code":'+authCode+'}'
        with self.client.post("/dcms/bmsAdmin/Admin-logon.action",reqBody,catch_response=True) as response:
            if response.status_code == 200:
                response.success()
                print("res:",response.text)
        # json_resp = response.json()
        # print("login",response,response.text)


class WebsiteUser(HttpLocust):
    task_set = UserBehavior
    min_wait = 3000
    max_wait = 6000