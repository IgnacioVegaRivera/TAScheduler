from django.test import TestCase, Client
from djangoProject1.models import User

class TestProfilePage(TestCase):
    def setUp(self):
        # Create users for testing
        self.adminUno = User.objects.create(first_name="Ad", last_name="User", username="admin", role="Admin",
                                            email="admin@uwm.edu",
                                            phone_number=1213439090, skills="None", address="709 Big Boy Lane")
        self.instructorUno = User.objects.create(first_name="Instruct", last_name="User", username="instructor",
                                                 role="Instructor",
                                                 email="instructor@uwm.edu", phone_number=1415458080,
                                                 skills="Data Structors, C, and Java", address="313 Llama Rd.")
        self.taUno = User.objects.create(first_name="TA", last_name="User", username="ta", role="TA",
                                         email="ta@uwm.edu",
                                         phone_number=1615959090, skills="Python, AI, and JavaScript", address="907 Chicken Ct.")
        self.adminUno.save()
        self.instructorUno.save()
        self.taUno.save()

    def test_admin_view_profile_page(self):
        self.assertEqual(self.adminUno.first_name, "Ad")
        self.assertEqual(self.adminUno.last_name, "User")
        self.assertEqual(self.adminUno.username, "admin")
        self.assertEqual(self.adminUno.role, "Admin")
        self.assertEqual(self.adminUno.email, "admin@uwm.edu")
        self.assertEqual(self.adminUno.phone_number, 1213439090)
        self.assertEqual(self.adminUno.skills, "None")
        self.assertEqual(self.adminUno.address, "709 Big Boy Lane")

    def test_instructor_view_profile_page(self):
        self.assertEqual(self.instructorUno.first_name, "Instruct")
        self.assertEqual(self.instructorUno.last_name, "User")
        self.assertEqual(self.instructorUno.username, "instructor")
        self.assertEqual(self.instructorUno.role, "Instructor")
        self.assertEqual(self.instructorUno.email, "instructor@uwm.edu")
        self.assertEqual(self.instructorUno.phone_number, 1415458080)
        self.assertEqual(self.instructorUno.skills, "Data Structors, C, and Java")
        self.assertEqual(self.instructorUno.address, "313 Llama Rd.")

    def test_ta_view_profile_page(self):
        self.assertEqual(self.taUno.first_name, "TA")
        self.assertEqual(self.taUno.last_name, "User")
        self.assertEqual(self.taUno.username, "ta")
        self.assertEqual(self.taUno.role, "TA")
        self.assertEqual(self.taUno.email, "ta@uwm.edu")
        self.assertEqual(self.taUno.phone_number, 1615959090)
        self.assertEqual(self.taUno.skills, "Python, AI, and JavaScript")
        self.assertEqual(self.taUno.address, "907 Chicken Ct.")


