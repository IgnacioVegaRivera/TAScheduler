from django.test import TestCase, Client
from djangoProject1.models import User, Course, Section

class TestCourseDirectoryAcceptance(TestCase):
    def setUp(self):
        self.client = Client()