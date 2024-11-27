from django.test import TestCase, Client

from djangoProject1.MethodFiles.Administrator import CreateUser
from djangoProject1.models import User

class UserUnitTest(TestCase):
    def setUp(self):
        self.user = User(first_name="Bob", last_name="Smith", username="login", password="thepassword",
                     email="bob@gmail.com", phone_number="4141234567",
                         address="UWM Campus", role="Admin" )
        self.user.save()

    def test_creation_users(self):
        #Allow the self.user data info to be passed as an arguement
        user_data = vars(self.user)

        # Tests for creating users helper method
        user = CreateUser.create_user(user_name=user_data["username"],
            user_email=user_data["email"],
            user_password=user_data["password"],
            user_first_name=user_data["first_name"],
            user_last_name=user_data["last_name"],
            user_phone_number=user_data["phone_number"],
            user_address=user_data["address"],
            user_role=user_data["role"]
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
                user_name=user_data[" "],
                user_password=user_data["password"],
                user_first_name=user_data["first_name"],
                user_last_name=user_data["last_name"],
                user_phone_number=user_data["phone_number"],
                user_address=user_data["address"],
                user_role=user_data["role"],
                user_email=user_data["email"]
            )

    def test_username_exists(self):
        user = CreateUser.create_user(user_name="username",
            user_email="email",
            user_password="password",
            user_first_name="first_name",
            user_last_name="last_name",
            user_phone_number="phone_number",
            user_address="address",
            user_role="role"
        )
        self.assertEqual(user.user_name, "username")

    def test_email_exists(self):
        user = CreateUser.create_user(user_name="username",
                                      user_email="email",
                                      user_password="password",
                                      user_first_name="first_name",
                                      user_last_name="last_name",
                                      user_phone_number="phone_number",
                                      user_address="address",
                                      user_role="role"
                                      )
        self.assertEqual(user.user_email, "email")

