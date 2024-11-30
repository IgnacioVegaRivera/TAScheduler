from django.test import TestCase, Client
from djangoProject1.models import User, Course, Lab


class TestCourseFilterUnit(TestCase):
    def setUp(self):
        # Create users
        self.ta = User.objects.create(username="ta_user", role="TA")
        self.instructor = User.objects.create(username="instructor_user", role="Instructor")
        self.admin = User.objects.create(username="admin_user", role="Admin")

        # Create courses
        self.course1 = Course.objects.create(name="Course 1")
        self.course2 = Course.objects.create(name="Course 2")
        self.course3 = Course.objects.create(name="Course 3")

        # Assign instructor to course2
        self.course2.instructors.add(self.instructor)

        # Create labs and assign to TA
        self.lab1 = Lab.objects.create(name="Lab 1", course=self.course1, ta=self.ta)
        self.lab2 = Lab.objects.create(name="Lab 2", course=self.course3, ta=self.ta)

    def test_filter_for_ta(self):
        assigned_courses = Course.objects.filter(labs__ta=self.ta).distinct()
        self.assertEqual(assigned_courses.count(), 2)
        self.assertIn(self.course1, assigned_courses)
        self.assertIn(self.course3, assigned_courses)
        self.assertNotIn(self.course2, assigned_courses)

    def test_filter_for_instructor(self):
        assigned_courses = self.instructor.courses.all()
        self.assertEqual(assigned_courses.count(), 1)
        self.assertIn(self.course2, assigned_courses)
        self.assertNotIn(self.course1, assigned_courses)
        self.assertNotIn(self.course3, assigned_courses)

    def test_filter_for_admin(self):
        all_courses = Course.objects.all()
        self.assertEqual(all_courses.count(), 3)

    def test_ta_no_assignments(self):
        unassigned_ta = User.objects.create(username="unassigned_ta", role="TA")
        assigned_courses = Course.objects.filter(labs__ta=unassigned_ta).distinct()
        self.assertEqual(assigned_courses.count(), 0)

    def test_instructor_no_assignments(self):
        unassigned_instructor = User.objects.create(username="unassigned_instructor", role="Instructor")
        assigned_courses = unassigned_instructor.courses.all()
        self.assertEqual(assigned_courses.count(), 0)


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
        self.lab1 = Lab.objects.create(name="Lab 1", course=self.course1, ta=self.ta)
        self.lab2 = Lab.objects.create(name="Lab 2", course=self.course3, ta=self.ta)

    def test_ta_view_assigned_courses(self):
        self.client.post("/", {"username": "ta_user", "password": "password"}, follow=True)
        response = self.client.get("/course_Directory.html")
        self.assertContains(response, "Course 1")
        self.assertContains(response, "Course 2")
        self.assertContains(response, "Course 3")

        response = self.client.get("/course_Directory.html?filter=assigned")
        self.assertContains(response, "Course 1")
        self.assertContains(response, "Course 3")
        self.assertNotContains(response, "Course 2")

    def test_instructor_view_assigned_courses(self):
        self.client.post("/", {"username": "instructor_user", "password": "password"}, follow=True)
        response = self.client.get("/course_Directory.html")
        self.assertContains(response, "Course 1")
        self.assertContains(response, "Course 2")
        self.assertContains(response, "Course 3")

        response = self.client.get("/course_Directory.html?filter=assigned")
        self.assertContains(response, "Course 2")
        self.assertNotContains(response, "Course 1")
        self.assertNotContains(response, "Course 3")

    def test_admin_view_all_courses(self):
        self.client.post("/", {"username": "admin_user", "password": "password"}, follow=True)
        response = self.client.get("/course_Directory.html")
        self.assertContains(response, "Course 1")
        self.assertContains(response, "Course 2")
        self.assertContains(response, "Course 3")

        response = self.client.get("/course_Directory.html?filter=assigned")
        self.assertContains(response, "Course 1")
        self.assertContains(response, "Course 2")
        self.assertContains(response, "Course 3")