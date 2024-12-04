from django.test import TestCase, Client

from djangoProject1.MethodFiles.Administrator import EditCourse
from djangoProject1.models import User, Course


class test_edt_course(TestCase):
    def setUp(self):
        self.client = Client()
        self.temp_user = User(first_name="Jason",
                         last_name="Rock",
                         username="login1",
                         passwword="password1",
                         email="<jason@gmail.com>",
                         phone_number="4141234567",
                         address="UWM Campus",
                         role="Instructor")
        self.temp_course = Course("CS361", self.temp_user)
        self.temp_user.save()
        self.temp_course.save()

    def test_editInstructorName(self):
        pass

    def test_editCourseName(self):
        pass


