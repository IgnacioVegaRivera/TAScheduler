from django.test import TestCase, Client

from djangoProject1.models import User, Course, Section

class TestCourseDirectoryAcceptance(TestCase):
    def setUp(self):
        self.client = Client()

        # Create users
        self.admin = User.objects.create(username="admin", role="Admin", password="password")
        self.instructor = User.objects.create(username="instructor", role="Instructor", password="password")
        self.ta = User.objects.create(username="ta", role="TA", password="password")

        # Create courses and labs
        self.course1 = Course.objects.create(name="Course 1")
        self.course2 = Course.objects.create(name="Course 2")
        self.course3 = Course.objects.create(name="Course 3")

        # Assign instructors to courses
        self.course1.instructors.add(self.instructor)
        self.course2.instructors.add(self.instructor)

        # Create labs and assign TAs
        self.lab1 = Section.objects.create(name="Lab 1", course=self.course1, ta=self.ta)
        self.lab2 = Section.objects.create(name="Lab 2", course=self.course2, ta=None)
        self.lab3 = Section.objects.create(name="Lab 3", course=self.course3, ta=self.ta)

    def login_as(self, username):
        self.client.post("/", {"username": username, "password": "password"})

    def test_admin_view_all_courses(self):
        self.login_as("admin")
        response = self.client.get("/course_directory.html")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Course 1")
        self.assertContains(response, "Course 2")
        self.assertContains(response, "Course 3")

    def test_instructor_view_all_courses(self):
        self.login_as("instructor")
        response = self.client.get("/course_directory.html")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Course 1")
        self.assertContains(response, "Course 2")
        self.assertContains(response, "Course 3")

    def test_instructor_filter_assigned_courses(self):
        self.login_as("instructor")
        response = self.client.get("/course_directory.html?filter=assigned")
        self.assertContains(response, "Course 1")
        self.assertContains(response, "Course 2")
        self.assertNotContains(response, "Course 3")

    def test_ta_view_all_courses(self):
        self.login_as("ta")
        response = self.client.get("/course_directory.html")
        self.assertContains(response, "Course 1")
        self.assertContains(response, "Course 2")
        self.assertContains(response, "Course 3")

    def test_ta_filter_assigned_courses(self):
        self.login_as("ta")
        response = self.client.get("/course_directory.html?filter=assigned")
        self.assertContains(response, "Course 1")
        self.assertContains(response, "Course 3")
        self.assertNotContains(response, "Course 2")

    def test_course_with_no_labs(self):
        self.course4 = Course.objects.create(name="Course 4")
        self.login_as("admin")
        response = self.client.get("/course_directory.html")
        self.assertContains(response, "Course 4")

    def test_lab_with_no_ta(self):
        self.login_as("admin")
        response = self.client.get("/course_directory.html")
        self.assertContains(response, "Lab 2")