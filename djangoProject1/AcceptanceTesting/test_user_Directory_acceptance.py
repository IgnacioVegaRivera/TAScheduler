from django.test import TestCase, Client
from djangoProject1.models import User, Course, Section

class TestCourseDirectoryAcceptance(TestCase):
    def setUp(self):
        self.client = Client()

        # Create users for testing
        self.admin1 = User.objects.create(first_name="Ad1", last_name="User", username="admin", role="Admin",
                                            email="admin@uwm.edu",
                                            phone_number=1213439090, skills="None", password="password")
        self.instructor1 = User.objects.create(first_name="Instruct1", last_name="User", username="instructor",
                                                 role="Instructor",
                                                 email="instructor@uwm.edu", phone_number=1415458080,
                                                 skills="Data Structors, C, and Java", password="password")
        self.ta1 = User.objects.create(first_name="TA1", last_name="User", username="ta", role="TA",
                                         email="ta@uwm.edu",
                                         phone_number=1615959090, skills="Python, AI, and JavaScript", password="password")

        # Create courses for testing
        self.course1 = Course.objects.create(name="CourseOne")
        self.course2 = Course.objects.create(name="CourseTwo")
        self.course3 = Course.objects.create(name="CourseThree")

        # Save the TA to course for the assignment of the Lab
        self.course1.users.add(self.ta1)
        self.course3.users.add(self.ta1)

        # Create labs and assign TAs
        self.lab1 = Section.objects.create(name="Lab One", course=self.course1, days="Monday", time="3:00",
                                             location="EMS", user=self.ta1)
        self.lab2 = Section.objects.create(name="Lab Two", course=self.course2, days="Wednesday", time="12:00",
                                             location="Kenwood", user=None)  # Unassigned lab
        self.lab3 = Section.objects.create(name="Lab Three", course=self.course3, days="Thursday", time="2:30",
                                               location="Physics", user=self.ta1)

        # Assign instructors to courses
        self.course1.users.add(self.instructor1)
        self.course2.users.add(self.instructor1)
        # leave courseThree empty for testing

        # save the users created
        self.admin1.save()
        self.instructor1.save()
        self.ta1.save()

    def login_as(self, username):
        self.client.post("/", {"username": username, "password": "password"})


    def test_admin_view_all_users_acceptance(self):
        self.login_as("admin")
        response = self.client.get("/user_directory.html")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Ad1 User")
        self.assertContains(response, "Instruct1 User")
        self.assertContains(response, "TA1 User")

    def test_instructor_view_all_users_acceptance(self):
        self.login_as("instructor")
        response = self.client.get("/user_directory.html")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Ad1 User")
        self.assertContains(response, "Instruct1 User")
        self.assertContains(response, "TA1 User")

    def test_ta_view_all_users_acceptance(self):
        self.login_as("ta")
        response = self.client.get("/user_directory.html")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Ad1 User")
        self.assertContains(response, "Instruct1 User")
        self.assertContains(response, "TA1 User")

    def test_admin_view_user_email_acceptance(self):
        self.login_as("admin")
        response = self.client.get("/user_directory.html")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "admin@uwm.edu")
        self.assertContains(response, "instructor@uwm.edu")
        self.assertContains(response, "ta@uwm.edu")

    def test_instructor_view_user_email_acceptance(self):
        self.login_as("instructor")
        response = self.client.get("/user_directory.html")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "admin@uwm.edu")
        self.assertContains(response, "instructor@uwm.edu")
        self.assertContains(response, "ta@uwm.edu")

    def test_ta_view_user_email_acceptance(self):
        self.login_as("ta")
        response = self.client.get("/user_directory.html")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "admin@uwm.edu")
        self.assertContains(response, "instructor@uwm.edu")
        self.assertContains(response, "ta@uwm.edu")

    def test_admin_view_user_phone_number_acceptance(self):
        self.login_as("admin")
        response = self.client.get("/user_directory.html")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "121-343-9090")
        self.assertContains(response, "141-545-8080")
        self.assertContains(response, "161-595-9090")

    def test_instructor_view_user_phone_number_acceptance(self):
        self.login_as("instructor")
        response = self.client.get("/user_directory.html")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "121-343-9090")
        self.assertContains(response, "141-545-8080")
        self.assertContains(response, "161-595-9090")

    def test_ta_instructor_view_user_phone_number_acceptance(self):
        self.login_as("ta")
        response = self.client.get("/user_directory.html")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "121-343-9090")
        self.assertContains(response, "141-545-8080")
        self.assertContains(response, "161-595-9090")

    def test_admin_view_user_skills_acceptance(self):
        self.login_as("admin")
        response = self.client.get("/user_directory.html")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "None")
        self.assertContains(response, "Data Structors, C, and Java")
        self.assertContains(response, "Python, AI, and JavaScript")

    def test_instructor_view_user_skills_acceptance(self):
        self.login_as("instructor")
        response = self.client.get("/user_directory.html")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "None")
        self.assertContains(response, "Data Structors, C, and Java")
        self.assertContains(response, "Python, AI, and JavaScript")

    def test_ta_view_user_skills_acceptance(self):
        self.login_as("ta")
        response = self.client.get("/user_directory.html")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "None")
        self.assertContains(response, "Data Structors, C, and Java")
        self.assertContains(response, "Python, AI, and JavaScript")

    def test_admin_view_user_sections_acceptance(self):
        self.login_as("admin")
        response = self.client.get("/user_directory.html")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Lab One - CourseOne")
        self.assertNotContains(response, "Lab Two - CourseTwo")
        self.assertContains(response, "Lab Three - CourseThree")

    def test_instructor_view_user_sections_acceptance(self):
        self.login_as("instructor")
        response = self.client.get("/user_directory.html")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Lab One - CourseOne")
        self.assertNotContains(response, "Lab Two - CourseTwo")
        self.assertContains(response, "Lab Three - CourseThree")

    def test_ta_view_user_sections_acceptance(self):
        self.login_as("ta")
        response = self.client.get("/user_directory.html")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Lab One - CourseOne")
        self.assertNotContains(response, "Lab Two - CourseTwo")
        self.assertContains(response, "Lab Three - CourseThree")



