from django.test import TestCase, Client
from djangoProject1.models import User

class TestProfilePageAcceptance(TestCase):
    def setUp(self):
        self.client = Client()
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

    def login_as(self, username):
        self.client.post("/", {"username": username, "password": "password"})

    def test_admin_view_profile_page(self):
        self.login_as("admin")
        response = self.client.get("/profile_page.html")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Ad")
        self.assertContains(response, "User")
        self.assertContains(response, "admin")
        self.assertContains(response, "Admin")
        self.assertContains(response, "admin@uwm.edu")
        self.assertContains(response, 1213439090)
        self.assertContains(response, "None")
        self.assertContains(response, "709 Big Boy Lane")

    def test_instructor_view_profile_page(self):
        self.login_as("instructor")
        response = self.client.get("/profile_page.html")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Instruct")
        self.assertContains(response, "User")
        self.assertContains(response, "instructor")
        self.assertContains(response, "Instructor")
        self.assertContains(response, "instructor@uwm.edu")
        self.assertContains(response, 1415458080)
        self.assertContains(response, "Data Structors, C, and Java")
        self.assertContains(response, "313 Llama Rd.")

    def test_ta_view_profile_page(self):
        self.login_as("ta")
        response = self.client.get("/profile_page.html")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "TA")
        self.assertContains(response, "User")
        self.assertContains(response, "ta")
        self.assertContains(response, "TA")
        self.assertContains(response, "ta@uwm.edu")
        self.assertContains(response, 1615959090)
        self.assertContains(response, "Python, AI, and JavaScript")
        self.assertContains(response, "907 Chicken Ct.")