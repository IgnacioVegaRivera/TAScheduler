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
        response = self.client.post('/configure_user.html', {'id': self.user.id, 'first_name': 'Jane',
                                                            "form_name": "edit_user",
                                                            'last_name': 'Doe',
                                                            'email': 'johndoe@example.com',
                                                            'username': 'johndoe',
                                                            'phone_number': '1234567890',
                                                            'role': 'TA',
                                                            'address': '123 Main St',
                                                            'skills': 'not much'})
        self.user.refresh_from_db()
        self.assertEqual(self.user.first_name, "Jane")

    def test_EditFirstNameBlankEntry(self):
        response = self.client.post('/configure_user.html', {'id': self.user.id, 'first_name': '',
                                                            "form_name": "edit_user",
                                                            'last_name': 'Doe',
                                                            'email': 'johndoe@example.com',
                                                            'username': 'johndoe',
                                                            'phone_number': '1234567890',
                                                            'role': 'TA',
                                                            'address': '123 Main St',
                                                            'skills': 'not much'})
        self.user.refresh_from_db()
        self.assertEqual(self.user.first_name, "John")

    def test_EditFirstNameNumber(self):
        response = self.client.post('/configure_user.html', {'id': self.user.id, 'first_name': '123',
                                                            "form_name": "edit_user",
                                                            'last_name': 'Doe',
                                                            'email': 'johndoe@example.com',
                                                            'username': 'johndoe',
                                                            'phone_number': '1234567890',
                                                            'role': 'TA',
                                                            'address': '123 Main St',
                                                            'skills': 'not much'})
        self.user.refresh_from_db()
        self.assertEqual(self.user.first_name, "John")

    def test_EditFirstNameSpecial(self):
        response = self.client.post('/configure_user.html', {'id': self.user.id, 'first_name': '[Jane]',
                                                            "form_name": "edit_user",
                                                            'last_name': 'Doe',
                                                            'email': 'johndoe@example.com',
                                                            'username': 'johndoe',
                                                            'phone_number': '1234567890',
                                                            'role': 'TA',
                                                            'address': '123 Main St',
                                                            'skills': 'not much'})
        self.user.refresh_from_db()
        self.assertEqual(self.user.first_name, "John")

    #last name tests
    def test_EditLastName(self):
        response = self.client.post('/configure_user.html', {'id': self.user.id, 'first_name': 'John',
                                                            "form_name": "edit_user",
                                                            'last_name': 'Smith',
                                                            'email': 'johndoe@example.com',
                                                            'username': 'johndoe',
                                                            'phone_number': '1234567890',
                                                            'role': 'TA',
                                                            'address': '123 Main St',
                                                            'skills': 'not much'})
        self.user.refresh_from_db()
        self.assertEqual(self.user.last_name, "Smith")

    def test_EditLastNameNumber(self):
        response = self.client.post('/configure_user.html', {'id': self.user.id, 'first_name': 'John',
                                                            "form_name": "edit_user",
                                                            'last_name': '456',
                                                            'email': 'johndoe@example.com',
                                                            'username': 'johndoe',
                                                            'phone_number': '1234567890',
                                                            'role': 'TA',
                                                            'address': '123 Main St',
                                                            'skills': 'not much'})
        self.user.refresh_from_db()
        self.assertEqual(self.user.last_name, "Doe")

    def test_EditLastNameSpecial(self):
        response = self.client.post('/configure_user.html', {'id': self.user.id, 'first_name': 'John',
                                                            "form_name": "edit_user",
                                                            'last_name': '[Doe]',
                                                            'email': 'johndoe@example.com',
                                                            'username': 'johndoe',
                                                            'phone_number': '1234567890',
                                                            'role': 'TA',
                                                            'address': '123 Main St',
                                                            'skills': 'not much'})
        self.user.refresh_from_db()
        self.assertEqual(self.user.last_name, "Doe")

    def test_EditLastNameBlankEntry(self):
        response = self.client.post('/configure_user.html', {'id': self.user.id, 'first_name': 'John',
                                                            "form_name": "edit_user",
                                                            'last_name': '',
                                                            'email': 'johndoe@example.com',
                                                            'username': 'johndoe',
                                                            'phone_number': '1234567890',
                                                            'role': 'TA',
                                                            'address': '123 Main St',
                                                            'skills': 'not much'})
        self.user.refresh_from_db()
        self.assertEqual(self.user.last_name, "Doe")

    #email tests
    def test_EditEmail(self):
        response = self.client.post('/configure_user.html', {'id': self.user.id, 'first_name': 'John',
                                                            "form_name": "edit_user",
                                                            'last_name': 'Doe',
                                                            'email': 'janesmith@example.com',
                                                            'username': 'johndoe',
                                                            'phone_number': '1234567890',
                                                            'role': 'TA',
                                                            'address': '123 Main St',
                                                            'skills': 'not much'})
        self.user.refresh_from_db()
        self.assertEqual(self.user.email, "janesmith@example.com")

    def test_EditEmailBlankEntry(self):
        response = self.client.post('/configure_user.html', {'id': self.user.id, 'first_name': 'John',
                                                            "form_name": "edit_user",
                                                            'last_name': 'Doe',
                                                            'email': '',
                                                            'username': 'johndoe',
                                                            'phone_number': '1234567890',
                                                            'role': 'TA',
                                                            'address': '123 Main St',
                                                            'skills': 'not much'})
        self.user.refresh_from_db()
        self.assertEqual(self.user.email, "johndoe@example.com")

    def test_EditEmailNoAt(self):
        response = self.client.post('/configure_user.html', {'id': self.user.id, 'first_name': 'John',
                                                            "form_name": "edit_user",
                                                            'last_name': 'Doe',
                                                            'email': 'janesmithexample.com',
                                                            'username': 'johndoe',
                                                            'phone_number': '1234567890',
                                                            'role': 'TA',
                                                            'address': '123 Main St',
                                                            'skills': 'not much'})
        self.user.refresh_from_db()
        self.assertEqual(self.user.email, "johndoe@example.com")

    def test_EditEmailNoPeriod(self):
        response = self.client.post('/configure_user.html', {'id': self.user.id, 'first_name': 'John',
                                                            "form_name": "edit_user",
                                                            'last_name': 'Doe',
                                                            'email': 'janesmith@examplecom',
                                                            'username': 'johndoe',
                                                            'phone_number': '1234567890',
                                                            'role': 'TA',
                                                            'address': '123 Main St',
                                                            'skills': 'not much'})
        self.user.refresh_from_db()
        self.assertEqual(self.user.email, "johndoe@example.com")

    #phone tests
    def test_EditPhone(self):
        response = self.client.post('/configure_user.html', {'id': self.user.id, 'first_name': 'John',
                                                            "form_name": "edit_user",
                                                            'last_name': 'Doe',
                                                            'email': 'janesmith@example.com',
                                                            'username': 'johndoe',
                                                            'phone_number': '1234567899',
                                                            'role': 'TA',
                                                            'address': '123 Main St',
                                                            'skills': 'not much'})
        self.user.refresh_from_db()
        self.assertEqual(self.user.phone_number, "1234567899")

    def test_EditPhoneInvalidEntry(self):
        response = self.client.post('/configure_user.html', {'id': self.user.id, 'first_name': 'John',
                                                            "form_name": "edit_user",
                                                            'last_name': 'Doe',
                                                            'email': 'janesmith@example.com',
                                                            'username': 'johndoe',
                                                            'phone_number': 'invalidate',
                                                            'role': 'TA',
                                                            'address': '123 Main St',
                                                            'skills': 'not much'})
        self.user.refresh_from_db()
        self.assertEqual(self.user.phone_number, "1234567890")

    def test_EditPhoneTooShort(self):
        response = self.client.post('/configure_user.html', {'id': self.user.id, 'first_name': 'John',
                                                            "form_name": "edit_user",
                                                            'last_name': 'Doe',
                                                            'email': 'janesmith@example.com',
                                                            'username': 'johndoe',
                                                            'phone_number': '12345',
                                                            'role': 'TA',
                                                            'address': '123 Main St',
                                                            'skills': 'not much'})
        self.user.refresh_from_db()
        self.assertEqual(self.user.phone_number, "1234567890")

    def test_EditPhoneTooLong(self):
        response = self.client.post('/configure_user.html', {'id': self.user.id, 'first_name': 'John',
                                                            "form_name": "edit_user",
                                                            'last_name': 'Doe',
                                                            'email': 'janesmith@example.com',
                                                            'username': 'johndoe',
                                                            'phone_number': '1234567890123',
                                                            'role': 'TA',
                                                            'address': '123 Main St',
                                                            'skills': 'not much'})
        self.user.refresh_from_db()
        self.assertEqual(self.user.phone_number, "1234567890")

    #phonenumber is optional field
    def test_EditPhoneBlank(self):
        response = self.client.post('/configure_user.html', {'id': self.user.id, 'first_name': 'John',
                                                            "form_name": "edit_user",
                                                            'last_name': 'Doe',
                                                            'email': 'janesmith@example.com',
                                                            'username': 'johndoe',
                                                            'phone_number': '',
                                                            'role': 'TA',
                                                            'address': '123 Main St',
                                                            'skills': 'not much'})
        self.user.refresh_from_db()
        self.assertEqual(self.user.phone_number, "")

    #role tests
    def test_MakeIntoInstructor(self):
        response = self.client.post('/configure_user.html', {'id': self.user.id, 'first_name': 'John',
                                                            "form_name": "edit_user",
                                                            'last_name': 'Doe',
                                                            'email': 'janesmith@example.com',
                                                            'username': 'johndoe',
                                                            'phone_number': '1234567890',
                                                            'role': 'Instructor',
                                                            'address': '123 Main St',
                                                            'skills': 'not much'})
        self.user.refresh_from_db()
        self.course.refresh_from_db()
        self.lab.refresh_from_db()
        self.assertEqual(self.user.role, "Instructor")
        #ta to instructor and vice versa removes the user from their sections, not their courses
        self.assertEqual(self.course.users.count(), 1)
        self.assertEqual(self.lab.user, None)

    def test_MakeIntoAdmin(self):
        response = self.client.post('/configure_user.html', {'id': self.user.id, 'first_name': 'John',
                                                             "form_name": "edit_user",
                                                             'last_name': 'Doe',
                                                             'email': 'janesmith@example.com',
                                                             'username': 'johndoe',
                                                             'phone_number': '1234567890',
                                                             'role': 'Admin',
                                                             'address': '123 Main St',
                                                             'skills': 'not much'})
        self.user.refresh_from_db()
        self.course.refresh_from_db()
        self.lab.refresh_from_db()
        self.assertEqual(self.user.role, "Admin")
        # when a user is made into an admin then they are no longer assigned to any courses or sections
        self.assertEqual(self.course.users.count(), 0)
        self.assertEqual(self.lab.user, None)

    def test_EditRoleInvalidEntry(self):
        response = self.client.post('/configure_user.html', {'id': self.user.id, 'first_name': 'John',
                                                            "form_name": "edit_user",
                                                            'last_name': 'Doe',
                                                            'email': 'janesmith@example.com',
                                                            'username': 'johndoe',
                                                            'phone_number': '1234567890',
                                                            'role': 'Invalid',
                                                            'address': '123 Main St',
                                                            'skills': 'not much'})
        self.user.refresh_from_db()
        self.assertEqual(self.user.role, "TA")

    #address tests
    def test_EditAddress(self):
        response = self.client.post('/configure_user.html', {'id': self.user.id, 'first_name': 'John',
                                                             "form_name": "edit_user",
                                                             'last_name': 'Doe',
                                                             'email': 'janesmith@example.com',
                                                             'username': 'johndoe',
                                                             'phone_number': '1234567890',
                                                             'role': 'TA',
                                                             'address': '123 Elm Rd',
                                                             'skills': 'not much'})
        self.user.refresh_from_db()
        self.assertEqual(self.user.address, "123 Elm Rd")

    #address is optional
    def test_EditAddressEmpty(self):
        response = self.client.post('/configure_user.html', {'id': self.user.id, 'first_name': 'John',
                                                             "form_name": "edit_user",
                                                             'last_name': 'Doe',
                                                             'email': 'janesmith@example.com',
                                                             'username': 'johndoe',
                                                             'phone_number': '1234567890',
                                                             'role': 'TA',
                                                             'address': '',
                                                             'skills': 'not much'})
        self.user.refresh_from_db()
        self.assertEqual(self.user.address, "")

    def test_EditAddressNoNumber(self):
        response = self.client.post('/configure_user.html', {'id': self.user.id, 'first_name': 'John',
                                                             "form_name": "edit_user",
                                                             'last_name': 'Doe',
                                                             'email': 'janesmith@example.com',
                                                             'username': 'johndoe',
                                                             'phone_number': '1234567890',
                                                             'role': 'TA',
                                                             'address': 'Elm Rd',
                                                             'skills': 'not much'})
        self.user.refresh_from_db()
        self.assertEqual(self.user.address, "123 Main St")

    def test_EditAddressNoLetters(self):
        response = self.client.post('/configure_user.html', {'id': self.user.id, 'first_name': 'John',
                                                             "form_name": "edit_user",
                                                             'last_name': 'Doe',
                                                             'email': 'janesmith@example.com',
                                                             'username': 'johndoe',
                                                             'phone_number': '1234567890',
                                                             'role': 'TA',
                                                             'address': '123',
                                                             'skills': 'not much'})
        self.user.refresh_from_db()
        self.assertEqual(self.user.address, "123 Main St")

    def test_EditSkills(self):
        response = self.client.post('/configure_user.html', {'id': self.user.id, 'first_name': 'John',
                                                             "form_name": "edit_user",
                                                             'last_name': 'Doe',
                                                             'email': 'janesmith@example.com',
                                                             'username': 'johndoe',
                                                             'phone_number': '1234567890',
                                                             'role': 'TA',
                                                             'address': '123 Main St',
                                                             'skills': 'What about the skills?'})
        self.user.refresh_from_db()
        self.assertEqual(self.user.skills, "What about the skills?")

    #skills is an optional field
    def test_EditSkillsEmpty(self):
        response = self.client.post('/configure_user.html', {'id': self.user.id, 'first_name': 'John',
                                                             "form_name": "edit_user",
                                                             'last_name': 'Doe',
                                                             'email': 'janesmith@example.com',
                                                             'username': 'johndoe',
                                                             'phone_number': '1234567890',
                                                             'role': 'TA',
                                                             'address': '123 Main St',
                                                             'skills': ''})
        self.user.refresh_from_db()
        self.assertEqual(self.user.skills, "")


# class EditUserAcceptanceTest(TestCase):
#     def setUp(self):
#         self.client = Client()
#         self.user = User.objects.create(
#             first_name="John",
#             last_name="Doe",
#             username="johndoe",
#             password="password123",
#             email="johndoe@example.com",
#             phone_number="1234567890",
#             address="123 Main St",
#             role="Admin"
#         )
#         self.user.save()
#
#     def test_EditFirstName(self):
#         response = self.client.post('/configure_user.html', {'id': self.user.id, 'first_name': 'Jane',
#                                                             "form_name": "edit_user",
#                                                             'last_name': 'Doe',
#                                                             'email': 'johndoe@example.com',
#                                                             'username' : 'johndoe',
#                                                             'phone_number': '1234567890',
#                                                             'role': 'Admin'})
#         self.user.refresh_from_db()
#         self.assertEqual(self.user.first_name, "Jane")
#         self.assertEqual(User.objects.count(), 1)
#         self.assertIn('message', response.context)
#         self.assertEqual(response.context['message'], 'The user has been successfully updated')
#
#
#     def test_EditFirstNameInvalidEntry(self):
#         response = self.client.post('/configure_user.html',
#                                     {'id': self.user.id, 'first_name': '',
#                                                             "form_name": "edit_user",
#                                                             'last_name': 'Doe',
#                                                             'email': 'johndoe@example.com',
#                                                             'username' : 'johndoe',
#                                                             'phone_number': '1234567890',
#                                                             'role': 'Admin'})
#         self.user.refresh_from_db()
#         self.assertEqual(self.user.first_name, "John")
#         self.assertEqual(User.objects.count(), 1)
#         self.assertIn('message', response.context)
#         self.assertEqual(response.context['message'], 'Something went wrong when updating the user')
#
#     def test_EditLastName(self):
#         response = self.client.post('/configure_user.html',
#                                     {'id': self.user.id, 'first_name': 'John',
#                                                             "form_name": "edit_user",
#                                                             'last_name': 'Smith',
#                                                             'email': 'johndoe@example.com',
#                                                             'username' : 'johndoe',
#                                                             'phone_number': '1234567890',
#                                                             'role': 'Admin'})
#         self.user.refresh_from_db()
#         self.assertEqual(self.user.last_name, "Smith")
#         self.assertEqual(User.objects.count(), 1)
#         self.assertIn('message', response.context)
#         self.assertEqual(response.context['message'], 'The user has been successfully updated')
#
#     def test_EditLastNameInvalidEntry(self):
#         response = self.client.post('/configure_user.html',
#                                     {'id': self.user.id, 'first_name': 'John',
#                                                             "form_name": "edit_user",
#                                                             'last_name': '',
#                                                             'email': 'johndoe@example.com',
#                                                             'username' : 'johndoe',
#                                                             'phone_number': '1234567890',
#                                                             'role': 'Admin'})
#         self.user.refresh_from_db()
#         self.assertEqual(self.user.last_name, "Doe")
#         self.assertEqual(User.objects.count(), 1)
#         self.assertIn('message', response.context)
#         self.assertEqual(response.context['message'], 'Something went wrong when updating the user')
#
#     def test_EditEmail(self):
#         response = self.client.post('/configure_user.html',
#                                     {'id': self.user.id, 'first_name': 'John',
#                                                             "form_name": "edit_user",
#                                                             'last_name': 'Doe',
#                                                             'email': 'janesmith@example.com',
#                                                             'username' : 'johndoe',
#                                                             'phone_number': '1234567890',
#                                                             'role': 'Admin'})
#         self.user.refresh_from_db()
#         self.assertEqual(self.user.email, "janesmith@example.com")
#         self.assertEqual(User.objects.count(), 1)
#         self.assertIn('message', response.context)
#         self.assertEqual(response.context['message'], 'The user has been successfully updated')
#
#     def test_EditEmailInvalidEntry(self):
#         response = self.client.post('/configure_user.html',
#                                     {'id': self.user.id, 'first_name': 'John',
#                                                             "form_name": "edit_user",
#                                                             'last_name': 'Doe',
#                                                             'email': 'invalidemail',
#                                                             'username' : 'johndoe',
#                                                             'phone_number': '1234567890',
#                                                             'role': 'Admin'})
#         self.user.refresh_from_db()
#         self.assertEqual(self.user.email, "johndoe@example.com")
#         self.assertEqual(User.objects.count(), 1)
#         self.assertIn('message', response.context)
#         self.assertEqual(response.context['message'], 'Something went wrong when updating the user')
#
#     def test_EditPhone(self):
#         response = self.client.post('/configure_user.html',
#                                     {'id': self.user.id, 'first_name': 'John',
#                                                             "form_name": "edit_user",
#                                                             'last_name': 'Doe',
#                                                             'email': 'johndoe@example.com',
#                                                             'username' : 'johndoe',
#                                                             'phone_number': '1234567899',
#                                                             'role': 'Admin'})
#         self.user.refresh_from_db()
#         self.assertEqual(self.user.phone_number, "1234567899")
#         self.assertEqual(User.objects.count(), 1)
#         self.assertIn('message', response.context)
#         self.assertEqual(response.context['message'], 'The user has been successfully updated')
#
#     def test_EditPhoneInvalidEntry(self):
#         response = self.client.post('/configure_user.html',
#                                     {'id': self.user.id, 'first_name': 'John',
#                                                             "form_name": "edit_user",
#                                                             'last_name': 'Doe',
#                                                             'email': 'johndoe@example.com',
#                                                             'username' : 'johndoe',
#                                                             'phone_number': 'invalid',
#                                                             'role': 'Admin'})
#         self.user.refresh_from_db()
#         self.assertEqual(self.user.phone_number, "1234567890")
#         self.assertEqual(User.objects.count(), 1)
#         self.assertIn('message', response.context)
#         self.assertEqual(response.context['message'], 'Something went wrong when updating the user')
#
#     def test_EditRole(self):
#         response = self.client.post('/configure_user.html',
#                                     {'id': self.user.id, 'first_name': 'John',
#                                                             "form_name": "edit_user",
#                                                             'last_name': 'Doe',
#                                                             'email': 'johndoe@example.com',
#                                                             'username' : 'johndoe',
#                                                             'phone_number': '1234567890',
#                                                             'role': 'TA'})
#         self.user.refresh_from_db()
#         self.assertEqual(self.user.role, "TA")
#         self.assertEqual(User.objects.count(), 1)
#         self.assertIn('message', response.context)
#         self.assertEqual(response.context['message'], 'The user has been successfully updated')
#
#     def test_EditRoleInvalidEntry(self):
#         response = self.client.post('/configure_user.html',
#                                     {'id': self.user.id, 'first_name': 'John',
#                                                             "form_name": "edit_user",
#                                                             'last_name': 'Doe',
#                                                             'email': 'johndoe@example.com',
#                                                             'username' : 'johndoe',
#                                                             'phone_number': '1234567890',
#                                                             'role': 'Invalid'})
#         self.user.refresh_from_db()
#         self.assertEqual(self.user.role, "Admin")
#         self.assertEqual(User.objects.count(), 1)
#         self.assertIn('message', response.context)
#         self.assertEqual(response.context['message'], 'Something went wrong when updating the user')
