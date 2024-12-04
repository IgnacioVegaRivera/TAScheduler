from django.test import TestCase, Client
from djangoProject1.MethodFiles.Administrator import EditLab
from djangoProject1.models import User, Course, Lab

class test_edit_lab(TestCase):
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

        self.temp_user_TA = User(first_name="Ryan",
                         last_name="Reynolds",
                         username="login2",
                         passwword="password2",
                         email="<ja@gmail.com>",
                         phone_number="3141234567",
                         address="UWM Campus",
                         role="TA")

        self.temp_course = Course("CS361", self.temp_user)

        self.temp_lab = Lab("Lab001", self.temp_course, self.temp_user_TA)

        self.temp_lab.save()
        self.temp_course.save()
        self.temp_user_TA.save()
        self.temp_user_TA.save()