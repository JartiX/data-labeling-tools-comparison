from locust import HttpUser, task, between
import json
import random
import io

class CVATUser(HttpUser):
    wait_time = between(0.5, 1)

    def on_start(self):
        self.login()

    def login(self):
        response = self.client.post(
            "/api/auth/login",
            json={
                "username": f"user{random.randint(1, 5)}",
                "password": "testpass123"
            },
            headers={"Content-Type": "application/json"}
        )
        if response.status_code == 200:
            key = response.json().get("key")
            if key:
                self.client.headers.update({"Authorization": f"Token {key}"})
        else:
            print(f"Login failed: {response.status_code}, {response.text}")

    @task(3)
    def open_project(self):
        self.client.get("/api/projects/8")

    @task(1)
    def export_annotations(self):
        self.client.get("/api/tasks/17/annotations")

    @task(1)
    def import_annotations(self):
        coco_annotation = {
            "images": [{
                "id": 1,
                "width": 800,
                "height": 600,
                "file_name": "image1.jpg"
            }],
            "annotations": [{
                "id": 1,
                "image_id": 1,
                "category_id": 1,
                "bbox": [100, 100, 100, 100],
                "area": 10000,
                "iscrowd": 0
            }],
            "categories": [{
                "id": 1,
                "name": "label1"
            }]
        }

        annotation_bytes = json.dumps(coco_annotation).encode('utf-8')
        annotation_file = io.BytesIO(annotation_bytes)
        annotation_file.name = "annotations.json"

        self.client.post(
            "/api/tasks/17/annotations?format=COCO%201.0",
            headers={"Authorization": self.client.headers.get("Authorization")},
            files={"annotation_file": annotation_file}
        )
