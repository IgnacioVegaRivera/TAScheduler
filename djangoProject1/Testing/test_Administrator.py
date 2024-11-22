# from Administrator import Admin
from djangoProject1.models import User, Course
from django.test import TestCase, Client
import unittest
from unittest.mock import Mock

class UnitAdminTest(unittest.TestCase):
    def setUp(self):
        self.client = Client()
        temp  = User(first_name="Bob", last_name="Smith", username="login", passwword="thepassword",
                     email="<bob@gmail.com>", phone_number="4141234567", address="UWM Campus", role="Administrator" )
        # self.User = Mock()
        # self.User.first_name = "Bob"
        # self.User.last_name = "Smith"
        # self.User.username = "login"
        # self.User.password = "<thepassword>"
        # self.User.email = "<bob@gmail.com>"
        # self.User.phone_number = "4141234567"
        # self.User.address = "UWM Campus"
        # self.User.role = "Admin"
        # self.User.first_name =  (username="login", password="<PASSWORD>")


    def test_default(self):
        self.assertEqual(self.temp.role, "Admin")

    # def test_Create_Course_2(self):
    #     classA = Course(name="mathClass", professor="BobS.")
    #     newClass = self.admin.create_course(classA)
    #     self.assertEqual(classA.name,"mathClass","The course name is not correct")

    # def test_Create_Course_1(self):
    #     user = self.User
    #     classA = Course(name="mathClass", professor="BobS.")
    #     newClass = user.create_course(classA)
    #     self.assertEqual(classA.name,"mathClass","The course name is not correct")
    #
    # def test_Create_Course_2(self):
    #     user = self.User
    #     classA = Course(name="mathClass", professor="BobS.")
    #     newClass = user.create_course(classA)
    #     self.assertEqual(classA.name,"mathClass","The course name is not correct")

    def test_Create_Course_CourseName(self):
        self.a = Mock()
        self.a = User("Bob", "Smith", "login", "password", "<EMAIL>", "4141234567", "UWM", "Admin")
        # classA = Course(name="mathClass", instructors="BobS.")
        # newClass = self.a.create_course(classA)
        newClass = self.a.create_course({"name": "mathClass", "instructors": "BobS."})
        self.assertEqual(newClass.name,"mathClass","The course name is not correct")

    def test_Create_Course_InstructorName(self):
        self.a = Mock()
        self.a = User("Bob", "Smith", "login", "password", "<EMAIL>", "4141234567", "UWM", "Admin")
        # classA = Course(name="mathClass", instructors="BobS.")
        # newClass = self.a.create_course(classA)
        newClass = self.a.create_course({"name": "mathClass", "instructors": "BobS."})
        self.assertEqual(newClass.instructors,"BobS.","The instructor name is not correct")

    def test_Create_Account_firstName(self):
        self.a = Mock()
        self.a = User("Bob", "Smith", "login", "password", "<EMAIL>", "4141234567", "UWM", "Admin")
        newAccount = self.a.create_account({"first_name":"Bob"})
        self.assertEqual(newAccount.first_name,"Bob","The first name is not correct")

    def test_Create_Account_lastName(self):
        self.a = Mock()
        self.a = User("Bob", "Smith", "login", "password", "<EMAIL>", "4141234567", "UWM", "Admin")
        newAccount = self.a.create_account({"last_name":"Sorenson"})
        self.assertEqual(newAccount.last_name,"Sorenson","The last name is not correct")

    def test_Create_Account_defaultFirstNames(self):
        self.a = Mock()
        self.a = User("Bob", "Smith", "login", "password", "<EMAIL>", "4141234567", "UWM", "Admin")
        newAccount = self.a.create_account()
        self.assertEqual(newAccount.first_name,"DefaultFirst","The default first name is not correct")

    def test_Create_Account_defaultLastNames(self):
        self.a = Mock()
        self.a = User("Bob", "Smith", "login", "password", "<EMAIL>", "4141234567", "UWM", "Admin")
        newAccount = self.a.create_account()
        self.assertEqual(newAccount.last_name,"DefaultLast","The default last name is not correct")

    # add more unit tests for Create account, checking indivdually whether or not each parameter
# class AcceptanceAdminTest(unittest.TestCase):

    def test_Delete_Account(self):
        a = User("Bob", "Smith", "login", "password", "<EMAIL>", "4141234567", "UWM", "Admin")
        alt_user = User("Steve", "Jobs", "login2", "password2", "<EMAIL2>", "4141234568", "UWM2", "TA")
        self.assertEquals(alt_user, a.delete_account(),"")