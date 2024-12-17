from django.test import TestCase, Client

from djangoProject1.models import User, Course, Section

class TestConfigureUserAcceptanceTest(TestCase):
    def setUp(self):
        self.donkey = Client()

    def admin_user(self):
        self.admin = User.objects.create(first_name='Ad', last_name='Min', username='admin',
                                         email='admin@uwm.edu', phone_number="1234567890", role='Admin')
        self.admin.save()

    #instructor with no courses
    def instructor_user1(self):
        self.instructor = User.objects.create(first_name='Inst', last_name='Ructor', username='instructor',
                                              email='instructor@uwm.edu', phone_number="0123456789", role='Instructor')
        self.instructor.save()

    #instructor with 1 course
    def instructor_user2(self):
        self.instructor = User.objects.create(first_name='Inst', last_name='Ructor', username='instructor',
                                              email='instructor@uwm.edu', phone_number="0123456789", role='Instructor')
        self.instructor.save()
        self.course = Course.objects.create(name="Course 1")
        self.course.save()
        self.course.users.add(self.instructor)

    #instructor with more than 1 course
    def instructor_user3(self):
        self.instructor = User.objects.create(first_name='Inst', last_name='Ructor', username='instructor',
                                              email='instructor@uwm.edu', phone_number="0123456789", role='Instructor')
        self.instructor.save()
        self.course1 = Course.objects.create(name="Course 1")
        self.course1.save()
        self.course1.users.add(self.instructor)
        self.course2 = Course.objects.create(name="Course 2")
        self.course2.save()
        self.course2.users.add(self.instructor)

    def ta_user1(self):
        self.ta = User.objects.create(first_name='T', last_name='A', username='ta',
                                      email='ta@uwm.edu', phone_number="9876543210", role='TA')
        self.ta.save()

    def ta_user2(self):
        self.ta = User.objects.create(first_name='T', last_name='A', username='ta',
                                      email='ta@uwm.edu', phone_number="9876543210", role='TA')
        self.ta.save()

        self.instructor_user2()

        self.lab = Section.objects.create(name="Lab 1", course=self.course, user=self.ta)
        self.lab.save()

    def ta_user3(self):
        self.ta = User.objects.create(first_name='T', last_name='A', username='ta',
                                      email='ta@uwm.edu', phone_number="9876543210", role='TA')
        self.ta.save()

        self.instructor_user2()

        self.lab1 = Section.objects.create(name="Lab 1", course=self.course, user=self.ta)
        self.lab1.save()

        self.lab2 = Section.objects.create(name="Lab 2", course=self.course, user=self.ta)
        self.lab2.save()

    def admin_login(self):
        self.admin_user()
        self.donkey.post("/", {"username": "admin", "password": "Default_Password"})

    def test_admin_user_shows(self):
        self.admin_login()
        response = self.donkey.get("/configure_user.html")
        self.assertContains(response, "Ad Min")
        self.assertContains(response, "Admin")
        self.assertContains(response, "No assignments.")
        self.assertContains(response, "admin@uwm.edu")
        self.assertContains(response, "1234567890")
        self.assertContains(response, "Edit") #each user will have an edit field

    def test_instructor_user1_shows(self):
        self.admin_login()
        self.instructor_user1()
        response = self.donkey.get("/configure_user.html")
        self.assertContains(response, "Inst")
        self.assertContains(response, "Ructor")
        self.assertContains(response, "Instructor")
        self.assertContains(response, "No section assigned.")
        self.assertNotContains(response, "Course 1") #other courses aren't printing when we have none
        self.assertContains(response, "instructor@uwm.edu")
        self.assertContains(response, "0123456789")


    def test_instructor_user2_shows(self):
        self.admin_login()
        self.instructor_user2()
        response = self.donkey.get("/configure_user.html")
        self.assertContains(response, "Inst")
        self.assertContains(response, "Ructor")
        self.assertContains(response, "Instructor")

        self.assertContains(response, "instructor@uwm.edu")
        self.assertContains(response, "0123456789")

    def test_instructor_user3_shows(self):
        self.admin_login()
        self.instructor_user3()
        response = self.donkey.get("/configure_user.html")
        self.assertContains(response, "Inst")
        self.assertContains(response, "Ructor")
        self.assertContains(response, "Instructor")

        self.assertContains(response, "instructor@uwm.edu")
        self.assertContains(response, "0123456789")

    def test_ta_user1_shows(self):
        self.admin_login()
        self.ta_user1()
        response = self.donkey.get("/configure_user.html")
        self.assertContains(response, "T")
        self.assertContains(response, "A")
        self.assertContains(response, "TA")
        self.assertContains(response, "No section assigned.")
        self.assertContains(response, "ta@uwm.edu")
        self.assertContains(response, "9876543210")

    def test_ta_user2_shows(self):
        self.admin_login()
        self.ta_user2()
        response = self.donkey.get("/configure_user.html")
        self.assertContains(response, "T")
        self.assertContains(response, "A")
        self.assertContains(response, "TA")

        self.assertContains(response, "ta@uwm.edu")
        self.assertContains(response, "9876543210")

    def test_ta_user3_shows(self):
        self.admin_login()
        self.ta_user3()
        response = self.donkey.get("/configure_user.html")
        self.assertContains(response, "T")
        self.assertContains(response, "A")
        self.assertContains(response, "TA")

        self.assertContains(response, "ta@uwm.edu")
        self.assertContains(response, "9876543210")