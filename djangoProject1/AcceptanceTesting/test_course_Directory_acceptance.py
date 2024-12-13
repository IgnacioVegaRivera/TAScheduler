from django.test import TestCase, Client

from djangoProject1.models import User, Course, Section

class TestCourseDirectoryAcceptance(TestCase):
    def setUp(self):
        self.donkey = Client()

        # create users
        self.admin = User.objects.create(username="admin", role="Admin", password="password")
        self.instructor = User.objects.create(username="instructor", role="Instructor", password="password")
        self.ta = User.objects.create(username="ta", role="TA", password="password")

        # create courses
        self.course1 = Course.objects.create(name="Course 1")
        self.course2 = Course.objects.create(name="Course 2")
        self.course3 = Course.objects.create(name="Course 3")

        # assign users
        self.course1.users.add(self.instructor, self.ta)
        self.course2.users.add(self.instructor)
        self.course3.users.add(self.ta)

        # create sections
        self.section1 = Section.objects.create(
            name="Section 1",
            course=self.course1,
            days=["Monday", "Wednesday"],
            time="09:00:00",
            location="EMS",
            user=self.ta,
        )
        self.section2 = Section.objects.create(
            name="Section 2",
            course=self.course2,
            days=["Tuesday"],
            time="10:00:00",
            location="Kenwood",
            user=self.instructor,
        )
        self.section3 = Section.objects.create(
            name="Section 3",
            course=self.course3,
            days=["Friday"],
            time="14:00:00",
            location="Physics",
            user=self.ta,
        )

    def login_as(self, username):
        self.donkey.post("/", {"username": username, "password": "password"})

    def test_admin_view_all_courses(self):
        self.login_as("admin")
        response = self.donkey.get("/course_directory.html")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Course 1")
        self.assertContains(response, "Course 2")
        self.assertContains(response, "Course 3")
        self.assertContains(response, "Section 1")
        self.assertContains(response, "Section 2")
        self.assertContains(response, "Section 3")

    def test_instructor_view_all_courses(self):
        self.login_as("instructor")
        response = self.donkey.get("/course_directory.html")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Course 1")
        self.assertContains(response, "Course 2")
        self.assertContains(response, "Course 3")
        self.assertContains(response, "Section 1")
        self.assertContains(response, "Section 2")
        self.assertContains(response, "Section 3")

    def test_ta_view_all_courses(self):
        self.login_as("ta")
        response = self.donkey.get("/course_directory.html")
        self.assertContains(response, "Course 1")
        self.assertContains(response, "Course 2")
        self.assertContains(response, "Course 3")
        self.assertContains(response, "Section 1")
        self.assertContains(response, "Section 3")
        self.assertContains(response, "Section 2")

    def test_course_with_no_section(self):
        self.course4 = Course.objects.create(name="Course 4")
        self.login_as("admin")
        response = self.donkey.get("/course_directory.html")
        self.assertContains(response, "Course 4")

    def test_lab_with_no_ta(self):
        self.login_as("admin")
        response = self.donkey.get("/course_directory.html")
        self.assertContains(response, "Section 2")