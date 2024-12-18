from django.test import TestCase

from djangoProject1.MethodFiles.GeneralMethods import CheckPermission
from djangoProject1.models import User

class TestInstructorPageUnit(TestCase):
    def setUp(self):
        self.admin = User(username='Admin', role="Admin")
        self.instructor = User(username='Instructor', role='Instructor')
        self.ta = User(username='TA', role='TA')


    def test_admin_user(self):
        self.assertTrue(CheckPermission.check_admin(self.admin))


    def test_instructor(self):
        self.assertFalse(CheckPermission.check_admin(self.instructor))


    def test_ta(self):
        self.assertFalse(CheckPermission.check_admin(self.ta))


    def test_no_user(self):
        self.assertFalse(CheckPermission.check_admin(None))