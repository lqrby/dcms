from locust import HttpLocust, TaskSet, task

class UserBehavior(TaskSet):

    @task(1)
    def appLogin(self):
        reqBody = '{"role":"5","username":"cszfj", "password":"123456"}'
        with self.client.post("/",reqBody,catch_response=True) as response:
            if response.status_code == 200:
                response.success()
                print("res:",response.text)
        # json_resp = response.json()
        # print("login",response,response.text)



class WebsiteUser(HttpLocust):
    task_set = UserBehavior
    min_wait = 3000
    max_wait = 6000