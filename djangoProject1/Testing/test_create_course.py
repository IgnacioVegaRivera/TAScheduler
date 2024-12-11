from django.test import TestCase, Client

from djangoProject1.MethodFiles.Administrator import CreateCourse
from djangoProject1.models import User, Course


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



# class CreateCourseAcceptanceTest(TestCase):
#     def setUp(self):
#         self.donkey = Client()
#         self.valid = User(username="valid", first_name="(no", last_name="instructor)", role="Instructor")
#         self.invalid = User(role="TA")
#         self.valid.save()
#         self.invalid.save()
#
#     #test if the inputted course is valid then it is added to the database
#     def test_valid_course(self):
#         response = self.donkey.post("/configure_course.html",
#                                 {"instructors": User.objects.filter(role="Instructor"), "instructor": self.valid,
#                                     "course_name": "course name", "form_name": "create_course"}, follow=True)
#         self.assertEqual(Course.objects.count(), 1)
#         self.assertIn('message', response.context)
#         self.assertEqual(response.context["message"], "The course \"course name\" has been created")
#
#
#     def test_invalid_role(self):
#         response = self.donkey.post("/configure_course.html",
#                                 {"instructors" : User.objects.filter(role="Instructor"),"instructor" : self.invalid,
#                                     "course_name": "course name", "form_name": "create_course"}, follow=True)
#         self.assertEqual(Course.objects.count(), 0)
#         self.assertIn('message', response.context)
#         self.assertEqual(response.context["message"], "Something went wrong when creating the course \"course name\"")
#
#     def test_no_instructor_selected(self):
#         response = self.donkey.post("/configure_course.html",
#                                     {"instructors": User.objects.filter(role="Instructor"), "instructor": "",
#                                      "course_name": "course name", "form_name": "create_course"}, follow=True)
#         self.assertEqual(Course.objects.count(), 0)
#         self.assertIn('message', response.context)
#         self.assertEqual(response.context["message"], "Something went wrong when creating the course \"course name\"")
#
#     def test_invalid_name(self):
#         response = self.donkey.post("/configure_course.html",
#                                 {"instructors" : User.objects.filter(role="Instructor"), "instructor" : self.valid,
#                                     "course_name": "", "form_name": "create_course"}, follow=True)
#         self.assertEqual(Course.objects.count(), 0)
#         self.assertIn('message', response.context)
#         self.assertEqual(response.context["message"], "Something went wrong when creating the course \"\"")
#
#     def test_invalid_form(self):
#         response = self.donkey.post("/configure_course.html",
#                                 {"instructors" : User.objects.filter(role="Instructor"), "instructor" : self.valid,
#                                     "course_name": "course name", "form_name": "fake_form"}, follow=True)
#         self.assertEqual(Course.objects.count(), 0)
#         self.assertIn('message', response.context)
#         self.assertEqual(response.context["message"], "Something went wrong when fetching the form, please try again.")