from application import create_app
from application.models import db, Mechanic
import unittest


class TestMechanic(unittest.TestCase):
    def setUp(self):
        self.app = create_app("TestingConfig")
        with self.app.app_context():
            db.drop_all()
            db.create_all()
            self.test_mechanic = Mechanic(
                name="Test Mechanic",
                email="mech@example.com",
                phone="555-0000",
                salary=50000.0
            )
            db.session.add(self.test_mechanic)
            db.session.commit()
            self.mechanic_id = self.test_mechanic.id
        self.client = self.app.test_client()

    def test_create_mechanic(self):
        payload = {
            "name": "New Mechanic",
            "email": "newmech@example.com",
            "phone": "555-1111",
            "salary": 55000.0
        }
        response = self.client.post('/mechanics/', json=payload)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json['name'], "New Mechanic")

    def test_create_mechanic_missing_field(self):
        payload = {"name": "Incomplete Mechanic"}
        response = self.client.post('/mechanics/', json=payload)
        self.assertEqual(response.status_code, 400)

    def test_get_all_mechanics(self):
        response = self.client.get('/mechanics/')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(isinstance(response.json, list))

    def test_update_mechanic(self):
        payload = {
            "name": "Updated Mechanic",
            "email": "mech@example.com",
            "phone": "555-0000",
            "salary": 60000.0
        }
        response = self.client.put(f'/mechanics/{self.mechanic_id}', json=payload)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['name'], "Updated Mechanic")

    def test_update_mechanic_not_found(self):
        payload = {
            "name": "Ghost",
            "email": "ghost@example.com",
            "phone": "000-0000",
            "salary": 0
        }
        response = self.client.put('/mechanics/9999', json=payload)
        self.assertEqual(response.status_code, 404)

    def test_delete_mechanic(self):
        response = self.client.delete(f'/mechanics/{self.mechanic_id}')
        self.assertEqual(response.status_code, 200)

    def test_delete_mechanic_not_found(self):
        response = self.client.delete('/mechanics/9999')
        self.assertEqual(response.status_code, 404)

    def test_mechanics_by_ticket_count(self):
        response = self.client.get('/mechanics/most-tickets')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(isinstance(response.json, list))


if __name__ == '__main__':
    unittest.main()
