from locust import HttpLocust
from locust import TaskSet
from locust import task


class HelloTaskSet(TaskSet):

    @task
    def my_task(self):
        self.client.get('/')
        base64string = base64.encodestring('%s:%s' % ('nkhare', '12345')).replace('\n', '')
        self.client.get("/login", headers={"Authorization":"Basic %s" % base64string})


class HelloLocust(HttpLocust):
    task_set = HelloTaskSet
