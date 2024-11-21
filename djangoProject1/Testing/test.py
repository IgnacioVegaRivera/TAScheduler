from django.test import TestCase, Client
from djangoProject1.models import User
# test file for testing the models, database, and various functions to be implemented

#Unit Tests for logging in
class TestLoginUnit(TestCase):
    def setUp(self):
        self.donkey = Client()
        temp = User(username="one", password="two")
        temp.save()

    def test_page_access(self):
        # gets the login url and makes sure the user can access it
        response = self.donkey.get('/')
        self.assertEqual(response.status_code, 200)
        # checks that the page it leads to is the login page that we made
        self.assertTemplateUsed(response, 'login.html')

    def test_success_login(self):
        # if the login info is correct then the user redirects
        response = self.donkey.post('/', {"username": "one", "password": "two"})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, "home.html")

    def test_fail_login(self):
        #if the login info is incorrect then the user doesn't redirect
        response = self.donkey.post('/', {"username": "one", "password": "wrong"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.url, "login.html")

    def test_empty(self):
        response = self.donkey.post('/', {"username": "", "password": ""})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.url, "login.html")

    def test_no_username(self):
        #if no username entered then user doesn't redirect
        response = self.donkey.post('/', {"username": "", "password": "two"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.url, "login.html")

    def test_no_password(self):
        # if no password entered then user doesn't redirect
        response = self.donkey.post('/', {"username": "one", "password": ""})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.url, "login.html")




#Acceptance Tests for logging in
class TestLoginAcceptance(TestCase):
    def setUp(self):
        self.donkey = Client()
        temp = User(name="one", password="two")
        temp.save()

    def test_login_success(self):
        #create a response of us entering the correct password
        response = self.donkey.post("/",{"username" : "one", "password" : "two"}, follow=True)
        self.assertEqual(response.status_code, 200)

        #check that we get redirected to the things page after we enter the right password
        self.assertRedirects(response, "/home/", 302)

    def test_login_fail(self):
        response = self.donkey.post("/", {"username": "one", "password": "wrong"}, follow=True)
        # even though the password is wrong the site stays up so check for 200
        self.assertEqual(response.status_code, 200)

        # is the message appearing
        self.assertIn("message", response.context)

        # is the message equal to "bad password"
        self.assertEqual(response.context["message"], "Username or Password is incorrect")

