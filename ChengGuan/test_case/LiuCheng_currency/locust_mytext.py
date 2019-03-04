from locust import HttpLocust, TaskSet, task

#WebsiteTasks（继承自TaskSet）TaskSet类就好比是蝗虫的大脑，控制着蝗虫的具体行为，即实际业务场景测试对应的任务集
class WebsiteTasks(TaskSet):
    def on_start(self):
        self.client.post("/login", {
            "username": "test",
            "password": "123456"
        })

    @task(2)
    def index(self):
        self.client.get("/")

    @task(1)
    def about(self):
        self.client.get("/about/")

#WebsiteUser（继承自HttpLocust，而HttpLocust继承自Locust）Locust类就好比是一群蝗虫，而每一只蝗虫就是一个类的实例
class WebsiteUser(HttpLocust):
    task_set = WebsiteTasks
    host = "http://debugtalk.com"
    min_wait = 1000
    max_wait = 5000