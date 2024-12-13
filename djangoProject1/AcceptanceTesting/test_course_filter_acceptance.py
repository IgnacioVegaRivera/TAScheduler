from django.test import TestCase, Client

from djangoProject1.models import User, Course, Section

class TestCourseFilterAcceptance(TestCase):
    def setUp(self):
        self.donkey = Client()

        # create users
        self.ta = User.objects.create(username="ta_user", password="password", role="TA", first_name="TA", last_name="User")
        self.instructor = User.objects.create(username="instructor_user", password="password", role="Instructor", first_name="Instructor", last_name="User")
        self.admin = User.objects.create(username="admin_user", password="password", role="Admin", first_name="Admin", last_name="User")

        # create courses
        self.course1 = Course.objects.create(name="Course 1")
        self.course2 = Course.objects.create(name="Course 2")
        self.course3 = Course.objects.create(name="Course 3")

        # assign users
        self.course1.users.add(self.ta, self.instructor)
        self.course2.users.add(self.instructor)
        self.course3.users.add(self.ta)

        # create sections
        self.section1 = Section.objects.create(
            name="Section 1", course=self.course1, user=self.ta,
            days=["Monday"], time="09:00:00", location="Room 101"
        )
        self.section2 = Section.objects.create(
            name="Section 2", course=self.course2, user=self.instructor,
            days=["Tuesday"], time="10:00:00", location="Room 202"
        )
        self.section3 = Section.objects.create(
            name="Section 3", course=self.course3, user=None,
            days=["Friday"], time="14:00:00", location="Room 303"
        )

    def login_as(self, username):
        self.donkey.post("/", {"username": username, "password": "password"}, follow=True)

    def test_ta_view_assigned_courses(self):
        self.login_as("ta_user")
        response = self.donkey.get("/course_directory.html")
        self.assertContains(response, "Course 1")
        self.assertContains(response, "Course 2")
        self.assertContains(response, "Course 3")

        response = self.donkey.get("/course_directory.html?filter=assigned")
        self.assertContains(response, "Course 1")
        self.assertContains(response, "Course 3")
        self.assertNotContains(response, "Course 2")

    def test_instructor_view_assigned_courses(self):
        self.login_as("instructor_user")
        response = self.donkey.get("/course_directory.html")
        self.assertContains(response, "Course 1")
        self.assertContains(response, "Course 2")
        self.assertContains(response, "Course 3")

        response = self.donkey.get("/course_directory.html?filter=assigned")
        self.assertContains(response, "Course 2")
        self.assertContains(response, "Course 1")
        self.assertNotContains(response, "Course 3")

    def test_admin_view_all_courses(self):
        self.login_as("admin_user")
        response = self.donkey.get("/course_directory.html")
        self.assertContains(response, "Course 1")
        self.assertContains(response, "Course 2")
        self.assertContains(response, "Course 3")

        response = self.donkey.get("/course_directory.html?filter=assigned")
        # admin should see all
        self.assertContains(response, "Course 1")
        self.assertContains(response, "Course 2")
        self.assertContains(response, "Course 3")