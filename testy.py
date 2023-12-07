import unittest
from flask_testing import TestCase
from src.app import app, users

class TestApp(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True
        users.clear()

    def test_hello_endpoint(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.decode(), 'Hello, this is an HTTP/1.1 server!')

    def test_get_all_users_endpoint(self):
        response = self.app.get('/users')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, [])

    def test_create_user_endpoint(self):
        payload = {"name": "Jan", "lastname": "Kowalski"}
        response = self.app.post('/users', json=payload)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json, {"message": "User created successfully"})
        self.assertEqual(users, [{"id": 1, "name": "Jan", "lastname": "Kowalski"}])

    def test_get_user_endpoint(self):
        users.append({"id": 1, "name": "Alicja", "lastname": "Nowak"})
        response = self.app.get('/users/1')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {"id": 1, "name": "Alicja", "lastname": "Nowak"})

    def test_get_user_not_found_endpoint(self):
        response = self.app.get('/users/100')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json, {"error": "User with id 100 not found"})

    def test_update_user_endpoint(self):
        users.append({"id": 1, "name": "Bartosz", "lastname": "Jankowski"})
        payload = {"name": "Robert"}
        response = self.app.patch('/users/1', json=payload)
        self.assertEqual(response.status_code, 204)
        self.assertEqual(users, [{"id": 1, "name": "Robert", "lastname": "Jankowski"}])

    def test_update_user_not_found_endpoint(self):
        payload = {"name": "Robert"}
        response = self.app.patch('/users/100', json=payload)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json, {"error": "User with id 100 not found"})

    def test_update_user_bad_request_endpoint(self):
        users.append({"id": 1, "name": "Bartosz", "lastname": "Jankowski"})
        payload = {"invalid_field": "Robert"}
        response = self.app.patch('/users/1', json=payload)
        self.assertEqual(response.status_code, 400)

    def test_replace_user_endpoint(self):
        users.append({"id": 1, "name": "Kacper", "lastname": "Woźniak"})
        payload = {"name": "Karol", "lastname": "Woźniak"}
        response = self.app.put('/users/1', json=payload)
        self.assertEqual(response.status_code, 204)
        self.assertEqual(users, [{"id": 1, "name": "Karol", "lastname": "Woźniak"}])

    def test_replace_user_not_found_endpoint(self):
        payload = {"name": "Karol", "lastname": "Woźniak"}
        response = self.app.put('/users/100', json=payload)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json, {"error": "User with id 100 not found"})

    def test_delete_user_endpoint(self):
        users.append({"id": 1, "name": "Dawid", "lastname": "Kamiński"})
        response = self.app.delete('/users/1')
        self.assertEqual(response.status_code, 204)
        self.assertEqual(users, [])

    def test_delete_user_not_found_endpoint(self):
        response = self.app.delete('/users/100')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json, {"error": "User with id 100 not found"})

class TestAppIntegration(TestCase):

    def create_app(self):
        return app

    def test_integration(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.decode(), 'Hello, this is an HTTP/1.1 server!')

        response = self.client.get('/users')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, [])

        payload = {"name": "Jan", "lastname": "Kowalski"}
        response = self.client.post('/users', json=payload)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json, {"message": "User created successfully"})
        self.assertEqual(users, [{"id": 1, "name": "Jan", "lastname": "Kowalski"}])

        response = self.client.get('/users/1')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {"id": 1, "name": "Jan", "lastname": "Kowalski"})

        response = self.client.patch('/users/1', json={"name": "Janek"})
        self.assertEqual(response.status_code, 204)
        self.assertEqual(users, [{"id": 1, "name": "Janek", "lastname": "Kowalski"}])

        response = self.client.put('/users/1', json={"name": "Jan", "lastname": "Kowalski Jr."})
        self.assertEqual(response.status_code, 204)
        self.assertEqual(users, [{"id": 1, "name": "Jan", "lastname": "Kowalski Jr."}])

        response = self.client.delete('/users/1')
        self.assertEqual(response.status_code, 204)
        self.assertEqual(users, [])

if __name__ == '__main__':
    unittest.main()
