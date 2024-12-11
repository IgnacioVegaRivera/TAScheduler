from django.test import TestCase, Client

from djangoProject1.models import User, Course

class CreateCourseAcceptanceTest(TestCase):
    def setUp(self):
        self.donkey = Client()
        self.valid = User(username="valid", first_name="(no", last_name="instructor)", role="Instructor")
        self.invalid = User(role="TA")
        self.valid.save()
        self.invalid.save()

    #test if the inputted course is valid then it is added to the database
    def test_valid_course(self):
        response = self.donkey.post("/configure_course.html",
                                {"instructors": User.objects.filter(role="Instructor"), "instructor": self.valid,
                                    "course_name": "course name", "form_name": "create_course"}, follow=True)
        self.assertEqual(Course.objects.count(), 1)
        self.assertIn('message', response.context)
        self.assertEqual(response.context["message"], "The course \"course name\" has been created")


    def test_invalid_role(self):
        response = self.donkey.post("/configure_course.html",
                                {"instructors" : User.objects.filter(role="Instructor"),"instructor" : self.invalid,
                                    "course_name": "course name", "form_name": "create_course"}, follow=True)
        self.assertEqual(Course.objects.count(), 0)
        self.assertIn('message', response.context)
        self.assertEqual(response.context["message"], "Something went wrong when creating the course \"course name\"")

    def test_no_instructor_selected(self):
        response = self.donkey.post("/configure_course.html",
                                    {"instructors": User.objects.filter(role="Instructor"), "instructor": "",
                                     "course_name": "course name", "form_name": "create_course"}, follow=True)
        self.assertEqual(Course.objects.count(), 0)
        self.assertIn('message', response.context)
        self.assertEqual(response.context["message"], "Something went wrong when creating the course \"course name\"")

    def test_invalid_name(self):
        response = self.donkey.post("/configure_course.html",
                                {"instructors" : User.objects.filter(role="Instructor"), "instructor" : self.valid,
                                    "course_name": "", "form_name": "create_course"}, follow=True)
        self.assertEqual(Course.objects.count(), 0)
        self.assertIn('message', response.context)
        self.assertEqual(response.context["message"], "Something went wrong when creating the course \"\"")

    def test_invalid_form(self):
        response = self.donkey.post("/configure_course.html",
                                {"instructors" : User.objects.filter(role="Instructor"), "instructor" : self.valid,
                                    "course_name": "course name", "form_name": "fake_form"}, follow=True)
        self.assertEqual(Course.objects.count(), 0)
        self.assertIn('message', response.context)
        self.assertEqual(response.context["message"], "Something went wrong when fetching the form, please try again.")