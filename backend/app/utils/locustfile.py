from locust import HttpUser, task, between

class LoadTestUser(HttpUser):
    """
    Default Locust load test file.
    This version is for manual running only:
    `locust -f backend/app/utils/locustfile.py --host https://reqres.in`
    """
    wait_time = between(1, 2)

    @task
    def get_users(self):
        self.client.get("/api/users")
