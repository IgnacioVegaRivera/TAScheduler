# from Administrator import Admin
from djangoProject1.models import User
from django.test import TestCase, Client
import unittest
from unittest.mock import Mock
from djangoProject1.MethodFiles.Administrator import CreateCourse

class UnitAdmin_CreateCourseTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.temp  = User(first_name="Bob", last_name="Smith", username="login", passwword="thepassword",
                     email="<bob@gmail.com>", phone_number="4141234567", address="UWM Campus", role="Admin" )
        self.temp.save()

    def test_default(self):
        self.assertEqual(self.temp.role, "Admin")

    #unit tests for course creation

    def test_Create_Course_CourseName(self):
        self.a = User("Bob", "Smith", "login", "password", "<EMAIL>", "4141234567", "UWM", "Admin")
        newClass = self.a.create_course({"name": "mathClass", "instructors": "BobS."})
        self.assertEqual(newClass.name,"mathClass","The course name is not correct")

    def test_Create_Course_InstructorName(self):
        self.a = User("Bob", "Smith", "login", "password", "<EMAIL>", "4141234567", "UWM", "Admin")
        newClass = self.a.create_course({"name": "mathClass", "instructors": "BobS."})
        self.assertEqual(newClass.instructors,"BobS.","The instructor name is not correct")

    def test_Create_Course_DefaultCourseName(self):
        self.a = User("Bob", "Smith", "login", "password", "<EMAIL>", "4141234567", "UWM", "Admin")
        newClass = self.a.create_course()
        self.assertEqual(newClass.name,"Default Course Name","The default course name is not correct")


    #unit tests for each field in creation(user input)
class UnitAdmin_CreateAccountTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.temp  = User(first_name="Bob", last_name="Smith", username="login", passwword="thepassword",
                     email="<bob@gmail.com>", phone_number="4141234567", address="UWM Campus", role="Admin" )
        self.temp.save()

    def test_Create_Account_firstName(self):
        self.a = User("Bob", "Smith", "login", "password", "<EMAIL>", "4141234567", "UWM", "Admin")
        newAccount = self.a.create_account({"first_name":"Bob"})
        self.assertEqual(newAccount.first_name,"Bob","The first name is not correct")

    def test_Create_Account_lastName(self):
        self.a = User("Bob", "Smith", "login", "password", "<EMAIL>", "4141234567", "UWM", "Admin")
        newAccount = self.a.create_account({"last_name":"Sorenson"})
        self.assertEqual(newAccount.last_name,"Sorenson","The last name is not correct")

    def test_Create_Account_Username(self):
        self.a = User("Bob", "Smith", "login", "password", "<EMAIL>", "4141234567", "UWM", "Admin")
        newAccount = self.a.create_account({"username": "login"})
        self.assertEqual(newAccount.username,"login","The username is not correct")

    def test_Create_Account_Password(self):
        self.a = User("Bob", "Smith", "login", "password", "<EMAIL>", "4141234567", "UWM", "Admin")
        newAccount = self.a.create_account({"last_name": "password"})
        self.assertEqual(newAccount.password,"password","The password is not correct")

    def test_Create_Account_Email(self):
        self.a = User("Bob", "Smith", "login", "password", "bob@gmail.com", "4141234567", "UWM", "Admin")
        newAccount = self.a.create_account({"email": "bob@gmail.com"})
        self.assertEqual(newAccount.email,"bob@gmail.com","The email is not correct")

    def test_Create_Account_Phone(self):
        self.a = User("Bob", "Smith", "login", "password", "<EMAIL>", "4141234567", "UWM", "Admin")
        newAccount = self.a.create_account({"phone_number": "4141234567"})
        self.assertEqual(newAccount.phone_number,"4141234567","The phone number is not correct")

    def test_Create_Account_Address(self):
        self.a = User("Bob", "Smith", "login", "password", "<EMAIL>", "4141234567", "UWM", "Admin")
        newAccount = self.a.create_account({"address": "UWM"})
        self.assertEqual(newAccount.address,"UWM","The address is not correct")

    def test_Create_Account_Role(self):
        self.a = User("Bob", "Smith", "login", "password", "<EMAIL>", "4141234567", "UWM", "Admin")
        newAccount = self.a.create_account({"role": "Admin"})
        self.assertEqual(newAccount.role,"Admin","The role is not correct")

    #unit tests testing created account with default values

    def test_Create_Account_defaultFirstNames(self):
        self.a = User("Bob", "Smith", "login", "password", "<EMAIL>", "4141234567", "UWM", "Admin")
        newAccount = self.a.create_account()
        self.assertEqual(newAccount.first_name,"DefaultFirst","The default first name is not correct")

    def test_Create_Account_defaultLastNames(self):
        self.a = User("Bob", "Smith", "login", "password", "<EMAIL>", "4141234567", "UWM", "Admin")
        newAccount = self.a.create_account()
        self.assertEqual(newAccount.last_name,"DefaultLast","The default last name is not correct")

    def test_Create_Account_defaultUsername(self):
        self.a = User("Bob", "Smith", "login", "password", "<EMAIL>", "4141234567", "UWM", "Admin")
        newAccount = self.a.create_account()
        self.assertEqual(newAccount.username,"Default_Username","The default username is not correct")

    def test_Create_Account_defaultPassword(self):
        self.a = User("Bob", "Smith", "login", "password", "<EMAIL>", "4141234567", "UWM", "Admin")
        newAccount = self.a.create_account()
        self.assertEqual(newAccount.password,"Default_Password","The default password is not correct")

    def test_Create_Account_defaultEmail(self):
        self.a = User("Bob", "Smith", "login", "password", "<EMAIL>", "4141234567", "UWM", "Admin")
        newAccount = self.a.create_account()
        self.assertEqual(newAccount.email,"<default@example.com>","The default email is not correct")

    def test_Create_Account_defaultRole(self):
        self.a = User("Bob", "Smith", "login", "password", "<EMAIL>", "4141234567", "UWM", "Admin")
        newAccount = self.a.create_account()
        self.assertEqual(newAccount.role,"TA","The default role is not correct")

# add more unit tests for Create account, checking indivdually whether or not each parameter
# class AcceptanceAdminTest(unittest.TestCase):

class UnitAdmin_DeleteAccountTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.temp  = User(first_name="Bob", last_name="Smith", username="login", passwword="thepassword",
                     email="<bob@gmail.com>", phone_number="4141234567", address="UWM Campus", role="Admin" )
        self.temp.save()

    def test_Delete_Account(self):
        self.a = User("Bob", "Smith", "login", "password", "<EMAIL>", "4141234567", "UWM", "Admin")
        self.alt_user = User("Steve", "Jobs", "login2", "password2", "<EMAIL2>", "4141234568", "UWM2", "TA")
        self.assertEqual(self.alt_user, self.a.delete_account(),"")
