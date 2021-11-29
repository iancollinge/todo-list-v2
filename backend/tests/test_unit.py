from flask import url_for
from flask_testing import TestCase
from application import app, db
from application.models import Tasks

test_task = {
                "id": 1,
                "description": "Run unit tests",
                "completed": False
            }

class TestBase(TestCase):

    def create_app(self):
        # Defines the flask object's configuration for the unit tests
        app.config.update(
            SQLALCHEMY_DATABASE_URI='sqlite:///',
            DEBUG=True,
            WTF_CSRF_ENABLED=False
        )
        return app

    def setUp(self):
        # Will be called before every test
        db.create_all()
        db.session.add(Tasks(description="Run unit tests"))
        db.session.commit()

    def tearDown(self):
        # Will be called after every test
        db.session.remove()
        db.drop_all()

class TestRead(TestBase):

    def test_read_all_tasks(self):
        response = self.client.get(url_for('read_tasks'))
        all_tasks = { "tasks": [test_task] }
        self.assertEquals(all_tasks, response.json)
    
    def test_read_task(self):
        response = self.client.get(url_for('read_task', id=1))
        self.assertEquals(test_task, response.json)

class TestCreate(TestBase):

    def test_create_task(self):
        response = self.client.post(
            url_for('create_task'),
            json={"description": "Testing create functionality"},
            follow_redirects=True
        )
        self.assertEquals(b"Added task with description: Testing create functionality", response.data)
        self.assertEquals(Tasks.query.get(2).description, "Testing create functionality")
    
class TestUpdate(TestBase):

    def test_update_task(self):
        response = self.client.put(
            url_for('update_task', id=1),
            json={"description": "Testing update functionality"}
        )
        self.assertEquals(b"Updated task (ID: 1) with description: Testing update functionality", response.data)
        self.assertEquals(Tasks.query.get(1).description, "Testing update functionality")
    
    def test_complete_task(self):
        response = self.client.put(url_for('complete_task', id=1), follow_redirects=True)
        self.assertEquals(b"Task with ID: 1 set to completed = True", response.data)
        self.assertEquals(Tasks.query.get(1).completed, True)
    
    def test_incomplete_task(self):
        response = self.client.put(url_for('incomplete_task', id=1), follow_redirects=True)
        self.assertEquals(b"Task with ID: 1 set to completed = False", response.data)
        self.assertEquals(Tasks.query.get(1).completed, False)
        

class TestDelete(TestBase):

    def test_delete_task(self):
        response = self.client.delete(url_for('delete_task', id=1))
        self.assertEquals(b"Deleted task with ID: 1", response.data)
        self.assertIsNone(Tasks.query.get(1))
