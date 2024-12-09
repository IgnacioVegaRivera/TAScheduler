from django.template.context_processors import request
from django.test import TestCase, Client
import unittest

from djangoProject1.MethodFiles.Administrator import EditUser
from djangoProject1.models import User


class EditUserUnitTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.mock_user = User(
            id=1,
            first_name="John",
            last_name="Doe",
            username="johndoe",
            password="password123",
            email="johndoe@example.com",
            phone_number="1234567890",
            address="123 Main St",
            role="Admin"
        )
        self.mock_user.save()

    def test_EditFirstName(self):
        response = self.client.post('/configure_user.html', {'id': self.mock_user.id, 'first_name': 'Jane',
                                                            "form_name": "edit_user",
                                                            'last_name': 'Doe',
                                                            'email': 'johndoe@example.com',
                                                            'username': 'johndoe',
                                                            'phone_number': '1234567890',
                                                            'role': 'Admin'})
        self.mock_user.refresh_from_db()
        self.assertEqual(self.mock_user.first_name, "Jane")

    def test_EditFirstNameBlankEntry(self):
        response = self.client.post('/configure_user.html', {'id': self.mock_user.id, 'first_name': '',
                                                            "form_name": "edit_user",
                                                            'last_name': 'Doe',
                                                            'email': 'johndoe@example.com',
                                                            'username': 'johndoe',
                                                            'phone_number': '1234567890',
                                                            'role': 'Admin'})
        self.mock_user.refresh_from_db()
        self.assertEqual(self.mock_user.first_name, "John")

    def test_EditFirstNameInvalidEntry(self):
        response = self.client.post('/configure_user.html', {'id': self.mock_user.id, 'first_name': '123',
                                                            "form_name": "edit_user",
                                                            'last_name': 'Doe',
                                                            'email': 'johndoe@example.com',
                                                            'username': 'johndoe',
                                                            'phone_number': '1234567890',
                                                            'role': 'Admin'})
        self.mock_user.refresh_from_db()
        self.assertEqual(self.mock_user.first_name, "John")

    def test_EditLastName(self):
        response = self.client.post('/configure_user.html', {'id': self.mock_user.id, 'first_name': 'John',
                                                            "form_name": "edit_user",
                                                            'last_name': 'Smith',
                                                            'email': 'johndoe@example.com',
                                                            'username': 'johndoe',
                                                            'phone_number': '1234567890',
                                                            'role': 'Admin'})
        self.mock_user.refresh_from_db()
        self.assertEqual(self.mock_user.last_name, "Smith")

    def test_EditLastNameInvalidEntry(self):
        response = self.client.post('/configure_user.html', {'id': self.mock_user.id, 'first_name': 'John',
                                                            "form_name": "edit_user",
                                                            'last_name': '456',
                                                            'email': 'johndoe@example.com',
                                                            'username': 'johndoe',
                                                            'phone_number': '1234567890',
                                                            'role': 'Admin'})
        self.mock_user.refresh_from_db()
        self.assertEqual(self.mock_user.last_name, "Doe")

    def test_EditLastNameBlankEntry(self):
        response = self.client.post('/configure_user.html', {'id': self.mock_user.id, 'first_name': 'John',
                                                            "form_name": "edit_user",
                                                            'last_name': '',
                                                            'email': 'johndoe@example.com',
                                                            'username': 'johndoe',
                                                            'phone_number': '1234567890',
                                                            'role': 'Admin'})
        self.mock_user.refresh_from_db()
        self.assertEqual(self.mock_user.last_name, "Doe")

    def test_EditEmail(self):
        response = self.client.post('/configure_user.html', {'id': self.mock_user.id, 'first_name': 'John',
                                                            "form_name": "edit_user",
                                                            'last_name': 'Doe',
                                                            'email': 'janesmith@example.com',
                                                            'username': 'johndoe',
                                                            'phone_number': '1234567890',
                                                            'role': 'Admin'})
        self.mock_user.refresh_from_db()
        self.assertEqual(self.mock_user.email, "janesmith@example.com")

    def test_EditEmailBlankEntry(self):
        response = self.client.post('/configure_user.html', {'id': self.mock_user.id, 'first_name': 'John',
                                                            "form_name": "edit_user",
                                                            'last_name': 'Doe',
                                                            'email': '',
                                                            'username': 'johndoe',
                                                            'phone_number': '1234567890',
                                                            'role': 'Admin'})
        self.mock_user.refresh_from_db()
        self.assertEqual(self.mock_user.email, "johndoe@example.com")

    def test_EditEmailNoAt(self):
        response = self.client.post('/configure_user.html', {'id': self.mock_user.id, 'first_name': 'John',
                                                            "form_name": "edit_user",
                                                            'last_name': 'Doe',
                                                            'email': 'janesmithexample.com',
                                                            'username': 'johndoe',
                                                            'phone_number': '1234567890',
                                                            'role': 'Admin'})
        self.mock_user.refresh_from_db()
        self.assertEqual(self.mock_user.email, "johndoe@example.com")

    def test_EditEmailNoPeriod(self):
        response = self.client.post('/configure_user.html', {'id': self.mock_user.id, 'first_name': 'John',
                                                            "form_name": "edit_user",
                                                            'last_name': 'Doe',
                                                            'email': 'janesmith@examplecom',
                                                            'username': 'johndoe',
                                                            'phone_number': '1234567890',
                                                            'role': 'Admin'})
        self.mock_user.refresh_from_db()
        self.assertEqual(self.mock_user.email, "johndoe@example.com")

    def test_EditPhone(self):
        response = self.client.post('/configure_user.html', {'id': self.mock_user.id, 'first_name': 'John',
                                                            "form_name": "edit_user",
                                                            'last_name': 'Doe',
                                                            'email': 'janesmith@example.com',
                                                            'username': 'johndoe',
                                                            'phone_number': '1234567899',
                                                            'role': 'Admin'})
        self.mock_user.refresh_from_db()
        self.assertEqual(self.mock_user.phone_number, "1234567899")

    def test_EditPhoneInvalidEntry(self):
        response = self.client.post('/configure_user.html', {'id': self.mock_user.id, 'first_name': 'John',
                                                            "form_name": "edit_user",
                                                            'last_name': 'Doe',
                                                            'email': 'janesmith@example.com',
                                                            'username': 'johndoe',
                                                            'phone_number': 'invalidate',
                                                            'role': 'Admin'})
        self.mock_user.refresh_from_db()
        self.assertEqual(self.mock_user.phone_number, "1234567890")

    def test_EditPhoneTooShort(self):
        response = self.client.post('/configure_user.html', {'id': self.mock_user.id, 'first_name': 'John',
                                                            "form_name": "edit_user",
                                                            'last_name': 'Doe',
                                                            'email': 'janesmith@example.com',
                                                            'username': 'johndoe',
                                                            'phone_number': '12345',
                                                            'role': 'Admin'})
        self.mock_user.refresh_from_db()
        self.assertEqual(self.mock_user.phone_number, "1234567890")

    def test_EditPhoneTooLong(self):
        response = self.client.post('/configure_user.html', {'id': self.mock_user.id, 'first_name': 'John',
                                                            "form_name": "edit_user",
                                                            'last_name': 'Doe',
                                                            'email': 'janesmith@example.com',
                                                            'username': 'johndoe',
                                                            'phone_number': '1234567890123',
                                                            'role': 'Admin'})
        self.mock_user.refresh_from_db()
        self.assertEqual(self.mock_user.phone_number, "1234567890")

    def test_EditRole(self):
        response = self.client.post('/configure_user.html', {'id': self.mock_user.id, 'first_name': 'John',
                                                            "form_name": "edit_user",
                                                            'last_name': 'Doe',
                                                            'email': 'janesmith@example.com',
                                                            'username': 'johndoe',
                                                            'phone_number': '1234567890',
                                                            'role': 'TA'})
        self.mock_user.refresh_from_db()
        self.assertEqual(self.mock_user.role, "TA")

    def test_EditRoleInvalidEntry(self):
        response = self.client.post('/configure_user.html', {'id': self.mock_user.id, 'first_name': 'John',
                                                            "form_name": "edit_user",
                                                            'last_name': 'Doe',
                                                            'email': 'janesmith@example.com',
                                                            'username': 'johndoe',
                                                            'phone_number': '1234567890',
                                                            'role': 'Invalid'})
        self.mock_user.refresh_from_db()
        self.assertEqual(self.mock_user.role, "Admin")


class EditUserAcceptanceTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create(
            first_name="John",
            last_name="Doe",
            username="johndoe",
            password="password123",
            email="johndoe@example.com",
            phone_number="1234567890",
            address="123 Main St",
            role="Admin"
        )
        self.user.save()

    def test_EditFirstName(self):
        response = self.client.post('/configure_user.html', {'id': self.user.id, 'first_name': 'Jane',
                                                            "form_name": "edit_user",
                                                            'last_name': 'Doe',
                                                            'email': 'johndoe@example.com',
                                                            'username' : 'johndoe',
                                                            'phone_number': '1234567890',
                                                            'role': 'Admin'})
        self.user.refresh_from_db()
        self.assertEqual(self.user.first_name, "Jane")
        self.assertEqual(User.objects.count(), 1)
        self.assertIn('message', response.context)
        self.assertEqual(response.context['message'], 'The user has been successfully updated')


    def test_EditFirstNameInvalidEntry(self):
        response = self.client.post('/configure_user.html',
                                    {'id': self.user.id, 'first_name': '',
                                                            "form_name": "edit_user",
                                                            'last_name': 'Doe',
                                                            'email': 'johndoe@example.com',
                                                            'username' : 'johndoe',
                                                            'phone_number': '1234567890',
                                                            'role': 'Admin'})
        self.user.refresh_from_db()
        self.assertEqual(self.user.first_name, "John")
        self.assertEqual(User.objects.count(), 1)
        self.assertIn('message', response.context)
        self.assertEqual(response.context['message'], 'Something went wrong when updating the user')

    def test_EditLastName(self):
        response = self.client.post('/configure_user.html',
                                    {'id': self.user.id, 'first_name': 'John',
                                                            "form_name": "edit_user",
                                                            'last_name': 'Smith',
                                                            'email': 'johndoe@example.com',
                                                            'username' : 'johndoe',
                                                            'phone_number': '1234567890',
                                                            'role': 'Admin'})
        self.user.refresh_from_db()
        self.assertEqual(self.user.last_name, "Smith")
        self.assertEqual(User.objects.count(), 1)
        self.assertIn('message', response.context)
        self.assertEqual(response.context['message'], 'The user has been successfully updated')

    def test_EditLastNameInvalidEntry(self):
        response = self.client.post('/configure_user.html',
                                    {'id': self.user.id, 'first_name': 'John',
                                                            "form_name": "edit_user",
                                                            'last_name': '',
                                                            'email': 'johndoe@example.com',
                                                            'username' : 'johndoe',
                                                            'phone_number': '1234567890',
                                                            'role': 'Admin'})
        self.user.refresh_from_db()
        self.assertEqual(self.user.last_name, "Doe")
        self.assertEqual(User.objects.count(), 1)
        self.assertIn('message', response.context)
        self.assertEqual(response.context['message'], 'Something went wrong when updating the user')

    def test_EditEmail(self):
        response = self.client.post('/configure_user.html',
                                    {'id': self.user.id, 'first_name': 'John',
                                                            "form_name": "edit_user",
                                                            'last_name': 'Doe',
                                                            'email': 'janesmith@example.com',
                                                            'username' : 'johndoe',
                                                            'phone_number': '1234567890',
                                                            'role': 'Admin'})
        self.user.refresh_from_db()
        self.assertEqual(self.user.email, "janesmith@example.com")
        self.assertEqual(User.objects.count(), 1)
        self.assertIn('message', response.context)
        self.assertEqual(response.context['message'], 'The user has been successfully updated')

    def test_EditEmailInvalidEntry(self):
        response = self.client.post('/configure_user.html',
                                    {'id': self.user.id, 'first_name': 'John',
                                                            "form_name": "edit_user",
                                                            'last_name': 'Doe',
                                                            'email': 'invalidemail',
                                                            'username' : 'johndoe',
                                                            'phone_number': '1234567890',
                                                            'role': 'Admin'})
        self.user.refresh_from_db()
        self.assertEqual(self.user.email, "johndoe@example.com")
        self.assertEqual(User.objects.count(), 1)
        self.assertIn('message', response.context)
        self.assertEqual(response.context['message'], 'Something went wrong when updating the user')

    def test_EditPhone(self):
        response = self.client.post('/configure_user.html',
                                    {'id': self.user.id, 'first_name': 'John',
                                                            "form_name": "edit_user",
                                                            'last_name': 'Doe',
                                                            'email': 'johndoe@example.com',
                                                            'username' : 'johndoe',
                                                            'phone_number': '1234567899',
                                                            'role': 'Admin'})
        self.user.refresh_from_db()
        self.assertEqual(self.user.phone_number, "1234567899")
        self.assertEqual(User.objects.count(), 1)
        self.assertIn('message', response.context)
        self.assertEqual(response.context['message'], 'The user has been successfully updated')

    def test_EditPhoneInvalidEntry(self):
        response = self.client.post('/configure_user.html',
                                    {'id': self.user.id, 'first_name': 'John',
                                                            "form_name": "edit_user",
                                                            'last_name': 'Doe',
                                                            'email': 'johndoe@example.com',
                                                            'username' : 'johndoe',
                                                            'phone_number': 'invalid',
                                                            'role': 'Admin'})
        self.user.refresh_from_db()
        self.assertEqual(self.user.phone_number, "1234567890")
        self.assertEqual(User.objects.count(), 1)
        self.assertIn('message', response.context)
        self.assertEqual(response.context['message'], 'Something went wrong when updating the user')

    def test_EditRole(self):
        response = self.client.post('/configure_user.html',
                                    {'id': self.user.id, 'first_name': 'John',
                                                            "form_name": "edit_user",
                                                            'last_name': 'Doe',
                                                            'email': 'johndoe@example.com',
                                                            'username' : 'johndoe',
                                                            'phone_number': '1234567890',
                                                            'role': 'TA'})
        self.user.refresh_from_db()
        self.assertEqual(self.user.role, "TA")
        self.assertEqual(User.objects.count(), 1)
        self.assertIn('message', response.context)
        self.assertEqual(response.context['message'], 'The user has been successfully updated')

    def test_EditRoleInvalidEntry(self):
        response = self.client.post('/configure_user.html',
                                    {'id': self.user.id, 'first_name': 'John',
                                                            "form_name": "edit_user",
                                                            'last_name': 'Doe',
                                                            'email': 'johndoe@example.com',
                                                            'username' : 'johndoe',
                                                            'phone_number': '1234567890',
                                                            'role': 'Invalid'})
        self.user.refresh_from_db()
        self.assertEqual(self.user.role, "Admin")
        self.assertEqual(User.objects.count(), 1)
        self.assertIn('message', response.context)
        self.assertEqual(response.context['message'], 'Something went wrong when updating the user')
