from django.test import TestCase, Client
from djangoProject1.models import User, Course, Section

class TestUserDirectoryUnit(TestCase):
    def setUp(self):
        # Create users for testing
        self.adminOne = User.objects.create(first_name="Ad", last_name="User", username="admin", role="Admin", email="admin@uwm.edu",
                                            phone_number= 1213439090, skills="None")
        self.instructorOne = User.objects.create(first_name="Instruct", last_name="User", username="instructor", role="Instructor",
                                                 email="instructor@uwm.edu", phone_number= 1415458080, skills="Data Structors, C, and Java")
        self.taOne = User.objects.create(first_name="TA", last_name="User", username="ta", role="TA", email="ta@uwm.edu",
                                         phone_number= 1615959090, skills="Python, AI, and JavaScript")

        # Create courses for testing
        self.courseOne = Course.objects.create(name="Course1")
        self.courseTwo = Course.objects.create(name="Course2")
        self.courseThree = Course.objects.create(name="Course3")

        # Create labs and assign TAs
        self.labOne = Section.objects.create(name="Lab 1", course=self.courseOne, days="Monday", time="3:00", location="EMS", user=self.taOne)
        self.labTwo = Section.objects.create(name="Lab 2", course=self.courseTwo, days="Wednesday", time="12:00", location="Kenwood", user=None)  # Unassigned lab
        self.labThree = Section.objects.create(name="Lab 3", course=self.courseThree, days="Thursday", time="2:30", location="Physics", user=self.taOne)

        # Assign instructors to courses
        self.courseOne.users.add(self.instructorOne)
        self.courseTwo.users.add(self.instructorOne)
        # leave courseThree empty for testing

    def test_admin_view_all_users(self):
        users = User.objects.all()
        self.assertEqual(users.count(), 3)
        self.assertIn(self.adminOne, users)
        self.assertIn(self.instructorOne, users)
        self.assertIn(self.taOne, users)

    def test_instructor_view_all_users(self):
        users = User.objects.all()
        self.assertEqual(users.count(), 3)
        self.assertIn(self.adminOne, users)
        self.assertIn(self.instructorOne, users)
        self.assertIn(self.taOne, users)

    def test_ta_view_all_users(self):
        users = User.objects.all()
        self.assertEqual(users.count(), 3)
        self.assertIn(self.adminOne, users)
        self.assertIn(self.instructorOne, users)
        self.assertIn(self.taOne, users)

    def test_view_user_phone_number(self):
        self.assertEqual(self.adminOne.phone_number, 1213439090)
        self.assertEqual(self.instructorOne.phone_number, 1415458080)
        self.assertEqual(self.taOne.phone_number, 1615959090)

    def test_view_user_email(self):
        self.assertEqual(self.adminOne.email, "admin@uwm.edu")
        self.assertEqual(self.instructorOne.email, "instructor@uwm.edu")
        self.assertEqual(self.taOne.email, "ta@uwm.edu")

    def test_view_user_skills(self):
        self.assertEqual(self.adminOne.skills, "None")
        self.assertEqual(self.instructorOne.skills, "Data Structors, C, and Java")
        self.assertEqual(self.taOne.skills, "Python, AI, and JavaScript")


