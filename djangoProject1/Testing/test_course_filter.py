from django.test import TestCase, Client
from djangoProject1.models import User, Course, Section


class TestCourseFilterUnit(TestCase):
    def setUp(self):
        # create users
        self.ta = User.objects.create(username="ta_user", role="TA", first_name="TA", last_name="User")
        self.instructor = User.objects.create(username="instructor_user", role="Instructor", first_name="Instructor", last_name="User")
        self.admin = User.objects.create(username="admin_user", role="Admin", first_name="Admin", last_name="User")

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
            days=["Wednesday"], time="10:00:00", location="Room 202"
        )
        self.section3 = Section.objects.create(
            name="Section 3", course=self.course3, user=None,
            days=["Friday"], time="14:00:00", location="Room 303"
        )

    def test_filter_for_ta(self):
        assigned_courses = Course.objects.filter(users=self.ta).distinct()
        self.assertEqual(assigned_courses.count(), 2)
        self.assertIn(self.course1, assigned_courses)
        self.assertIn(self.course3, assigned_courses)
        self.assertNotIn(self.course2, assigned_courses)

    def test_filter_for_instructor(self):
        assigned_courses = Course.objects.filter(users=self.instructor).distinct()
        self.assertEqual(assigned_courses.count(), 2)
        self.assertIn(self.course2, assigned_courses)
        self.assertIn(self.course1, assigned_courses)
        self.assertNotIn(self.course3, assigned_courses)

    def test_filter_for_admin(self):
        all_courses = Course.objects.all()
        self.assertEqual(all_courses.count(), 3)
        self.assertIn(self.course1, all_courses)
        self.assertIn(self.course2, all_courses)
        self.assertIn(self.course3, all_courses)

    def test_ta_no_assignments(self):
        unassigned_ta = User.objects.create(username="unassigned_ta", role="TA")
        assigned_courses = Course.objects.filter(users=unassigned_ta).distinct()
        self.assertEqual(assigned_courses.count(), 0)

    def test_instructor_no_assignments(self):
        unassigned_instructor = User.objects.create(username="unassigned_instructor", role="Instructor")
        assigned_courses = Course.objects.filter(users=unassigned_instructor).distinct()
        self.assertEqual(assigned_courses.count(), 0)

    def test_course_with_no_sections(self):
        course_no_sections = Course.objects.create(name="Course 4")
        sections = Section.objects.filter(course=course_no_sections)
        self.assertEqual(sections.count(), 0)
        self.assertNotIn(self.ta, course_no_sections.users.all())
        self.assertNotIn(self.instructor, course_no_sections.users.all())

    def test_course_with_no_users(self):
        course_no_users = Course.objects.create(name="Course 4")
        self.assertEqual(course_no_users.users.count(), 0)
        self.assertNotIn(self.ta, course_no_users.users.all())
        self.assertNotIn(self.instructor, course_no_users.users.all())