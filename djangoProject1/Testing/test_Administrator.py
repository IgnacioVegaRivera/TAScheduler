# from Administrator import Admin
from djangoProject1.models import User
from django.test import TestCase, Client
import unittest
from unittest.mock import Mock
from djangoProject1.MethodFiles.Administrator import CreateCourse, CreateUser


# class Unit_Admin_CreateCourseTest(TestCase):
#     def setUp(self):
#         self.client = Client()
#         self.temp  = User(first_name="Bob", last_name="Smith", username="login", passwword="thepassword",
#                      email="<bob@gmail.com>", phone_number="4141234567", address="UWM Campus", role="Admin" )
#         self.temp.save()
#
#     def test_default(self):
#         self.assertEqual(self.temp.role, "Admin")
#
#     #unit tests for course creation
#
#     def test_Create_Course_CourseName(self):
#         self.a = User("Bob", "Smith", "login", "password", "<EMAIL>", "4141234567", "UWM", "Admin")
#         newClass = self.a.create_course({"name": "mathClass", "instructors": "BobS."})
#         self.assertEqual(newClass.name,"mathClass","The course name is not correct")
#
#     def test_Create_Course_InstructorName(self):
#         self.a = User("Bob", "Smith", "login", "password", "<EMAIL>", "4141234567", "UWM", "Admin")
#         newClass = self.a.create_course({"name": "mathClass", "instructors": "BobS."})
#         self.assertEqual(newClass.instructors,"BobS.","The instructor name is not correct")
#
#     def test_Create_Course_DefaultCourseName(self):
#         self.a = User("Bob", "Smith", "login", "password", "<EMAIL>", "4141234567", "UWM", "Admin")
#         newClass = self.a.create_course()
#         self.assertEqual(newClass.name,"Default Course Name","The default course name is not correct")
#
#
# #add more unit tests for Create account, checking indivdually whether or not each parameter
# # class AcceptanceAdminTest(unittest.TestCase):
#
# class UnitAdmin_DeleteAccountTest(TestCase):
#     def setUp(self):
#         self.client = Client()
#         self.temp  = User(first_name="Bob", last_name="Smith", username="login", passwword="thepassword",
#                      email="<bob@gmail.com>", phone_number="4141234567", address="UWM Campus", role="Admin" )
#         self.temp.save()
#
#     def test_Delete_Account(self):
#         self.a = User("Bob", "Smith", "login", "password", "<EMAIL>", "4141234567", "UWM", "Admin")
#         self.alt_user = User("Steve", "Jobs", "login2", "password2", "<EMAIL2>", "4141234568", "UWM2", "TA")
#         self.assertEqual(self.alt_user, self.a.delete_account(),"")
#
#
# class UnitAdmin_AddInstructorCourse(TestCase):
#     def setUp(self):
#         self.client = Client()
#         self.temp  = User(first_name="Bob", last_name="Smith", username="login", passwword="thepassword",
#                      email="<bob@gmail.com>", phone_number="4141234567", address="UWM Campus", role="Admin" )
#         self.temp.save()
#
# class AcceptanceAdmin_AddInstructorCOurse(TestCase):
#     def setUp(self):
#         self.donkey = Client()
#         self.temp  = User(first_name="Bob", last_name="Smith", username="login", passwword="thepassword",
#                      email="<bob@gmail.com>", phone_number="4141234567", address="UWM Campus", role="Admin" )
#         self.temp.save()
#
# class UnitAdmin_EditLabSection(TestCase):
#     def setUp(self):
#         self.client = Client()
#         self.temp  = User(first_name="Bob", last_name="Smith", username="login", passwword="thepassword",
#                      email="<bob@gmail.com>", phone_number="4141234567", address="UWM Campus", role="Admin" )
#         self.temp.save()
#
# class AcceptanceAdmin_EditLabSection(TestCase):
#     def setUp(self):
#         self.donkey = Client()
#         self.temp  = User(first_name="Bob", last_name="Smith", username="login", passwword="thepassword",
#                      email="<bob@gmail.com>", phone_number="4141234567", address="UWM Campus", role="Admin" )
#         self.temp.save()