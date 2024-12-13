from django.test import TestCase, Client
from djangoProject1.models import User, Course, Section

class TestCourseDirectoryUnit(TestCase):
    def setUp(self):
        # users
        self.admin = User.objects.create(username="admin", role="Admin", first_name="Admin", last_name="User")
        self.instructor = User.objects.create(username="instructor", role="Instructor", first_name="Instructor", last_name="User")
        self.ta = User.objects.create(username="ta", role="TA", first_name="TA", last_name="User")

        # courses
        self.course1 = Course.objects.create(name="Course 1")
        self.course2 = Course.objects.create(name="Course 2")
        self.course3 = Course.objects.create(name="Course 3")

        # users
        self.course1.users.add(self.instructor, self.ta)
        self.course2.users.add(self.instructor)
        self.course3.users.add(self.ta)

        # sections
        self.section1 = Section.objects.create(name="Section 1", course=self.course1, user=self.ta, days=["Monday", "Wednesday"], time="09:00:00")
        self.section2 = Section.objects.create(name="Section 2", course=self.course2, user=None, days=["Tuesday"], time="10:00:00")
        self.section3 = Section.objects.create(name="Section 3", course=self.course3, user=self.ta, days=["Friday"], time="14:00:00")

    def test_admin_view_all_courses(self):
        courses = Course.objects.all()
        self.assertEqual(courses.count(), 3)
        self.assertIn(self.course1, courses)
        self.assertIn(self.course2, courses)
        self.assertIn(self.course3, courses)

    def test_instructor_view_all_courses(self):
        courses = Course.objects.all()
        self.assertEqual(courses.count(), 3)

    def test_instructor_filter_assigned_courses(self):
        assigned_courses = self.instructor.courses.all()
        self.assertEqual(assigned_courses.count(), 2)
        self.assertIn(self.course1, assigned_courses)
        self.assertIn(self.course2, assigned_courses)
        self.assertNotIn(self.course3, assigned_courses)

    def test_ta_view_all_courses(self):
        courses = Course.objects.all()
        self.assertEqual(courses.count(), 3)

    def test_ta_filter_assigned_courses(self):
        assigned_courses = self.ta.courses.all()
        self.assertEqual(assigned_courses.count(), 2)
        self.assertIn(self.course1, assigned_courses)
        self.assertIn(self.course3, assigned_courses)
        self.assertNotIn(self.course2, assigned_courses)

    def test_courses_with_no_labs(self):
        self.course4 = Course.objects.create(name="Course 4")
        labs = self.course4.labs.all()
        self.assertEqual(labs.count(), 0)

    def test_courses_with_no_users(self):
        self.course4 = Course.objects.create(name="Course 4")
        self.assertEqual(self.course4.users.count(), 0)

    def test_sections_with_instructor(self):
        sections_with_instructors = Section.objects.filter(user__role="Instructor")
        self.assertEqual(sections_with_instructors.count(), 1)
        self.assertIn(self.section2, sections_with_instructors)

    def test_sections_with_ta(self):
        sections_with_tas = Section.objects.filter(user__role="TA")
        self.assertEqual(sections_with_tas.count(), 2)
        self.assertIn(self.section1, sections_with_tas)
        self.assertIn(self.section3, sections_with_tas)

    def test_sections_with_no_assigned_user(self):
        unassigned_sections = Section.objects.filter(user=None)
        self.assertEqual(unassigned_sections.count(), 0)

    def test_course_has_sections(self):
        self.assertEqual(self.course1.sections.count(), 1)
        self.assertEqual(self.course2.sections.count(), 1)
        self.assertEqual(self.course3.sections.count(), 1)

    def test_course_without_sections(self):
        course_without_sections = Course.objects.create(name="Course 4")
        self.assertEqual(course_without_sections.sections.count(), 0)

# class TestCourseDirectoryAcceptance(TestCase):
#     def setUp(self):
#         self.client = Client()
#
#         # Create users
#         self.admin = User.objects.create(username="admin", role="Admin", password="password")
#         self.instructor = User.objects.create(username="instructor", role="Instructor", password="password")
#         self.ta = User.objects.create(username="ta", role="TA", password="password")
#
#         # Create courses and labs
#         self.course1 = Course.objects.create(name="Course 1")
#         self.course2 = Course.objects.create(name="Course 2")
#         self.course3 = Course.objects.create(name="Course 3")
#
#         # Assign instructors to courses
#         self.course1.instructors.add(self.instructor)
#         self.course2.instructors.add(self.instructor)
#
#         # Create labs and assign TAs
#         self.lab1 = Lab.objects.create(name="Lab 1", course=self.course1, ta=self.ta)
#         self.lab2 = Lab.objects.create(name="Lab 2", course=self.course2, ta=None)
#         self.lab3 = Lab.objects.create(name="Lab 3", course=self.course3, ta=self.ta)
#
#     def login_as(self, username):
#         self.client.post("/", {"username": username, "password": "password"})
#
#     def test_admin_view_all_courses(self):
#         self.login_as("admin")
#         response = self.client.get("/course_directory.html")
#         self.assertEqual(response.status_code, 200)
#         self.assertContains(response, "Course 1")
#         self.assertContains(response, "Course 2")
#         self.assertContains(response, "Course 3")
#
#     def test_instructor_view_all_courses(self):
#         self.login_as("instructor")
#         response = self.client.get("/course_directory.html")
#         self.assertEqual(response.status_code, 200)
#         self.assertContains(response, "Course 1")
#         self.assertContains(response, "Course 2")
#         self.assertContains(response, "Course 3")
#
#     def test_instructor_filter_assigned_courses(self):
#         self.login_as("instructor")
#         response = self.client.get("/course_directory.html?filter=assigned")
#         self.assertContains(response, "Course 1")
#         self.assertContains(response, "Course 2")
#         self.assertNotContains(response, "Course 3")
#
#     def test_ta_view_all_courses(self):
#         self.login_as("ta")
#         response = self.client.get("/course_directory.html")
#         self.assertContains(response, "Course 1")
#         self.assertContains(response, "Course 2")
#         self.assertContains(response, "Course 3")
#
#     def test_ta_filter_assigned_courses(self):
#         self.login_as("ta")
#         response = self.client.get("/course_directory.html?filter=assigned")
#         self.assertContains(response, "Course 1")
#         self.assertContains(response, "Course 3")
#         self.assertNotContains(response, "Course 2")
#
#     def test_course_with_no_labs(self):
#         self.course4 = Course.objects.create(name="Course 4")
#         self.login_as("admin")
#         response = self.client.get("/course_directory.html")
#         self.assertContains(response, "Course 4")
#
#     def test_lab_with_no_ta(self):
#         self.login_as("admin")
#         response = self.client.get("/course_directory.html")
#         self.assertContains(response, "Lab 2")