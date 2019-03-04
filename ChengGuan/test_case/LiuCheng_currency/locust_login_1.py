# import sys
# sys.path.append("E:/test/dcms/ChengGuan")
# from LiuCheng_currency import login_test
from locust import HttpLocust, TaskSet, task
# from selenium import webdriver
# import unittest
# from Test_LiuCheng_0login import MyTest
class UserBehavior(TaskSet):
    # def on_start(self):
    #     """ on_start is called when a Locust start before any task is scheduled """
    #     # print("11111111111111111111")
    #     self.login()

    # def on_stop(self):
    #     """ on_stop is called when the TaskSet is stopping """
        
    #     self.logout()
    @task(1)
    def login(self):
        # print("http://219.149.226.180:7897/publicworkstation/userManage/pwdLogin.action")
        self.client.post("/", {"role":"5","username":"cszfj", "password":"123456"})
        # print("打印login",res,res.text)
        # unittest.main()
        # driver = webdriver.Chrome("D:/python/chromeDriverSever/chromedriver.exe")
        # url = 'http://219.149.226.180:7897/dcms/bms/login.jsp'
        # login_test().test_web_login()
    # def logout(self):
    #     print("4444444444444444444")
    #     self.client.post("/logout", {"username":"cszfj", "password":"123456"})

    # @task(2)
    # def index(self):
    #     print("555555555555555555555")
    #     response = self.client.get("/", catch_response=True)
    #     print("打印1",response)
        
    #     if response.status_code == 200:
    #             response.success()
    #     print("打印2",response.text)

    # @task(1)
    # def profile(self):
    #     print("666666666666666666666666666")
    #     profile = self.client.get("/profile")
    #     print("profile",profile,profile.text)

class WebsiteUser(HttpLocust):
    task_set = UserBehavior
    min_wait = 1000
    max_wait = 3000