import random
from locust import HttpUser, task, between, events
from locust.exception import StopUser

from tokens import tokens # Список токенов из личного кабинета Label Studio для каждого тестового пользователя
class LabelStudioUser(HttpUser):
    wait_time = between(0.5, 1)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.auth_token = None
        self.project_id = 22
        self.user_id = None
        self.tasks_ = []

    def on_start(self):
        self.refresh_token()
        self.get_user_id()
        self.get_projects()

    def get_user_id(self):
        response = self.client.get(
            "/api/current-user/whoami",
        )
        if response.status_code == 200:
            user_data = response.json()
            self.user_id = user_data.get("id")

    @task(1)
    def refresh_token(self):
        user_num = random.randint(1, 5)
        credentials = {
            "refresh": tokens[user_num - 1]
        }

        response = self.client.post(
            "/api/token/refresh/",
            json=credentials,
            headers={"Content-Type": "application/json"},
        )
        if response.status_code == 200:
            data = response.json()
            self.auth_token = data.get("access")

            self.client.headers.update({
                "Authorization": f"Bearer {self.auth_token}"
            })
        else:
            raise StopUser()

    def get_projects(self):
        response = self.client.get(
            "/api/projects/",

        )
        if response.status_code == 200:
            projects = response.json()

    @task(3)
    def get_project_details(self):
        if not self.project_id:
            return

        response = self.client.get(
            f"/api/projects/{self.project_id}/",

        )

    @task(5)
    def get_next_task(self):
        if not self.project_id:
            return

        response = self.client.get(
            f"/api/projects/{self.project_id}/next/",

        )
        if response.status_code == 200:
            task_data = response.json()
            if task_data:
                self.tasks_.append(task_data)

    @task(4)
    def get_project_tasks(self):
        if not self.project_id:
            return

        params = {
            "page": random.randint(1, 3),
            "page_size": 10
        }

        response = self.client.get(
            f"/api/projects/{self.project_id}/tasks",
            params=params,

        )

    @task(1)
    def export_project(self):
        if not self.project_id:
            return

        export_formats = ["JSON", "CSV", "TSV", "COCO", "YOLO"]
        export_format = random.choice(export_formats)

        params = {
            "exportType": export_format
        }

        response = self.client.get(
            f"/api/projects/{self.project_id}/export",
            params=params,

        )

    @task(2)
    def get_project_summary(self):
        if not self.project_id:
            return

        response = self.client.get(
            f"/api/projects/{self.project_id}/summary/",

        )

    @task(1)
    def update_user_profile(self):
        if not self.user_id:
            return

        profile_data = {
            "first_name": f"TestUser{random.randint(1, 100)}",
            "last_name": f"Load{random.randint(1, 100)}"
        }

        response = self.client.patch(
            f"/api/users/{self.user_id}/",
            json=profile_data,

        )
