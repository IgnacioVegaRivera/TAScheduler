from django.test import TestCase, Client

from djangoProject1.MethodFiles.Administrator import CreateUser
from djangoProject1.models import User

class UserUnitTest(TestCase):
    def setUp(self):
        self.user = User( username="login", first_name="Bob", last_name="Smith", password="thepassword",
                     email="bob@gmail.com", phone_number="4141234567",
                         address="UWM Campus", role="Admin" )
        self.user.save()

    def test_creation_default_users(self):
        # Tests for creating users helper method
        user = CreateUser.create_user(
            username="username",
            email="email",
            password="password",
            first_name="first_name",
            last_name="last_name",
            phone_number="phone_number",
            address="address",
            role="role"
        )
        self.assertIsNotNone(user.id)
        self.assertEqual(user.first_name, "Bob")
        self.assertEqual(user.last_name, "Smith")
        self.assertEqual(user.username, "login")
        self.assertEqual(user.password, "thepassword")
        self.assertEqual(user.email, "bob@gmail.com")
        self.assertEqual(user.phone_number, "4141234567")
        self.assertEqual(user.address, "UWM Campus")
        self.assertEqual(user.role, "Admin")

    #If user inputs no username, then it will raise a ValueError
    def test_missing_username(self):
        user_data = vars(self.user)
        with self.assertRaises(ValueError):
            CreateUser.create_user(
                " ",
                email="email",
                password="password",
                first_name="first_name",
                last_name="last_name",
                phone_number="phone_number",
                address="address",
                role="role"
            )

    def test_username_exists(self):
        user = CreateUser.create_user(username="username",
            email="email",
            password="password",
            first_name="first_name",
            last_name="last_name",
            phone_number="phone_number",
            address="address",
            role="role"
        )
        self.assertEqual(user.user_name, "username")

    def test_email_exists(self):
        user = CreateUser.create_user(username="username",
            email="email",
            password="password",
            first_name="first_name",
            last_name="last_name",
            phone_number="phone_number",
            address="address",
            role="role"
                                      )
        self.assertEqual(user.user_email, "email")

