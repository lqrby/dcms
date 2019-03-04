import unittest
from locust import HttpLocust, TaskSet, task
from Test_LiuCheng_0login import MyTest
class UserBehavior(TaskSet):
    def on_start(self):
        """ on_start is called when a Locust start before any task is scheduled """
        self.login()

    # def on_stop(self):
    #     """ on_stop is called when the TaskSet is stopping """
    #     self.logout()

    def login(self):
        # self.client.post("/login", {"username":"ellen_key", "password":"education"})
        unittest.main()
    # def logout(self):
    #     self.client.post("/logout", {"username":"ellen_key", "password":"education"})

    @task(1)
    def index(self):
        self.client.get("/")

    # @task(1)
    # def profile(self):
    #     self.client.get("/profile")

class WebsiteUser(HttpLocust):
    task_set = UserBehavior
    min_wait = 1000
    max_wait = 3000