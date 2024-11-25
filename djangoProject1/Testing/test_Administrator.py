# from Administrator import Admin
from djangoProject1.models import User, Course
from django.test import TestCase, Client
import unittest
from unittest.mock import Mock
from djangoProject1.MethodFiles.Administrator import CreateCourse

class UnitAdminTest(TestCase):
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
        self.assertEqual(alt_user, a.delete_account(),"")


class CreateCourseUnitTest(TestCase):
    def setUp(self):
        self.user = User(first_name="(no", last_name="instructor)", role="Instructor")
        self.user.save()

    #to test properly we must save within the helper method
    def test_create_course(self):
        course = CreateCourse.create_course("name", self.user)
        self.assertEqual(course.name,"name")
        self.assertEqual(course.instructors.first(), self.user)

    #if anything is wrong then we want to set course to none and don't save it to the database
    def test_no_name(self):
        course = CreateCourse.create_course("", self.user)
        self.assertEqual(course, None)

    def test_no_instructor(self):
        course = CreateCourse.create_course("name", None)
        self.assertEqual(course, None)

    def test_not_an_instructor(self):
        ta = User(role="TA")
        course = CreateCourse.create_course("name", ta)
        self.assertEqual(course, None)

    def test_invalid_type(self):
        course = CreateCourse.create_course(123, self.user)
        self.assertEqual(course, None)

    def test_invalid_type_again(self):
        course = CreateCourse.create_course("name", "user")
        self.assertEqual(course, None)

    def test_course_already_exists(self):
        course = CreateCourse.create_course("name", self.user)
        self.assertEqual(course.name, "name")
        self.assertEqual(course.instructors.first(), self.user)

        course2 = CreateCourse.create_course("name", self.user)
        self.assertEqual(course2, None)



class CreateCourseAcceptanceTest(TestCase):
    def setUp(self):
        self.donkey = Client()
        self.valid = User(username="valid", first_name="(no", last_name="instructor)", role="Instructor")
        self.invalid = User(role="TA")
        self.valid.save()
        self.invalid.save()

    #test if the inputted course is valid then it is added to the database
    def test_valid_course(self):
        response = self.donkey.post("/configureCourse.html",
                                {"instructors": User.objects.filter(role="Instructor"), "instructor": self.valid,
                                    "course_name": "course name", "form_name": "create_course"}, follow=True)
        self.assertEqual(Course.objects.count(), 1)
        self.assertIn('message', response.context)
        self.assertEqual(response.context["message"], "The course \"course name\" has been created")


    def test_invalid_role(self):
        response = self.donkey.post("/configureCourse.html",
                                {"instructors" : User.objects.filter(role="Instructor"),"instructor" : self.invalid,
                                    "course_name": "course name", "form_name": "create_course"}, follow=True)
        self.assertEqual(Course.objects.count(), 0)
        self.assertIn('message', response.context)
        self.assertEqual(response.context["message"], "Something went wrong when creating the course \"course name\"")

    def test_invalid_name(self):
        response = self.donkey.post("/configureCourse.html",
                                {"instructors" : User.objects.filter(role="Instructor"), "instructor" : self.valid,
                                    "course_name": "", "form_name": "create_course"}, follow=True)
        self.assertEqual(Course.objects.count(), 0)
        self.assertIn('message', response.context)
        self.assertEqual(response.context["message"], "Something went wrong when creating the course \"\"")

    def test_invalid_form(self):
        response = self.donkey.post("/configureCourse.html",
                                {"instructors" : User.objects.filter(role="Instructor"), "instructor" : self.valid,
                                    "course_name": "course name", "form_name": "fake_form"}, follow=True)
        self.assertEqual(Course.objects.count(), 0)
        self.assertIn('message', response.context)
        self.assertEqual(response.context["message"], "Something went wrong when fetching the form, please try again")