from django.test import TestCase, Client
from djangoProject1.models import User, Course, Section

class TestConfigureUserUnit(TestCase):
    def setUp(self):
        #create some users
        self.admin = User.objects.create(first_name='Ad', last_name='Min', username='admin',
                                         email='admin@uwm.edu', phone_number="1234567890", role='Admin', skills='Admin skills')
        self.instructor = User.objects.create(first_name='Inst', last_name='Ructor', username='instructor',
                                         email='instructor@uwm.edu', phone_number="0123456789", role='Instructor',skills='Good at teaching')
        self.ta = User.objects.create(first_name='T', last_name='A', username='ta',
                                         email='ta@uwm.edu', phone_number="9876543210", role='TA', skills='Proficient in java')
        self.admin.save()
        self.instructor.save()
        self.ta.save()

        #create some courses/labs
        self.course = Course.objects.create(name="Course 1")
        self.course.save()
        self.course.users.add(self.instructor)

        self.lab = Section.objects.create(name="Lab 1", course=self.course, user=self.ta)
        self.lab.save()

    def test_user_list(self):
        users = User.objects.all()
        self.assertEqual(users.count(), 3)
        self.assertIn(self.admin, users)
        self.assertIn(self.instructor, users)
        self.assertIn(self.ta, users)

    def test_course_list(self):
        courses = Course.objects.all()
        self.assertEqual(courses.count(), 1)
        self.assertIn(self.course, courses)

    def test_lab_list(self):
        labs = Section.objects.all()
        self.assertEqual(labs.count(), 1)
        self.assertIn(self.lab, labs)

    def test_admin_list(self):
        admins = User.objects.filter(role="Admin")
        self.assertEqual(admins.count(), 1)
        self.assertIn(self.admin, admins)

    def test_instructor_list(self):
        instructors = User.objects.filter(role="Instructor")
        self.assertEqual(instructors.count(), 1)
        self.assertIn(self.instructor, instructors)

    def test_ta_list(self):
        tas = User.objects.filter(role="TA")
        self.assertEqual(tas.count(), 1)
        self.assertIn(self.ta, tas)

    def test_admin_display_values(self):
        self.assertEqual(self.admin.role, 'Admin')
        self.assertEqual(self.admin.first_name, 'Ad')
        self.assertEqual(self.admin.last_name, 'Min')
        self.assertEqual(self.admin.email, 'admin@uwm.edu')
        self.assertEqual(self.admin.phone_number, '1234567890')

    def test_admin_courses(self):
        courses = Course.objects.filter(users=self.admin)
        labs = Section.objects.filter(user=self.admin)
        self.assertEqual(courses.count(), 0)
        self.assertEqual(labs.count(), 0)

    def test_instructor_display_values(self):
        self.assertEqual(self.instructor.role, 'Instructor')
        self.assertEqual(self.instructor.first_name, 'Inst')
        self.assertEqual(self.instructor.last_name, 'Ructor')
        self.assertEqual(self.instructor.email, 'instructor@uwm.edu')
        self.assertEqual(self.instructor.phone_number, '0123456789')

    def test_instructor_courses(self):
        courses = Course.objects.filter(users=self.instructor)
        labs = Section.objects.filter(user=self.instructor)
        self.assertEqual(courses.count(), 1)
        self.assertEqual(labs.count(), 0)
        self.assertIn(self.course, courses)

    def test_ta_display_values(self):
        self.assertEqual(self.ta.role, 'TA')
        self.assertEqual(self.ta.first_name, 'T')
        self.assertEqual(self.ta.last_name, 'A')
        self.assertEqual(self.ta.email, 'ta@uwm.edu')
        self.assertEqual(self.ta.phone_number, '9876543210')

    def test_ta_courses(self):
        courses = Course.objects.filter(users=self.ta)
        labs = Section.objects.filter(user=self.ta)
        self.assertEqual(courses.count(), 0)
        self.assertEqual(labs.count(), 1)
        self.assertIn(self.lab, labs)

# class TestConfigureUserAcceptanceTest(TestCase):
#     def setUp(self):
#         self.donkey = Client()
#
#     def admin_user(self):
#         self.admin = User.objects.create(first_name='Ad', last_name='Min', username='admin',
#                                          email='admin@uwm.edu', phone_number="1234567890", role='Admin')
#         self.admin.save()
#
#     #instructor with no courses
#     def instructor_user1(self):
#         self.instructor = User.objects.create(first_name='Inst', last_name='Ructor', username='instructor',
#                                               email='instructor@uwm.edu', phone_number="0123456789", role='Instructor')
#         self.instructor.save()
#
#     #instructor with 1 course
#     def instructor_user2(self):
#         self.instructor = User.objects.create(first_name='Inst', last_name='Ructor', username='instructor',
#                                               email='instructor@uwm.edu', phone_number="0123456789", role='Instructor')
#         self.instructor.save()
#         self.course = Course.objects.create(name="Course 1")
#         self.course.save()
#         self.course.instructors.add(self.instructor)
#
#     #instructor with more than 1 course
#     def instructor_user3(self):
#         self.instructor = User.objects.create(first_name='Inst', last_name='Ructor', username='instructor',
#                                               email='instructor@uwm.edu', phone_number="0123456789", role='Instructor')
#         self.instructor.save()
#         self.course1 = Course.objects.create(name="Course 1")
#         self.course1.save()
#         self.course1.instructors.add(self.instructor)
#         self.course2 = Course.objects.create(name="Course 2")
#         self.course2.save()
#         self.course2.instructors.add(self.instructor)
#
#     def ta_user1(self):
#         self.ta = User.objects.create(first_name='T', last_name='A', username='ta',
#                                       email='ta@uwm.edu', phone_number="9876543210", role='TA')
#         self.ta.save()
#
#     def ta_user2(self):
#         self.ta = User.objects.create(first_name='T', last_name='A', username='ta',
#                                       email='ta@uwm.edu', phone_number="9876543210", role='TA')
#         self.ta.save()
#
#         self.instructor_user2()
#
#         self.lab = Lab.objects.create(name="Lab 1", course=self.course, ta=self.ta)
#         self.lab.save()
#
#     def ta_user3(self):
#         self.ta = User.objects.create(first_name='T', last_name='A', username='ta',
#                                       email='ta@uwm.edu', phone_number="9876543210", role='TA')
#         self.ta.save()
#
#         self.instructor_user2()
#
#         self.lab1 = Lab.objects.create(name="Lab 1", course=self.course, ta=self.ta)
#         self.lab1.save()
#
#         self.lab2 = Lab.objects.create(name="Lab 2", course=self.course, ta=self.ta)
#         self.lab2.save()
#
#     def admin_login(self):
#         self.admin_user()
#         self.donkey.post("/", {"username": "admin", "password": "Default_Password"})
#
#     def test_admin_user_shows(self):
#         self.admin_login()
#         response = self.donkey.get("/configure_user.html")
#         self.assertContains(response, "Ad Min")
#         self.assertContains(response, "Admin")
#         self.assertContains(response, "No Courses.")
#         self.assertContains(response, "admin@uwm.edu")
#         self.assertContains(response, "1234567890")
#         self.assertContains(response, "Edit") #each user will have an edit field
#
#     def test_instructor_user1_shows(self):
#         self.admin_login()
#         self.instructor_user1()
#         response = self.donkey.get("/configure_user.html")
#         self.assertContains(response, "Inst")
#         self.assertContains(response, "Ructor")
#         self.assertContains(response, "Instructor")
#         self.assertContains(response, "No Courses.")
#         self.assertNotContains(response, "Course 1") #other courses aren't printing when we have none
#         self.assertContains(response, "instructor@uwm.edu")
#         self.assertContains(response, "0123456789")
#
#
#     def test_instructor_user2_shows(self):
#         self.admin_login()
#         self.instructor_user2()
#         response = self.donkey.get("/configure_user.html")
#         self.assertContains(response, "Inst")
#         self.assertContains(response, "Ructor")
#         self.assertContains(response, "Instructor")
#         self.assertContains(response, "Course 1")
#         self.assertContains(response, "instructor@uwm.edu")
#         self.assertContains(response, "0123456789")
#
#     def test_instructor_user3_shows(self):
#         self.admin_login()
#         self.instructor_user3()
#         response = self.donkey.get("/configure_user.html")
#         self.assertContains(response, "Inst")
#         self.assertContains(response, "Ructor")
#         self.assertContains(response, "Instructor")
#         self.assertContains(response, "Course 1")
#         self.assertContains(response, "Course 2")
#         self.assertContains(response, "instructor@uwm.edu")
#         self.assertContains(response, "0123456789")
#
#     def test_ta_user1_shows(self):
#         self.admin_login()
#         self.ta_user1()
#         response = self.donkey.get("/configure_user.html")
#         self.assertContains(response, "T")
#         self.assertContains(response, "A")
#         self.assertContains(response, "TA")
#         self.assertContains(response, "No Labs.")
#         self.assertContains(response, "ta@uwm.edu")
#         self.assertContains(response, "9876543210")
#
#     def test_ta_user2_shows(self):
#         self.admin_login()
#         self.ta_user2()
#         response = self.donkey.get("/configure_user.html")
#         self.assertContains(response, "T")
#         self.assertContains(response, "A")
#         self.assertContains(response, "TA")
#         self.assertContains(response, "Lab 1")
#         self.assertContains(response, "ta@uwm.edu")
#         self.assertContains(response, "9876543210")
#
#     def test_ta_user3_shows(self):
#         self.admin_login()
#         self.ta_user3()
#         response = self.donkey.get("/configure_user.html")
#         self.assertContains(response, "T")
#         self.assertContains(response, "A")
#         self.assertContains(response, "TA")
#         self.assertContains(response, "Lab 1")
#         self.assertContains(response, "Lab 2")
#         self.assertContains(response, "ta@uwm.edu")
#         self.assertContains(response, "9876543210")

