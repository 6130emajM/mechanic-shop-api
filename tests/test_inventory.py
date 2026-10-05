from application import create_app
from application.models import db, Inventory
import unittest


class TestInventory(unittest.TestCase):
    def setUp(self):
        self.app = create_app("TestingConfig")
        with self.app.app_context():
            db.drop_all()
            db.create_all()
            self.test_item = Inventory(
                name="Test Part",
                price=19.99
            )
            db.session.add(self.test_item)
            db.session.commit()
            self.item_id = self.test_item.id
        self.client = self.app.test_client()

    def test_create_inventory_item(self):
        payload = {"name": "New Part", "price": 25.00}
        response = self.client.post('/inventory/', json=payload)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json['name'], "New Part")

    def test_create_inventory_item_missing_field(self):
        payload = {"name": "Incomplete Part"}
        response = self.client.post('/inventory/', json=payload)
        self.assertEqual(response.status_code, 400)

    def test_get_all_inventory(self):
        response = self.client.get('/inventory/')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(isinstance(response.json, list))

    def test_get_single_inventory_item(self):
        response = self.client.get(f'/inventory/{self.item_id}')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['name'], "Test Part")

    def test_get_single_inventory_item_not_found(self):
        response = self.client.get('/inventory/9999')
        self.assertEqual(response.status_code, 404)

    def test_update_inventory_item(self):
        payload = {"name": "Updated Part", "price": 30.00}
        response = self.client.put(f'/inventory/{self.item_id}', json=payload)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['name'], "Updated Part")

    def test_update_inventory_item_not_found(self):
        payload = {"name": "Ghost Part", "price": 0}
        response = self.client.put('/inventory/9999', json=payload)
        self.assertEqual(response.status_code, 404)

    def test_delete_inventory_item(self):
        response = self.client.delete(f'/inventory/{self.item_id}')
        self.assertEqual(response.status_code, 200)

    def test_delete_inventory_item_not_found(self):
        response = self.client.delete('/inventory/9999')
        self.assertEqual(response.status_code, 404)


if __name__ == '__main__':
    unittest.main()
