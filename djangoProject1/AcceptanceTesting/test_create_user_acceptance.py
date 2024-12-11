from django.test import TestCase, Client

from djangoProject1.models import User

class Acceptance_Admin_CreateAccountTest(TestCase):
    def setUp(self):
        self.donkey = Client()



    def test_valid_User(self):
        response = self.donkey.post("/configure_user.html", {"first_name" : "Administrator",
                "last_name":"Smith", "username":"login1", "password":"password1", "email":"<EMAIL1>@email.com",
                "phone_number":"1141234567", "address":"UWM1", "role":"Admin", "form_name":"create_user"}, follow=True)
        self.assertEqual(User.objects.count(), 1, "The amount of users do not match")
        self.assertIn('message', response.context)
        self.assertEqual(response.context['message'],
                         "The user \"Administrator Smith\" has been created")

    def test_invalid_User_firstName(self):
        response = self.donkey.post("/configure_user.html", {"first_name" : "",
                "last_name":"Smith", "username":"login1", "password":"password1", "email":"<EMAIL1>@email.com",
                "phone_number":"1141234567", "address":"UWM1", "role":"Admin", "form_name":"create_user"}, follow=True)
        self.assertEqual(User.objects.count(), 0, "The amount of users do not match")
        self.assertIn('message', response.context)
        self.assertEqual(response.context['message'],
                         "Something went wrong when creating the user \" Smith\"")

    def test_invalid_User_lastName(self):
        response = self.donkey.post("/configure_user.html", {"first_name" : "Administrator",
                "last_name":"", "username":"login1", "password":"password1", "email":"<EMAIL1>@email.com",
                "phone_number":"1141234567", "address":"UWM1", "role":"Admin", "form_name":"create_user"}, follow=True)
        self.assertEqual(User.objects.count(), 0, "The amount of users do not match")
        self.assertIn('message', response.context)
        self.assertEqual(response.context['message'],
                         "Something went wrong when creating the user \"Administrator \"")

    def test_invalid_User_Username(self):
        response = self.donkey.post("/configure_user.html", {"first_name" : "Administrator",
                "last_name":"Smith", "username":"", "password":"password1", "email":"<EMAIL1>@email.com",
                "phone_number":"1141234567", "address":"UWM1", "role":"Admin", "form_name":"create_user"}, follow=True)
        self.assertEqual(User.objects.count(), 0, "The amount of users do not match")
        self.assertIn('message', response.context)
        self.assertEqual(response.context['message'],
                         "Something went wrong when creating the user \"Administrator Smith\"")


    def test_invalid_User_Password(self):
        response = self.donkey.post("/configure_user.html", {"first_name" : "Administrator",
                "last_name":"Smith", "username":"login1", "password":"", "email":"<EMAIL1>@email.com",
                "phone_number":"1141234567", "address":"UWM1", "role":"Admin", "form_name":"create_user"}, follow=True)
        self.assertEqual(User.objects.count(), 0, "The amount of users do not match")
        self.assertIn('message', response.context)
        self.assertEqual(response.context['message'],
                         "Something went wrong when creating the user \"Administrator Smith\"")


    def test_invalid_User_Email(self):
        response = self.donkey.post("/configure_user.html", {"first_name" : "Administrator",
                "last_name":"Smith", "username":"login1", "password":"password1", "email":"",
                "phone_number":"1141234567", "address":"UWM1", "role":"Admin", "form_name":"create_user"}, follow=True)
        self.assertEqual(User.objects.count(), 0, "The amount of users do not match")
        self.assertIn('message', response.context)
        self.assertEqual(response.context['message'],
                         "Something went wrong when creating the user \"Administrator Smith\"")


    def test_invalid_User_PhoneNumber(self):
        response = self.donkey.post("/configure_user.html", {"first_name" : "Administrator",
                "last_name":"Smith", "username":"login1", "password":"password1", "email":"<EMAIL1>@email.com",
                "phone_number":"", "address":"UWM1", "role":"Admin", "form_name":"create_user"}, follow=True)
        self.assertEqual(User.objects.count(), 0, "The amount of users do not match")
        self.assertIn('message', response.context)
        self.assertEqual(response.context['message'],
                         "Something went wrong when creating the user \"Administrator Smith\"")


    def test_invalid_User_Address(self):
        response = self.donkey.post("/configure_user.html", {"first_name" : "Administrator",
                "last_name":"Smith", "username":"login1", "password":"password1", "email":"<EMAIL1>@email.com",
                "phone_number":"1141234567", "address":"", "role":"Admin", "form_name":"create_user"}, follow=True)
        self.assertEqual(User.objects.count(), 0, "The amount of users do not match")
        self.assertIn('message', response.context)
        self.assertEqual(response.context['message'],
                         "Something went wrong when creating the user \"Administrator Smith\"")


    def test_invalid_User_Role(self):
        response = self.donkey.post("/configure_user.html", {"first_name" : "Administrator",
                "last_name":"Smith", "username":"login1", "password":"password1", "email":"<EMAIL1>@email.com",
                "phone_number":"1141234567", "address":"UWM1", "role":"", "form_name":"create_user"}, follow=True)
        self.assertEqual(User.objects.count(), 0, "The amount of users do not match")
        self.assertIn('message', response.context)
        self.assertEqual(response.context['message'],
                         "Something went wrong when creating the user \"Administrator Smith\"")


    def test_invalid_User_FormName(self):
        response = self.donkey.post("/configure_user.html", {"first_name" : "Administrator",
                "last_name":"Smith", "username":"login1", "password":"password1", "email":"<EMAIL1>@email.com",
                "phone_number":"1141234567", "address":"UWM1", "role":"Admin", "form_name":""}, follow=True)
        self.assertEqual(User.objects.count(), 0, "The amount of users do not match")
        self.assertIn('message', response.context)
        self.assertEqual(response.context['message'],
                         "Something went wrong when fetching the form, please try again")