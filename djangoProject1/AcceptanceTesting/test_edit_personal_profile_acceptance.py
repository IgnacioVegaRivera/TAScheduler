from django.test import TestCase, Client
from djangoProject1.models import User, Course, Section

class TestEditPersonalProfileAcceptance(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User(
            first_name="John",
            last_name="Doe",
            username="johndoe",
            password="password123",
            email="johndoe@example.com",
            phone_number="1234567890",
            address="123 Main St",
            skills="not much",
            role="TA"
        )
        self.user.save()

    def login_as_user(self):
        self.client.post('/', {'username': 'johndoe', 'password': 'password123'})

    def test_EditFirstName(self):
        self.login_as_user()
        response = self.client.post('/profile_page.html', {'id': self.user.id, 'first_name': 'Jane',
                                                            "form_name": "edit_profile",
                                                            'last_name': 'Doe',
                                                            'email': 'johndoe@example.com',
                                                            'password': 'password123',
                                                            'phone_number': '1234567890',
                                                            'address': '123 Main St',
                                                            'skills': 'not much'})
        self.user.refresh_from_db()
        self.assertEqual(self.user.first_name, "Jane")
        self.assertEqual(User.objects.count(), 1)
        self.assertIn('message', response.context)
        self.assertEqual(response.context['message'], 'Your information has been successfully updated')

    def test_EditFirstNameBlankEntry(self):
        self.login_as_user()
        response = self.client.post('/profile_page.html', {'id': self.user.id, 'first_name': '',
                                                            "form_name": "edit_profile",
                                                            'last_name': 'Doe',
                                                            'email': 'johndoe@example.com',
                                                            'password': 'password123',
                                                            'phone_number': '1234567890',
                                                            'address': '123 Main St',
                                                            'skills': 'not much'})
        self.user.refresh_from_db()
        self.assertEqual(self.user.first_name, "John")
        self.assertEqual(User.objects.count(), 1)
        self.assertIn('message', response.context)
        self.assertEqual(response.context['message'],
                         'Something went wrong when updating your info')

    def test_EditFirstNameNumber(self):
        self.login_as_user()
        response = self.client.post('/profile_page.html', {'id': self.user.id, 'first_name': '123',
                                                            "form_name": "edit_profile",
                                                            'last_name': 'Doe',
                                                            'email': 'johndoe@example.com',
                                                            'password': 'password123',
                                                            'phone_number': '1234567890',
                                                            'address': '123 Main St',
                                                            'skills': 'not much'})
        self.user.refresh_from_db()
        self.assertEqual(self.user.first_name, "John")
        self.assertEqual(User.objects.count(), 1)
        self.assertIn('message', response.context)
        self.assertEqual(response.context['message'],
                         'Something went wrong when updating your info')

    def test_EditFirstNameSpecial(self):
        self.login_as_user()
        response = self.client.post('/profile_page.html', {'id': self.user.id, 'first_name': '[Jane]',
                                                            "form_name": "edit_profile",
                                                            'last_name': 'Doe',
                                                            'email': 'johndoe@example.com',
                                                            'password': 'password123',
                                                            'phone_number': '1234567890',
                                                            'address': '123 Main St',
                                                            'skills': 'not much'})
        self.user.refresh_from_db()
        self.assertEqual(self.user.first_name, "John")
        self.assertEqual(User.objects.count(), 1)
        self.assertIn('message', response.context)
        self.assertEqual(response.context['message'],
                         'Something went wrong when updating your info')

    #last name tests
    def test_EditLastName(self):
        self.login_as_user()
        response = self.client.post('/profile_page.html', {'id': self.user.id, 'first_name': 'John',
                                                            "form_name": "edit_profile",
                                                            'last_name': 'Smith',
                                                            'email': 'johndoe@example.com',
                                                            'password': 'password123',
                                                            'phone_number': '1234567890',
                                                            'address': '123 Main St',
                                                            'skills': 'not much'})
        self.user.refresh_from_db()
        self.assertEqual(self.user.last_name, "Smith")
        self.assertEqual(User.objects.count(), 1)
        self.assertIn('message', response.context)
        self.assertEqual(response.context['message'], 'Your information has been successfully updated')

    def test_EditLastNameNumber(self):
        self.login_as_user()
        response = self.client.post('/profile_page.html', {'id': self.user.id, 'first_name': 'John',
                                                            "form_name": "edit_profile",
                                                            'last_name': '456',
                                                            'email': 'johndoe@example.com',
                                                            'password': 'password123',
                                                            'phone_number': '1234567890',
                                                            'address': '123 Main St',
                                                            'skills': 'not much'})
        self.user.refresh_from_db()
        self.assertEqual(self.user.last_name, "Doe")
        self.assertEqual(User.objects.count(), 1)
        self.assertIn('message', response.context)
        self.assertEqual(response.context['message'],
                         'Something went wrong when updating your info')

    def test_EditLastNameSpecial(self):
        self.login_as_user()
        response = self.client.post('/profile_page.html', {'id': self.user.id, 'first_name': 'John',
                                                            "form_name": "edit_profile",
                                                            'last_name': '[Doe]',
                                                            'email': 'johndoe@example.com',
                                                            'password': 'password123',
                                                            'phone_number': '1234567890',
                                                            'address': '123 Main St',
                                                            'skills': 'not much'})
        self.user.refresh_from_db()
        self.assertEqual(self.user.last_name, "Doe")
        self.assertEqual(User.objects.count(), 1)
        self.assertIn('message', response.context)
        self.assertEqual(response.context['message'],
                         'Something went wrong when updating your info')

    def test_EditLastNameBlankEntry(self):
        self.login_as_user()
        response = self.client.post('/profile_page.html', {'id': self.user.id, 'first_name': 'John',
                                                            "form_name": "edit_profile",
                                                            'last_name': '',
                                                            'email': 'johndoe@example.com',
                                                            'password': 'password123',
                                                            'phone_number': '1234567890',
                                                            'address': '123 Main St',
                                                            'skills': 'not much'})
        self.user.refresh_from_db()
        self.assertEqual(self.user.last_name, "Doe")
        self.assertEqual(User.objects.count(), 1)
        self.assertIn('message', response.context)
        self.assertEqual(response.context['message'],
                         'Something went wrong when updating your info')

    #email tests
    def test_EditEmail(self):
        self.login_as_user()
        response = self.client.post('/profile_page.html', {'id': self.user.id, 'first_name': 'John',
                                                            "form_name": "edit_profile",
                                                            'last_name': 'Doe',
                                                            'email': 'janesmith@example.com',
                                                            'password': 'password123',
                                                            'phone_number': '1234567890',
                                                            'address': '123 Main St',
                                                            'skills': 'not much'})
        self.user.refresh_from_db()
        self.assertEqual(self.user.email, "janesmith@example.com")
        self.assertEqual(User.objects.count(), 1)
        self.assertIn('message', response.context)
        self.assertEqual(response.context['message'], 'Your information has been successfully updated')

    def test_EditEmailBlankEntry(self):
        self.login_as_user()
        response = self.client.post('/profile_page.html', {'id': self.user.id, 'first_name': 'John',
                                                            "form_name": "edit_profile",
                                                            'last_name': 'Doe',
                                                            'email': '',
                                                            'password': 'password123',
                                                            'phone_number': '1234567890',
                                                            'address': '123 Main St',
                                                            'skills': 'not much'})
        self.user.refresh_from_db()
        self.assertEqual(self.user.email, "johndoe@example.com")
        self.assertEqual(User.objects.count(), 1)
        self.assertIn('message', response.context)
        self.assertEqual(response.context['message'],
                         'Something went wrong when updating your info')

    def test_EditEmailNoAt(self):
        self.login_as_user()
        response = self.client.post('/profile_page.html', {'id': self.user.id, 'first_name': 'John',
                                                            "form_name": "edit_profile",
                                                            'last_name': 'Doe',
                                                            'email': 'janesmithexample.com',
                                                            'password': 'password123',
                                                            'phone_number': '1234567890',
                                                            'address': '123 Main St',
                                                            'skills': 'not much'})
        self.user.refresh_from_db()
        self.assertEqual(self.user.email, "johndoe@example.com")
        self.assertEqual(User.objects.count(), 1)
        self.assertIn('message', response.context)
        self.assertEqual(response.context['message'],
                         'Something went wrong when updating your info')

    def test_EditEmailNoPeriod(self):
        self.login_as_user()
        response = self.client.post('/profile_page.html', {'id': self.user.id, 'first_name': 'John',
                                                            "form_name": "edit_profile",
                                                            'last_name': 'Doe',
                                                            'email': 'janesmith@examplecom',
                                                            'password': 'password123',
                                                            'phone_number': '1234567890',
                                                            'address': '123 Main St',
                                                            'skills': 'not much'})
        self.user.refresh_from_db()
        self.assertEqual(self.user.email, "johndoe@example.com")
        self.assertEqual(User.objects.count(), 1)
        self.assertIn('message', response.context)
        self.assertEqual(response.context['message'],
                         'Something went wrong when updating your info')

    def test_EditPassword(self):
        self.login_as_user()
        response = self.client.post('/profile_page.html', {'id': self.user.id, 'first_name': 'John',
                                                           "form_name": "edit_profile",
                                                           'last_name': 'Smith',
                                                           'email': 'johndoe@example.com',
                                                           'password': 'password772',
                                                           'phone_number': '1234567890',
                                                           'address': '123 Main St',
                                                           'skills': 'not much'})
        self.user.refresh_from_db()
        self.assertEqual(self.user.password, "password772")
        self.assertEqual(User.objects.count(), 1)
        self.assertIn('message', response.context)
        self.assertEqual(response.context['message'], 'Your information has been successfully updated')

    def test_EditPasswordBlank(self):
        self.login_as_user()
        response = self.client.post('/profile_page.html', {'id': self.user.id, 'first_name': 'John',
                                                           "form_name": "edit_profile",
                                                           'last_name': 'Smith',
                                                           'email': 'johndoe@example.com',
                                                           'password': '',
                                                           'phone_number': '1234567890',
                                                           'address': '123 Main St',
                                                           'skills': 'not much'})
        self.user.refresh_from_db()
        self.assertEqual(self.user.password, "password123")
        self.assertEqual(User.objects.count(), 1)
        self.assertIn('message', response.context)
        self.assertEqual(response.context['message'],
                         'Something went wrong when updating your info')

    #phone tests
    def test_EditPhone(self):
        self.login_as_user()
        response = self.client.post('/profile_page.html', {'id': self.user.id, 'first_name': 'John',
                                                            "form_name": "edit_profile",
                                                            'last_name': 'Doe',
                                                            'email': 'janesmith@example.com',
                                                            'password': 'password123',
                                                            'phone_number': '1234567899',
                                                            'address': '123 Main St',
                                                            'skills': 'not much'})
        self.user.refresh_from_db()
        self.assertEqual(self.user.phone_number, "1234567899")
        self.assertEqual(User.objects.count(), 1)
        self.assertIn('message', response.context)
        self.assertEqual(response.context['message'], 'Your information has been successfully updated')

    def test_EditPhoneInvalidEntry(self):
        self.login_as_user()
        response = self.client.post('/profile_page.html', {'id': self.user.id, 'first_name': 'John',
                                                            "form_name": "edit_profile",
                                                            'last_name': 'Doe',
                                                            'email': 'janesmith@example.com',
                                                            'password': 'password123',
                                                            'phone_number': 'invalidate',
                                                            'address': '123 Main St',
                                                            'skills': 'not much'})
        self.user.refresh_from_db()
        self.assertEqual(self.user.phone_number, "1234567890")
        self.assertEqual(User.objects.count(), 1)
        self.assertIn('message', response.context)
        self.assertEqual(response.context['message'],
                         'Something went wrong when updating your info')

    def test_EditPhoneTooShort(self):
        self.login_as_user()
        response = self.client.post('/profile_page.html', {'id': self.user.id, 'first_name': 'John',
                                                            "form_name": "edit_profile",
                                                            'last_name': 'Doe',
                                                            'email': 'janesmith@example.com',
                                                            'password': 'password123',
                                                            'phone_number': '12345',
                                                            'address': '123 Main St',
                                                            'skills': 'not much'})
        self.user.refresh_from_db()
        self.assertEqual(self.user.phone_number, "1234567890")
        self.assertEqual(User.objects.count(), 1)
        self.assertIn('message', response.context)
        self.assertEqual(response.context['message'],
                         'Something went wrong when updating your info')

    def test_EditPhoneTooLong(self):
        self.login_as_user()
        response = self.client.post('/profile_page.html', {'id': self.user.id, 'first_name': 'John',
                                                            "form_name": "edit_profile",
                                                            'last_name': 'Doe',
                                                            'email': 'janesmith@example.com',
                                                            'password': 'password123',
                                                            'phone_number': '1234567890123',
                                                            'address': '123 Main St',
                                                            'skills': 'not much'})
        self.user.refresh_from_db()
        self.assertEqual(self.user.phone_number, "1234567890")
        self.assertEqual(User.objects.count(), 1)
        self.assertIn('message', response.context)
        self.assertEqual(response.context['message'],
                         'Something went wrong when updating your info')

    #phonenumber is optional field
    def test_EditPhoneBlank(self):
        self.login_as_user()
        response = self.client.post('/profile_page.html', {'id': self.user.id, 'first_name': 'John',
                                                            "form_name": "edit_profile",
                                                            'last_name': 'Doe',
                                                            'email': 'janesmith@example.com',
                                                            'password': 'password123',
                                                            'phone_number': '',
                                                            'address': '123 Main St',
                                                            'skills': 'not much'})
        self.user.refresh_from_db()
        self.assertEqual(self.user.phone_number, "")
        self.assertEqual(User.objects.count(), 1)
        self.assertIn('message', response.context)
        self.assertEqual(response.context['message'], 'Your information has been successfully updated')

    # address tests
    def test_EditAddress(self):
        self.login_as_user()
        response = self.client.post('/profile_page.html', {'id': self.user.id, 'first_name': 'John',
                                                                 "form_name": "edit_profile",
                                                                 'last_name': 'Doe',
                                                                 'email': 'janesmith@example.com',
                                                                 'password': 'password123',
                                                                 'phone_number': '1234567890',
                                                                 'address': '123 Elm Rd',
                                                                 'skills': 'not much'})
        self.user.refresh_from_db()
        self.assertEqual(self.user.address, "123 Elm Rd")
        self.assertEqual(User.objects.count(), 1)
        self.assertIn('message', response.context)
        self.assertEqual(response.context['message'], 'Your information has been successfully updated')

    # address is optional
    def test_EditAddressEmpty(self):
        self.login_as_user()
        response = self.client.post('/profile_page.html', {'id': self.user.id, 'first_name': 'John',
                                                                 "form_name": "edit_profile",
                                                                 'last_name': 'Doe',
                                                                 'email': 'janesmith@example.com',
                                                                 'password': 'password123',
                                                                 'phone_number': '1234567890',
                                                                 'address': '',
                                                                 'skills': 'not much'})
        self.user.refresh_from_db()
        self.assertEqual(self.user.address, "")
        self.assertEqual(User.objects.count(), 1)
        self.assertIn('message', response.context)
        self.assertEqual(response.context['message'], 'Your information has been successfully updated')

    def test_EditAddressNoNumber(self):
        self.login_as_user()
        response = self.client.post('/profile_page.html', {'id': self.user.id, 'first_name': 'John',
                                                                 "form_name": "edit_profile",
                                                                 'last_name': 'Doe',
                                                                 'email': 'janesmith@example.com',
                                                                 'password': 'password123',
                                                                 'phone_number': '1234567890',
                                                                 'address': 'Elm Rd',
                                                                 'skills': 'not much'})
        self.user.refresh_from_db()
        self.assertEqual(self.user.address, "123 Main St")
        self.assertEqual(User.objects.count(), 1)
        self.assertIn('message', response.context)
        self.assertEqual(response.context['message'],
                         'Something went wrong when updating your info')

    def test_EditAddressNoLetters(self):
        self.login_as_user()
        response = self.client.post('/profile_page.html', {'id': self.user.id, 'first_name': 'John',
                                                                 "form_name": "edit_profile",
                                                                 'last_name': 'Doe',
                                                                 'email': 'janesmith@example.com',
                                                                 'password': 'password123',
                                                                 'phone_number': '1234567890',
                                                                 'address': '123',
                                                                 'skills': 'not much'})
        self.user.refresh_from_db()
        self.assertEqual(self.user.address, "123 Main St")
        self.assertEqual(User.objects.count(), 1)
        self.assertIn('message', response.context)
        self.assertEqual(response.context['message'],
                         'Something went wrong when updating your info')

    def test_EditSkills(self):
        self.login_as_user()
        response = self.client.post('/profile_page.html', {'id': self.user.id, 'first_name': 'John',
                                                                 "form_name": "edit_profile",
                                                                 'last_name': 'Doe',
                                                                 'email': 'janesmith@example.com',
                                                                 'password': 'password123',
                                                                 'phone_number': '1234567890',
                                                                 'address': '123 Main St',
                                                                 'skills': 'What about the skills?'})
        self.user.refresh_from_db()
        self.assertEqual(self.user.skills, "What about the skills?")
        self.assertEqual(User.objects.count(), 1)
        self.assertIn('message', response.context)
        self.assertEqual(response.context['message'], 'Your information has been successfully updated')

    # skills is an optional field
    def test_EditSkillsEmpty(self):
        self.login_as_user()
        response = self.client.post('/profile_page.html', {'id': self.user.id, 'first_name': 'John',
                                                                 "form_name": "edit_profile",
                                                                 'last_name': 'Doe',
                                                                 'email': 'janesmith@example.com',
                                                                 'password': 'password123',
                                                                 'phone_number': '1234567890',
                                                                 'address': '123 Main St',
                                                                 'skills': ''})
        self.user.refresh_from_db()
        self.assertEqual(self.user.skills, "")
        self.assertEqual(User.objects.count(), 1)
        self.assertIn('message', response.context)
        self.assertEqual(response.context['message'], 'Your information has been successfully updated')


