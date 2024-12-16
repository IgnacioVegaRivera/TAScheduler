from django.test import TestCase, Client

from djangoProject1.MethodFiles.Administrator import CreateCourse
from djangoProject1.models import User, Course


class CreateCourseUnitTest(TestCase):
    def setUp(self):
        self.user = User(first_name="(no", last_name="instructor)", role="Instructor")
        self.user.save()
        self.ta = User(role="TA")
        self.ta.save()

    #to test properly we must save within the helper method
    def test_create_course(self):
        course = CreateCourse.create_course("name", [self.user])
        self.assertEqual(course.name,"name")
        self.assertEqual(course.users, [self.user])

    #if anything is wrong then we want to set course to none and don't save it to the database
    def test_no_name(self):
        course = CreateCourse.create_course("", [self.user])
        self.assertEqual(course, None)

    def test_no_instructor(self):
        course = CreateCourse.create_course("name", [])
        self.assertEqual(course.name, "name")
        self.assertEqual(course.users, [])

    def test_adding_ta(self):

        course = CreateCourse.create_course("name", [self.ta])
        self.assertEqual(course.name, "name")
        self.assertEqual(course.users, [self.ta])

    def test_invalid_type(self):
        course = CreateCourse.create_course(123, [self.user])
        self.assertEqual(course, None)

    def test_invalid_type_again(self):
        course = CreateCourse.create_course("name", ["user"])
        self.assertEqual(course, None)

    def test_course_already_exists(self):
        course = CreateCourse.create_course("name", [self.user])
        self.assertEqual(course.name, "name")
        self.assertEqual(course.users.first(), [self.user])

        course2 = CreateCourse.create_course("name", [self.user])
        self.assertEqual(course2, None)

    def test_course_add_two_users(self):
        course = CreateCourse.create_course("name", [self.ta, self.user])
        self.assertEqual(course.name, "name")
        self.assertEqual(course.users.first(), [self.ta, self.user])

    def test_course_one_valid_one_invalid_user(self):
        course = CreateCourse.create_course("name", [self.ta, "instructor"])
        self.assertEqual(course, None)

    def test_course_two_invalid_user(self):
        course = CreateCourse.create_course("name", [123, "instructor"])
        self.assertEqual(course, None)