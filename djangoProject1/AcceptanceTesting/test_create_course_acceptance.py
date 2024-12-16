from django.test import TestCase, Client

from djangoProject1.models import User, Course

class CreateCourseAcceptanceTest(TestCase):
    def setUp(self):
        self.donkey = Client()
        self.validInst = User(username="validInst", first_name="(no", last_name="instructor)", role="Instructor")
        self.validTA = User(username="validTA", first_name="(no", last_name="TA)", role="TA")
        self.invalid = User(role="Admin")
        self.validInst.save()
        self.validTA.save()
        self.invalid.save()

    #test if the inputted course is valid then it is added to the database
    def test_valid_course(self):
        response = self.donkey.post("/configure_course.html",
                                {"instructors": [self.validInst.id], "tas":[self.validTA.id],
                                       "course_name": "course name", "form_name": "create_course"}, follow=True)
        self.assertEqual(Course.objects.count(), 1)
        self.assertIn('message', response.context)
        self.assertEqual(response.context["message"], "The course \"course name\" has been created")


    def test_invalid_user_role(self):
        response = self.donkey.post("/configure_course.html",
                                {"instructors": [self.validInst.id], "tas":[self.invalid.id],
                                       "course_name": "course name", "form_name": "create_course"}, follow=True)
        self.assertEqual(Course.objects.count(), 0)
        self.assertIn('message', response.context)
        self.assertEqual(response.context["message"], "Something went wrong when creating the course \"course name\"")

    def test_no_user_selected(self):
        response = self.donkey.post("/configure_course.html",
                                    {"instructors": [], "tas":[],
                                       "course_name": "course name", "form_name": "create_course"}, follow=True)
        self.assertEqual(Course.objects.count(), 1)
        self.assertIn('message', response.context)
        self.assertEqual(response.context["message"], "The course \"course name\" has been created")

    def test_invalid_name(self):
        response = self.donkey.post("/configure_course.html",
                                {"instructors": [self.validInst.id], "tas":[self.validTA.id],
                                       "course_name": "", "form_name": "create_course"}, follow=True)
        self.assertEqual(Course.objects.count(), 0)
        self.assertIn('message', response.context)
        self.assertEqual(response.context["message"], "Something went wrong when creating the course \"\"")

    def test_invalid_form(self):
        response = self.donkey.post("/configure_course.html",
                                {"instructors": [self.validInst.id], "tas":[self.validTA.id],
                                       "course_name": "course name", "form_name": "fake_form"}, follow=True)
        self.assertEqual(Course.objects.count(), 0)
        self.assertIn('message', response.context)
        self.assertEqual(response.context["message"], "Something went wrong when fetching the form, please try again.")