from django.test import TestCase, Client

from djangoProject1.models import User, Course, Section

class TestCourseFilterAcceptance(TestCase):
    def setUp(self):
        self.client = Client()

        # Create users
        self.ta = User.objects.create(username="ta_user", password="password", role="TA")
        self.instructor = User.objects.create(username="instructor_user", password="password", role="Instructor")
        self.admin = User.objects.create(username="admin_user", password="password", role="Admin")

        # Create courses
        self.course1 = Course.objects.create(name="Course 1")
        self.course2 = Course.objects.create(name="Course 2")
        self.course3 = Course.objects.create(name="Course 3")

        # Assign instructor to course2
        self.course2.instructors.add(self.instructor)

        # Create labs and assign to TA
        self.lab1 = Section.objects.create(name="Lab 1", course=self.course1, ta=self.ta)
        self.lab2 = Section.objects.create(name="Lab 2", course=self.course3, ta=self.ta)

    def test_ta_view_assigned_courses(self):
        self.client.post("/", {"username": "ta_user", "password": "password"}, follow=True)
        response = self.client.get("/course_directory.html")
        self.assertContains(response, "Course 1")
        self.assertContains(response, "Course 2")
        self.assertContains(response, "Course 3")

        response = self.client.get("/course_directory.html?filter=assigned")
        self.assertContains(response, "Course 1")
        self.assertContains(response, "Course 3")
        self.assertNotContains(response, "Course 2")

    def test_instructor_view_assigned_courses(self):
        self.client.post("/", {"username": "instructor_user", "password": "password"}, follow=True)
        response = self.client.get("/course_directory.html")
        self.assertContains(response, "Course 1")
        self.assertContains(response, "Course 2")
        self.assertContains(response, "Course 3")

        response = self.client.get("/course_directory.html?filter=assigned")
        self.assertContains(response, "Course 2")
        self.assertNotContains(response, "Course 1")
        self.assertNotContains(response, "Course 3")

    def test_admin_view_all_courses(self):
        self.client.post("/", {"username": "admin_user", "password": "password"}, follow=True)
        response = self.client.get("/course_directory.html")
        self.assertContains(response, "Course 1")
        self.assertContains(response, "Course 2")
        self.assertContains(response, "Course 3")

        response = self.client.get("/course_directory.html?filter=assigned")
        self.assertContains(response, "Course 1")
        self.assertContains(response, "Course 2")
        self.assertContains(response, "Course 3")