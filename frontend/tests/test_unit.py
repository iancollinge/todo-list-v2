from flask import url_for
from flask_testing import TestCase
from application import app
from application.routes import backend_host
import requests_mock

test_task = {
                "id": 1,
                "description": "Test the frontend",
                "completed": False
            }

class TestBase(TestCase):

    def create_app(self):
        # Defines the flask object's configuration for the unit tests
        app.config.update(
            DEBUG=True,
            WTF_CSRF_ENABLED=False
        )
        return app

class TestViews(TestBase):
    # Test whether we get a successful response from our routes
    def test_home_get(self):
        with requests_mock.Mocker() as m:
            all_tasks = { "tasks": [test_task] }
            m.get(f"http://{backend_host}/read/allTasks", json=all_tasks)
            response = self.client.get(url_for('home'))
            self.assert200(response)
    
    def test_create_task_get(self):
        response = self.client.get(url_for('create_task'))
        self.assert200(response)

    def test_update_task_get(self):
        with requests_mock.Mocker() as m:
            m.get(f"http://{backend_host}/read/task/1", json=test_task)
            response = self.client.get(url_for('update_task', id=1))
            self.assert200(response)

class TestRead(TestBase):

    def test_read_home_tasks(self):
        with requests_mock.Mocker() as m:
            all_tasks = { "tasks": [test_task] }
            m.get(f"http://{backend_host}/read/allTasks", json=all_tasks)
            response = self.client.get(url_for('home'))
            self.assertIn(b"Test the frontend", response.data)

class TestCreate(TestBase):

    def test_create_task(self):
        with requests_mock.Mocker() as m:
            all_tasks = { "tasks": 
                [
                    test_task,
                    {
                        "id": 2,
                        "description": "Testing create functionality",
                        "completed": False
                    }
                ] 
            }
            m.post(f"http://{backend_host}/create/task", text="Test response")
            m.get(f"http://{backend_host}/read/allTasks", json=all_tasks)
            response = self.client.post(
                url_for('create_task'),
                json={"description": "Testing create functionality"},
                follow_redirects=True
            )
            self.assertIn(b"Testing create functionality", response.data)
    
class TestUpdate(TestBase):

    def test_update_task(self):
        with requests_mock.Mocker() as m:
            m.get(f"http://{backend_host}/read/task/1", json=test_task)
            m.put(f"http://{backend_host}/update/task/1", text="Test response")
            test_task["description"] = "Testing update functionality"
            m.get(f"http://{backend_host}/read/allTasks", json={ "tasks": [test_task] })
            response = self.client.post(
                url_for('update_task', id=1),
                data={"description": "Testing update functionality"},
                follow_redirects=True
            )
            self.assertIn(b"Testing update functionality", response.data)
    
    def test_complete_task(self):
        with requests_mock.Mocker() as m:
            m.put(f"http://{backend_host}/complete/task/1")
            test_task["completed"] = True
            m.get(f"http://{backend_host}/read/allTasks", json={ "tasks": [test_task] })
            response = self.client.get(url_for('complete_task', id=1), follow_redirects=True)
            self.assert200(response)
    
    def test_incomplete_task(self):
        with requests_mock.Mocker() as m:
            m.put(f"http://{backend_host}/incomplete/task/1")
            test_task["completed"] = False
            m.get(f"http://{backend_host}/read/allTasks", json={ "tasks": [test_task] })
            response = self.client.get(url_for('incomplete_task', id=1), follow_redirects=True)
            self.assert200(response)
        

class TestDelete(TestBase):

    def test_delete_task(self):
        with requests_mock.Mocker() as m:
            m.delete(f"http://{backend_host}/delete/task/1")
            m.get(f"http://{backend_host}/read/allTasks", json={ "tasks": [] })
            response = self.client.get(
                url_for('delete_task', id=1),
                follow_redirects=True
            )
            self.assertNotIn(b"Test the frontend", response.data)
