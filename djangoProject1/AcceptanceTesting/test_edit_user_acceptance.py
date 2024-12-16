from django.test import TestCase, Client

from djangoProject1.models import User

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
            role="Admin",
            skills="not much"
        )
        self.user.save()

    def test_EditFirstName(self):
        response = self.client.post('/configure_user.html', {'id': self.user.id, 'first_name': 'Jane',
                                                            "form_name": "edit_user",
                                                            'last_name': 'Doe',
                                                            'email': 'johndoe@example.com',
                                                            'username' : 'johndoe',
                                                            'phone_number': '1234567890',
                                                            'role': 'Admin',
                                                            'address': '123 Main St',
                                                            'skills': 'not much'})
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
                                                            'role': 'Admin',
                                                            'address': '123 Main St',
                                                            'skills': 'not much'})
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
                                                            'role': 'Admin',
                                                            'address': '123 Main St',
                                                            'skills': 'not much'})
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
                                                            'role': 'Admin',
                                                            'address': '123 Main St',
                                                            'skills': 'not much'})
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
                                                            'role': 'Admin',
                                                            'address': '123 Main St',
                                                            'skills': 'not much'})
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
                                                            'role': 'Admin',
                                                            'address': '123 Main St',
                                                            'skills': 'not much'})
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
                                                            'role': 'Admin',
                                                            'address': '123 Main St',
                                                            'skills': 'not much'})
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
                                                            'role': 'Admin',
                                                            'address': '123 Main St',
                                                            'skills': 'not much'})
        self.user.refresh_from_db()
        self.assertEqual(self.user.phone_number, "1234567890")
        self.assertEqual(User.objects.count(), 1)
        self.assertIn('message', response.context)
        self.assertEqual(response.context['message'], 'Something went wrong when updating the user')

    def test_EditPhoneBlankEntry(self):
        response = self.client.post('/configure_user.html',
                                    {'id': self.user.id, 'first_name': 'John',
                                                            "form_name": "edit_user",
                                                            'last_name': 'Doe',
                                                            'email': 'johndoe@example.com',
                                                            'username' : 'johndoe',
                                                            'phone_number': '',
                                                            'role': 'Admin',
                                                            'address': '123 Main St',
                                                            'skills': 'not much'})
        self.user.refresh_from_db()
        self.assertEqual(self.user.phone_number, "")
        self.assertEqual(User.objects.count(), 1)
        self.assertIn('message', response.context)
        self.assertEqual(response.context['message'], 'The user has been successfully updated')

    def test_EditRole(self):
        response = self.client.post('/configure_user.html',
                                    {'id': self.user.id, 'first_name': 'John',
                                                            "form_name": "edit_user",
                                                            'last_name': 'Doe',
                                                            'email': 'johndoe@example.com',
                                                            'username' : 'johndoe',
                                                            'phone_number': '1234567890',
                                                            'role': 'TA',
                                                            'address': '123 Main St',
                                                            'skills': 'not much'})
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
                                                            'role': 'Invalid',
                                                            'address': '123 Main St',
                                                            'skills': 'not much'})
        self.user.refresh_from_db()
        self.assertEqual(self.user.role, "Admin")
        self.assertEqual(User.objects.count(), 1)
        self.assertIn('message', response.context)
        self.assertEqual(response.context['message'], 'Something went wrong when updating the user')

    def test_EditAddress(self):
        response = self.client.post('/configure_user.html', {'id': self.user.id, 'first_name': 'John',
                                                             "form_name": "edit_user",
                                                             'last_name': 'Doe',
                                                             'email': 'johndoe@example.com',
                                                             'username': 'johndoe',
                                                             'phone_number': '1234567890',
                                                             'role': 'Admin',
                                                             'address': '123 Links Rd',
                                                             'skills': 'not much'})
        self.user.refresh_from_db()
        self.assertEqual(self.user.address, "123 Links Rd")
        self.assertEqual(User.objects.count(), 1)
        self.assertIn('message', response.context)
        self.assertEqual(response.context['message'], 'The user has been successfully updated')

    def test_EditAddressInvalid(self):
        response = self.client.post('/configure_user.html', {'id': self.user.id, 'first_name': 'John',
                                                             "form_name": "edit_user",
                                                             'last_name': 'Doe',
                                                             'email': 'johndoe@example.com',
                                                             'username': 'johndoe',
                                                             'phone_number': '1234567890',
                                                             'role': 'Admin',
                                                             'address': '123',
                                                             'skills': 'not much'})
        self.user.refresh_from_db()
        self.assertEqual(self.user.address, "123 Main St")
        self.assertEqual(User.objects.count(), 1)
        self.assertIn('message', response.context)
        self.assertEqual(response.context['message'], 'Something went wrong when updating the user')

    def test_EditSkills(self):
        response = self.client.post('/configure_user.html', {'id': self.user.id, 'first_name': 'John',
                                                             "form_name": "edit_user",
                                                             'last_name': 'Doe',
                                                             'email': 'johndoe@example.com',
                                                             'username': 'johndoe',
                                                             'phone_number': '1234567890',
                                                             'role': 'Admin',
                                                             'address': '123 Main St',
                                                             'skills': 'What about the skills?'})
        self.user.refresh_from_db()
        self.assertEqual(self.user.skills, "What about the skills?")
        self.assertEqual(User.objects.count(), 1)
        self.assertIn('message', response.context)
        self.assertEqual(response.context['message'], 'The user has been successfully updated')