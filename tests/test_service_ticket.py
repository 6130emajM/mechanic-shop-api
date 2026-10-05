from application import create_app
from application.models import db, Customer, Mechanic, ServiceTicket
import unittest
from datetime import date


class TestServiceTicket(unittest.TestCase):
    def setUp(self):
        self.app = create_app("TestingConfig")
        with self.app.app_context():
            db.drop_all()
            db.create_all()

            self.test_customer = Customer(
                name="Test Customer",
                email="customer@example.com",
                password="testpass"
            )
            db.session.add(self.test_customer)
            db.session.commit()
            self.customer_id = self.test_customer.id

            self.test_mechanic = Mechanic(
                name="Test Mechanic",
                email="mechanic@example.com",
                phone="555-0000",
                salary=50000.0
            )
            db.session.add(self.test_mechanic)
            db.session.commit()
            self.mechanic_id = self.test_mechanic.id

            self.test_ticket = ServiceTicket(
                VIN="1HGCM82633A123456",
                description="Test repair",
                service_date=date(2026, 1, 1),
                customer_id=self.customer_id
            )
            db.session.add(self.test_ticket)
            db.session.commit()
            self.ticket_id = self.test_ticket.id

        self.client = self.app.test_client()

    def login(self):
        credentials = {"email": "customer@example.com", "password": "testpass"}
        response = self.client.post('/customers/login', json=credentials)
        return response.json['token']

    def test_create_service_ticket(self):
        payload = {
            "VIN": "2FTRX18W1XCA12345",
            "description": "Oil change",
            "service_date": "2026-02-01",
            "customer_id": self.customer_id
        }
        response = self.client.post('/service-tickets/', json=payload)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json['description'], "Oil change")

    def test_create_service_ticket_missing_field(self):
        payload = {"description": "Incomplete ticket"}
        response = self.client.post('/service-tickets/', json=payload)
        self.assertEqual(response.status_code, 400)

    def test_get_all_service_tickets(self):
        response = self.client.get('/service-tickets/')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(isinstance(response.json, list))

    def test_assign_mechanic(self):
        response = self.client.put(f'/service-tickets/{self.ticket_id}/assign-mechanic/{self.mechanic_id}')
        self.assertEqual(response.status_code, 200)
        self.assertIn(self.mechanic_id, response.json['mechanics'])

    def test_assign_mechanic_not_found(self):
        response = self.client.put(f'/service-tickets/{self.ticket_id}/assign-mechanic/9999')
        self.assertEqual(response.status_code, 404)

    def test_remove_mechanic(self):
        self.client.put(f'/service-tickets/{self.ticket_id}/assign-mechanic/{self.mechanic_id}')
        response = self.client.put(f'/service-tickets/{self.ticket_id}/remove-mechanic/{self.mechanic_id}')
        self.assertEqual(response.status_code, 200)
        self.assertNotIn(self.mechanic_id, response.json['mechanics'])

    def test_my_tickets_with_token(self):
        token = self.login()
        headers = {'Authorization': f'Bearer {token}'}
        response = self.client.get('/service-tickets/my-tickets', headers=headers)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(isinstance(response.json, list))

    def test_my_tickets_no_token(self):
        response = self.client.get('/service-tickets/my-tickets')
        self.assertEqual(response.status_code, 401)

    def test_edit_ticket_mechanics(self):
        payload = {"add_ids": [self.mechanic_id], "remove_ids": []}
        response = self.client.put(f'/service-tickets/{self.ticket_id}/edit', json=payload)
        self.assertEqual(response.status_code, 200)
        self.assertIn(self.mechanic_id, response.json['mechanics'])

    def test_edit_ticket_not_found(self):
        payload = {"add_ids": [], "remove_ids": []}
        response = self.client.put('/service-tickets/9999/edit', json=payload)
        self.assertEqual(response.status_code, 404)


if __name__ == '__main__':
    unittest.main()
