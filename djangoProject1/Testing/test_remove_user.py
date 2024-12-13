from django.test import TestCase, Client
from djangoProject1.MethodFiles.Administrator import RemoveUser
from djangoProject1.models import User, Course, Section

class TestRemoveUserUnit(TestCase):
    def setUp(self):
        #create some users
        self.donkey = Client()
        self.admin = User.objects.create(first_name='Ad', last_name='Min', username='admin',
                                         email='admin@uwm.edu', phone_number="1234567890", role='Admin', skills='Admin skills')
        self.instructor = User.objects.create(first_name='Inst', last_name='Ructor', username='instructor',
                                         email='instructor@uwm.edu', phone_number="0123456789", role='Instructor',skills='Good at teaching')
        self.ta = User.objects.create(first_name='T', last_name='A', username='ta',
                                         email='ta@uwm.edu', phone_number="9876543210", role='TA', skills='Proficient in java')
        self.admin.save()
        self.instructor.save()
        self.ta.save()

        #create some courses/labs
        self.course = Course.objects.create(name="Course 1")
        self.course.save()
        self.course.users.add(self.instructor)

        self.lab = Section.objects.create(name="Lab 1", course=self.course, user=self.ta)
        self.lab.save()


    def test_remove_valid_user(self):
        RemoveUser.remove_user(self.instructor.id)
        self.assertIsNone(self.instructor, "The user should have been removed")
        self.assertEqual(User.objects.count(), 2)

    def test_remove_invalid_user(self):
        RemoveUser.remove_user(4)
        self.assertIsNotNone(self.instructor, "The user should have been removed, but an incorrect id was used")
        self.assertEqual(User.objects.count(), 3)

    def test_remove_twice(self):
        RemoveUser.remove_user(self.instructor.id)
        self.assertIsNone(self.instructor, "The user should have been removed")
        self.assertEqual(User.objects.count(), 2)

        RemoveUser.remove_user(self.instructor.id)
        self.assertEqual(User.objects.count(), 2)