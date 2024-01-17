# in yourappname/tests.py

from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from .models import Invoice, InvoiceDetail
from datetime import date

class InvoiceAPITestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.invoice_data = {
            'date': date.today(),
            'customer_name': 'Test Customer',
        }
        self.invoice = Invoice.objects.create(**self.invoice_data)
        self.detail_data = {
            'invoice': self.invoice,
            'description': 'Test Description',
            'quantity': 2,
            'unit_price': 10.50,
            'price': 21.00,
        }
        self.detail = InvoiceDetail.objects.create(**self.detail_data)

    def test_create_invoice(self):
        response = self.client.post('/api/invoices/', self.invoice_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Invoice.objects.count(), 2)

    def test_retrieve_invoice(self):
        response = self.client.get(f'/api/invoices/{self.invoice.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['customer_name'], 'Test Customer')

    def test_create_invoice_detail(self):
        # Use the ID of the related Invoice instance
        detail_data = {
            'invoice': self.invoice.id,
            'description': 'Test Description',
            'quantity': 2,
            'unit_price': 10.50,
            'price': 21.00,
        }
        response = self.client.post('/api/invoices-details/', detail_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(InvoiceDetail.objects.count(), 2)

    def test_retrieve_invoice_detail(self):
        response = self.client.get(f'/api/invoices-details/{self.detail.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['description'], 'Test Description')

    def test_update_invoice(self):
        updated_data = {
            'date': '2024-01-01',  # Replace with the desired date format
            'customer_name': 'Updated Customer'
        }
        response = self.client.put(f'/api/invoices/{self.invoice.id}/', updated_data, format='json')

        # print(response.content)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['customer_name'], 'Updated Customer')


    def test_delete_invoice(self):
        response = self.client.delete(f'/api/invoices/{self.invoice.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Invoice.objects.count(), 0)

    def test_update_invoice_detail(self):
        updated_data = {
            'quantity': 3,
            'unit_price': 15.00,
            'price': 45.00,
            'invoice': self.invoice.id,  # Replace with the correct invoice ID
            'description': 'Updated Description'
        }
        response = self.client.put(f'/api/invoices-details/{self.detail.id}/', updated_data, format='json')

        # print(response.content)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['description'], 'Updated Description')




    def test_delete_invoice_detail(self):
        response = self.client.delete(f'/api/invoices-details/{self.detail.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(InvoiceDetail.objects.count(), 0)
