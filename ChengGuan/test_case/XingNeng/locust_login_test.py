import sys
sys.path.append("E:/test/dcms/ChengGuan")
from test_case.LiuCheng_currency import login_test
from locust import HttpLocust, TaskSet, task
from selenium import webdriver
# import unittest
# from Test_LiuCheng_0login import MyTest
class UserBehavior(TaskSet):
    def on_start(self):
        """ on_start is called when a Locust start before any task is scheduled """
        self.login()

    def on_stop(self):
        """ on_stop is called when the TaskSet is stopping """
        self.logout()

    def login(self):
        self.client.post("http://219.149.226.180:7897/publicworkstation/userManage/pwdLogin.action", {"role":"5","username":"cszfj", "password":"123456"})
        # unittest.main()
        # driver = webdriver.Chrome("D:/python/chromeDriverSever/chromedriver.exe")
        # url = 'http://219.149.226.180:7897/dcms/bms/login.jsp'
        # login_test().test_web_login()
    def logout(self):
        self.client.post("/logout", {"username":"ellen_key", "password":"education"})

    @task(2)
    def index(self):
        self.client.get("/")

    @task(1)
    def profile(self):
        self.client.get("/profile")

class WebsiteUser(HttpLocust):
    task_set = UserBehavior
    min_wait = 1000
    max_wait = 3000