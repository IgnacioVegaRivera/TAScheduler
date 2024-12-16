from django.test import TestCase, Client
from djangoProject1.models import User, Course, Section

class EditUserUnitTest(TestCase):
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
            role="TA"
        )
        self.user.save()

        self.course = Course(name="course 1")
        self.course.save()
        self.course.users.add(self.user)

        self.lab = Section(name="Lab 1", course=self.course, user=self.user)
        self.lab.save()

    #firstname tests
    def test_EditFirstName(self):
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

    def test_EditFirstNameBlankEntry(self):
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

    def test_EditFirstNameNumber(self):
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

    def test_EditFirstNameSpecial(self):
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

    #last name tests
    def test_EditLastName(self):
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

    def test_EditLastNameNumber(self):
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

    def test_EditLastNameSpecial(self):
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

    def test_EditLastNameBlankEntry(self):
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

    #email tests
    def test_EditEmail(self):
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

    def test_EditEmailBlankEntry(self):
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

    def test_EditEmailNoAt(self):
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

    def test_EditEmailNoPeriod(self):
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

    def test_EditPassword(self):
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

    def test_EditPasswordBlank(self):
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

    #phone tests
    def test_EditPhone(self):
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

    def test_EditPhoneInvalidEntry(self):
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

    def test_EditPhoneTooShort(self):
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

    def test_EditPhoneTooLong(self):
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

    #phonenumber is optional field
    def test_EditPhoneBlank(self):
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

    # address tests
    def test_EditAddress(self):
        response = self.client.post('/configure_user.html', {'id': self.user.id, 'first_name': 'John',
                                                                 "form_name": "edit_profile",
                                                                 'last_name': 'Doe',
                                                                 'email': 'janesmith@example.com',
                                                                 'password': 'password123',
                                                                 'phone_number': '1234567890',
                                                                 'address': '123 Elm Rd',
                                                                 'skills': 'not much'})
        self.user.refresh_from_db()
        self.assertEqual(self.user.address, "123 Elm Rd")

    # address is optional
    def test_EditAddressEmpty(self):
        response = self.client.post('/configure_user.html', {'id': self.user.id, 'first_name': 'John',
                                                                 "form_name": "edit_profile",
                                                                 'last_name': 'Doe',
                                                                 'email': 'janesmith@example.com',
                                                                 'password': 'password123',
                                                                 'phone_number': '1234567890',
                                                                 'address': '',
                                                                 'skills': 'not much'})
        self.user.refresh_from_db()
        self.assertEqual(self.user.address, "")

    def test_EditAddressNoNumber(self):
        response = self.client.post('/configure_user.html', {'id': self.user.id, 'first_name': 'John',
                                                                 "form_name": "edit_profile",
                                                                 'last_name': 'Doe',
                                                                 'email': 'janesmith@example.com',
                                                                 'password': 'password123',
                                                                 'phone_number': '1234567890',
                                                                 'address': 'Elm Rd',
                                                                 'skills': 'not much'})
        self.user.refresh_from_db()
        self.assertEqual(self.user.address, "123 Main St")

    def test_EditAddressNoLetters(self):
        response = self.client.post('/configure_user.html', {'id': self.user.id, 'first_name': 'John',
                                                                 "form_name": "edit_profile",
                                                                 'last_name': 'Doe',
                                                                 'email': 'janesmith@example.com',
                                                                 'password': 'password123',
                                                                 'phone_number': '1234567890',
                                                                 'address': '123',
                                                                 'skills': 'not much'})
        self.user.refresh_from_db()
        self.assertEqual(self.user.address, "123 Main St")

    def test_EditSkills(self):
        response = self.client.post('/configure_user.html', {'id': self.user.id, 'first_name': 'John',
                                                                 "form_name": "edit_profile",
                                                                 'last_name': 'Doe',
                                                                 'email': 'janesmith@example.com',
                                                                 'password': 'password123',
                                                                 'phone_number': '1234567890',
                                                                 'address': '123 Main St',
                                                                 'skills': 'What about the skills?'})
        self.user.refresh_from_db()
        self.assertEqual(self.user.skills, "What about the skills?")

    # skills is an optional field
    def test_EditSkillsEmpty(self):
        response = self.client.post('/configure_user.html', {'id': self.user.id, 'first_name': 'John',
                                                                 "form_name": "edit_profile",
                                                                 'last_name': 'Doe',
                                                                 'email': 'janesmith@example.com',
                                                                 'password': 'password123',
                                                                 'phone_number': '1234567890',
                                                                 'address': '123 Main St',
                                                                 'skills': ''})
        self.user.refresh_from_db()
        self.assertEqual(self.user.skills, "")