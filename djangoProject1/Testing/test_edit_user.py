from django.test import TestCase, Client
import unittest

from djangoProject1.MethodFiles.Administrator import EditUser
from djangoProject1.models import User

class EditUserUnitTest(unittest.TestCase):
    def setUp(self):
        # Initialize the EditUser instance and mock User objects
        self.edit_user = EditUser()
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

    def test_EditFirstName(self):
        result = self.mock_user.edit_first_name(self.mock_user, "Jane")
        self.assertEqual(result.first_name, "Jane")

    def test_EditFirstNameInvalidEntry(self):
        with self.assertRaises(ValueError):
            self.edit_user.edit_first_name(self.mock_user, "")

    def test_EditLastName(self):
        result = self.edit_user.edit_last_name(self.mock_user, "Smith")
        self.assertEqual(result.last_name, "Smith")

    def test_EditLastNameInvalidEntry(self):
        with self.assertRaises(ValueError):
            self.edit_user.edit_last_name(self.mock_user, None)

    def test_EditUsername(self):
        result = self.edit_user.edit_username(self.mock_user, "janesmith")
        self.assertEqual(result.username, "janesmith")

    def test_EditUsernameInvalidEntry(self):
        with self.assertRaises(ValueError):
            self.edit_user.edit_username(self.mock_user, "a" * 51)

    def test_EditPassword(self):
        result = self.edit_user.edit_password(self.mock_user, "NewPassword123!")
        self.assertNotEqual(result.password, self.mock_user.password)

    def test_EditPasswordInvalidEntry(self):
        with self.assertRaises(ValueError):
            self.edit_user.edit_password(self.mock_user, "123")

    def test_EditEmail(self):
        result = self.edit_user.edit_email(self.mock_user, "janesmith@example.com")
        self.assertEqual(result.email, "janesmith@example.com")

    def test_EditEmailInvalidEntry(self):
        with self.assertRaises(ValueError):
            self.edit_user.edit_email(self.mock_user, "invalidemail")

    def test_EditPhone(self):
        result = self.edit_user.edit_phone(self.mock_user, "9876543210")
        self.assertEqual(result.phone_number, "9876543210")

    def test_EditPhoneInvalidEntry(self):
        with self.assertRaises(ValueError):
            self.edit_user.edit_phone(self.mock_user, "invalid")

    def test_EditAddress(self):
        result = self.edit_user.edit_address(self.mock_user, "456 Another St")
        self.assertEqual(result.address, "456 Another St")

    def test_EditAddressInvalidEntry(self):
        with self.assertRaises(ValueError):
            self.edit_user.edit_address(self.mock_user, "")

    def test_EditRole(self):
        result = self.edit_user.edit_role(self.mock_user, "Admin")
        self.assertEqual(result.role, "Admin")

    def test_EditRoleInvalidEntry(self):
        with self.assertRaises(ValueError):
            self.edit_user.edit_role(self.mock_user, "InvalidRole")


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

    def test_EditFirstName(self):
        response = self.client.post('/edit_user/', {'id': self.user.id, 'first_name': 'Jane'})
        self.user.refresh_from_db()
        self.assertEqual(self.user.first_name, "Jane")
        self.assertEqual(response.status_code, 200)

    def test_EditFirstNameInvalidEntry(self):
        response = self.client.post('/edit_user/', {'id': self.user.id, 'first_name': ''})
        self.assertEqual(response.status_code, 400)

    def test_EditLastName(self):
        response = self.client.post('/edit_user/', {'id': self.user.id, 'last_name': 'Smith'})
        self.user.refresh_from_db()
        self.assertEqual(self.user.last_name, "Smith")
        self.assertEqual(response.status_code, 200)

    def test_EditLastNameInvalidEntry(self):
        response = self.client.post('/edit_user/', {'id': self.user.id, 'last_name': ''})
        self.assertEqual(response.status_code, 400)

    def test_EditEmail(self):
        response = self.client.post('/edit_user/', {'id': self.user.id, 'email': 'janesmith@example.com'})
        self.user.refresh_from_db()
        self.assertEqual(self.user.email, "janesmith@example.com")
        self.assertEqual(response.status_code, 200)

    def test_EditEmailInvalidEntry(self):
        response = self.client.post('/edit_user/', {'id': self.user.id, 'email': 'invalidemail'})
        self.assertEqual(response.status_code, 400)

    def test_EditPhone(self):
        response = self.client.post('/edit_user/', {'id': self.user.id, 'phone': '1234567899'})
        self.user.refresh_from_db()
        self.assertEqual(self.user.phone_number, "1234567899")
        self.assertEqual(response.status_code, 200)

    def test_EditPhoneInvalidEntry(self):
        response = self.client.post('/edit_user/', {'id': self.user.id, 'phone': 'invalid'})
        self.assertEqual(response.status_code, 400)

    def test_EditAddress(self):
        response = self.client.post('/edit_user/', {'id': self.user.id, 'address': '124 Main St'})
        self.user.refresh_from_db()
        self.assertEqual(self.user.address, "123 Main St")
        self.assertEqual(response.status_code, 200)

    def test_EditAddressInvalidEntry(self):
        response = self.client.post('/edit_user/', {'id': self.user.id, 'address': ''})
        self.assertEqual(response.status_code, 400)

    def test_EditRole(self):
        response = self.client.post('/edit_user/', {'id': self.user.id, 'role': 'Admin'})
        self.user.refresh_from_db()
        self.assertEqual(self.user.role, "Admin")
        self.assertEqual(response.status_code, 200)

    def test_EditRoleInvalidEntry(self):
        response = self.client.post('/edit_user/', {'id': self.user.id, 'role': 'InvalidRole'})
        self.assertEqual(response.status_code, 400)