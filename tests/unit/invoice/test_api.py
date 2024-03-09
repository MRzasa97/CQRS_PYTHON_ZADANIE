import json
import unittest
from flask import Flask
from flask.testing import FlaskClient
from invoice.entrypoints.flask_app import app, BusWrapper

class FakeBus:
    def handle(self, cmd):
        pass

class TestApi(unittest.TestCase):
    def setUp(self):
        app.message_bus = BusWrapper(FakeBus())
        self.client = app.test_client()

    def test_create_invoice(self):
        data = {"email": "example@example.com", "amount": 2137}
        response = self.client.post('/invoices', json=data)
        self.assertEqual(response.status_code, 201)

    def test_update_invoice(self):
        data = {"id": 1, "amount": 2137}
        response = self.client.put('/invoices', json=data)
        self.assertEqual(response.status_code, 201)

    def test_delete_invoice(self):
        response = self.client.delete('/invoices/1')
        self.assertEqual(response.status_code, 200)

    def test_generate_report(self):
        data = {"email": "example@example.com"}
        response = self.client.post('/report', json=data)
        self.assertEqual(response.status_code, 200)

    def test_create_invoice_missing_email(self):
        data = {"amount": 2137}
        response = self.client.post('/invoices', json=data)
        self.assertEqual(response.status_code, 400)

    def test_create_invoice_missing_amount(self):
        data = {"email": "example@example.com"}
        response = self.client.post('/invoices', json=data)
        self.assertEqual(response.status_code, 400)

    def test_update_invoice_missing_id(self):
        data = {"amount": 2137}
        response = self.client.put('/invoices', json=data)
        self.assertEqual(response.status_code, 400)

    def test_update_invoice_missing_amount(self):
        data = {"id": 1}
        response = self.client.put('/invoices', json=data)
        self.assertEqual(response.status_code, 400)

    def test_generate_report_missing_email(self):
        data = {}
        response = self.client.post('/report', json=data)
        self.assertEqual(response.status_code, 400)