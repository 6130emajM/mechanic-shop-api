from application import create_app
from application.models import db, Customer
from application.utils import encode_token
import unittest


class TestCustomer(unittest.TestCase):
    def setUp(self):
        self.app = create_app("TestingConfig")
        with self.app.app_context():
            db.drop_all()
            db.create_all()
            self.test_customer = Customer(
                name="Test User",
                email="testuser@example.com",
                password="testpass"
            )
            db.session.add(self.test_customer)
            db.session.commit()
            self.customer_id = self.test_customer.id
        self.client = self.app.test_client()

    def login(self):
        credentials = {"email": "testuser@example.com", "password": "testpass"}
        response = self.client.post('/customers/login', json=credentials)
        return response.json['token']

    def test_create_customer(self):
        payload = {
            "name": "New Customer",
            "email": "newcustomer@example.com",
            "password": "newpass123"
        }
        response = self.client.post('/customers/', json=payload)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json['name'], "New Customer")

    def test_create_customer_duplicate_email(self):
        payload = {
            "name": "Duplicate",
            "email": "testuser@example.com",
            "password": "pass123"
        }
        response = self.client.post('/customers/', json=payload)
        self.assertEqual(response.status_code, 400)

    def test_create_customer_missing_field(self):
        payload = {"name": "Incomplete"}
        response = self.client.post('/customers/', json=payload)
        self.assertEqual(response.status_code, 400)

    def test_get_all_customers(self):
        response = self.client.get('/customers/')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(isinstance(response.json, list))

    def test_get_single_customer(self):
        response = self.client.get(f'/customers/{self.customer_id}')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['email'], "testuser@example.com")

    def test_get_single_customer_not_found(self):
        response = self.client.get('/customers/9999')
        self.assertEqual(response.status_code, 404)

    def test_login_success(self):
        credentials = {"email": "testuser@example.com", "password": "testpass"}
        response = self.client.post('/customers/login', json=credentials)
        self.assertEqual(response.status_code, 200)
        self.assertIn('token', response.json)

    def test_login_invalid_credentials(self):
        credentials = {"email": "testuser@example.com", "password": "wrongpass"}
        response = self.client.post('/customers/login', json=credentials)
        self.assertEqual(response.status_code, 401)

    def test_update_customer(self):
        token = self.login()
        headers = {'Authorization': f'Bearer {token}'}
        payload = {
            "name": "Updated Name",
            "email": "testuser@example.com",
            "password": "testpass"
        }
        response = self.client.put(f'/customers/{self.customer_id}', json=payload, headers=headers)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['name'], "Updated Name")

    def test_update_customer_no_token(self):
        payload = {
            "name": "Updated Name",
            "email": "testuser@example.com",
            "password": "testpass"
        }
        response = self.client.put(f'/customers/{self.customer_id}', json=payload)
        self.assertEqual(response.status_code, 401)

    def test_delete_customer(self):
        token = self.login()
        headers = {'Authorization': f'Bearer {token}'}
        response = self.client.delete(f'/customers/{self.customer_id}', headers=headers)
        self.assertEqual(response.status_code, 200)

    def test_delete_customer_no_token(self):
        response = self.client.delete(f'/customers/{self.customer_id}')
        self.assertEqual(response.status_code, 401)


if __name__ == '__main__':
    unittest.main()
