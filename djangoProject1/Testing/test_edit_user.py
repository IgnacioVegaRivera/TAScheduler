from django.test import TestCase, Client
import unittest

from djangoProject1.MethodFiles.Administrator import EditUser
from djangoProject1.models import User

class EditUserUnitTest(unittest.TestCase):
    def setUp(self):
        self.mock_user = User(
            id=1,
            first_name="John",
            last_name="Doe",
            username="johndoe",
            password="password123",
            email="johndoe@example.com",
            phone_number="1234567890",
            address="123 Main St",
            role="User"
        )
        #self.mock_user.save()

    def test_EditFirstName(self):
        EditUser.edit_first_name(self.mock_user, "Jane")
        self.assertEqual(self.mock_user.first_name, "Jane")

    def test_EditFirstNameInvalidEntry(self):
        with self.assertRaises(ValueError):
            EditUser.edit_first_name(self.mock_user, "")

    def test_EditLastName(self):
        EditUser.edit_last_name(self.mock_user, "Smith")
        self.assertEqual(self.mock_user.last_name, "Smith")

    def test_EditLastNameInvalidEntry(self):
        with self.assertRaises(ValueError):
            EditUser.edit_last_name(self.mock_user, None)

    def test_EditUsername(self):
        EditUser.edit_username(self.mock_user, "janesmith")
        self.assertEqual(self.mock_user.username, "janesmith")

    def test_EditUsernameInvalidEntry(self):
        with self.assertRaises(ValueError):
            EditUser.edit_username(self.mock_user, "a" * 51)

    def test_EditPassword(self):
        EditUser.edit_password(self.mock_user, "NewPassword123!")
        self.assertEqual(self.mock_user.password, "NewPassword123!")

    def test_EditPasswordInvalidEntry(self):
        with self.assertRaises(ValueError):
            EditUser.edit_password(self.mock_user, "123")

    def test_EditEmail(self):
        EditUser.edit_email(self.mock_user, "janesmith@example.com")
        self.assertEqual(self.mock_user.email, "janesmith@example.com")

    def test_EditEmailInvalidEntry(self):
        with self.assertRaises(ValueError):
            EditUser.edit_email(self.mock_user, "")

    def test_EditPhone(self):
        EditUser.edit_phone(self.mock_user, "9876543210")
        self.assertEqual(self.mock_user.phone_number, "9876543210")

    def test_EditPhoneInvalidEntry(self):
        with self.assertRaises(ValueError):
            EditUser.edit_phone(self.mock_user, "invalid")

    def test_EditAddress(self):
        EditUser.edit_address(self.mock_user, "456 Another St")
        self.assertEqual(self.mock_user.address, "456 Another St")

    def test_EditAddressInvalidEntry(self):
        with self.assertRaises(ValueError):
            EditUser.edit_address(self.mock_user, "")

    def test_EditRole(self):
        EditUser.edit_role(self.mock_user, "Admin")
        self.assertEqual(self.mock_user.role, "Admin")

    def test_EditRoleInvalidEntry(self):
        with self.assertRaises(ValueError):
            EditUser.edit_role(self.mock_user, "InvalidRole")


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
            role="TA"
        )
        self.user.save()

    def test_EditFirstName(self):
        response = self.client.post('/configureUser.html', {'id': self.user.id, 'first_name': 'Jane'})
        self.user.refresh_from_db()
        self.assertEqual(self.user.first_name, "Jane")
        self.assertEqual(response.status_code, 200)

    def test_EditFirstNameInvalidEntry(self):
        response = self.client.post('/configureUser.html', {'id': self.user.id, 'first_name': ''})
        self.assertEqual(response.status_code, 400)

    def test_EditLastName(self):
        response = self.client.post('/configureUser.html', {'id': self.user.id, 'last_name': 'Smith'})
        self.user.refresh_from_db()
        self.assertEqual(self.user.last_name, "Smith")
        self.assertEqual(response.status_code, 200)

    def test_EditLastNameInvalidEntry(self):
        response = self.client.post('/configureUser.html', {'id': self.user.id, 'last_name': ''})
        self.assertEqual(response.status_code, 400)

    def test_EditEmail(self):
        response = self.client.post('/configureUser.html', {'id': self.user.id, 'email': 'janesmith@example.com'})
        self.user.refresh_from_db()
        self.assertEqual(self.user.email, "janesmith@example.com")
        self.assertEqual(response.status_code, 200)

    def test_EditEmailInvalidEntry(self):
        response = self.client.post('/configureUser.html', {'id': self.user.id, 'email': 'invalidemail'})
        self.assertEqual(response.status_code, 400)

    def test_EditPhone(self):
        response = self.client.post('/configureUser.html', {'id': self.user.id, 'phone': '1234567899'})
        self.user.refresh_from_db()
        self.assertEqual(self.user.phone_number, "1234567899")
        self.assertEqual(response.status_code, 200)

    def test_EditPhoneInvalidEntry(self):
        response = self.client.post('/configureUser.html', {'id': self.user.id, 'phone': 'invalid'})
        self.assertEqual(response.status_code, 400)

    def test_EditAddress(self):
        response = self.client.post('/configureUser.html', {'id': self.user.id, 'address': '124 Main St'})
        self.user.refresh_from_db()
        self.assertEqual(self.user.address, "123 Main St")
        self.assertEqual(response.status_code, 200)

    def test_EditAddressInvalidEntry(self):
        response = self.client.post('/configureUser.html', {'id': self.user.id, 'address': ''})
        self.assertEqual(response.status_code, 400)

    def test_EditRole(self):
        response = self.client.post('/configureUser.html', {'id': self.user.id, 'role': 'Admin'})
        self.user.refresh_from_db()
        self.assertEqual(self.user.role, "Admin")
        self.assertEqual(response.status_code, 200)

    def test_EditRoleInvalidEntry(self):
        response = self.client.post('/configureUser.html', {'id': self.user.id, 'role': 'InvalidRole'})
        self.assertEqual(response.status_code, 400)