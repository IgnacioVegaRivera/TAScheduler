import uuid
from datetime import time

from django.test import TestCase, Client
from djangoProject1.MethodFiles.Administrator import EditSection
from djangoProject1.models import User, Course, Section

class test_edit_section(TestCase):
    def setUp(self):
        #create some users
        self.llama = Client()
        self.ta = User(first_name="TA", last_name="Joe", role="TA")
        self.instructor = User(first_name="Instructor", last_name="Jake", role="Instructor")
        self.ta2 = User(first_name="TA", last_name="Josh", role="TA")
        self.instructor2 = User(first_name="Instructor", last_name="Jane", role="Instructor")
        self.ta.save()
        self.instructor.save()
        self.ta2.save()
        self.instructor2.save()

        #create courses
        self.course = Course(name="course 1")
        self.course.save()
        self.course.users.add(self.instructor)
        self.course.users.add(self.ta)
        self.course.users.add(self.instructor2)
        self.course.users.add(self.ta2)
        self.course.refresh_from_db()
        self.course2 = Course(name="course 2")
        self.course2.save()

        self.lab = Section(name="Lab 01", course=self.course, days=["Monday", "Wednesday"], time=time(9, 30),
                           location="Building 123", user=self.ta)
        self.lecture = Section(name="Lecture 01", course=self.course, days=["Tuesday", "Thursday"],
                               time=time(11, 45),location="Building 456", user=self.instructor)
        self.lab.save()
        self.lecture.save()

    def test_edit_section_name(self):
        pass



# class test_unit_edit_lab(TestCase):
#     def setUp(self):
#         self.client = Client()
#         self.temp_user = User(first_name="Jason",
#                          last_name="Rock",
#                          username="login1",
#                          password="password1",
#                          email="<jason@gmail.com>",
#                          phone_number="4141234567",
#                          address="UWM Campus",
#                          role="Instructor")
#
#         self.temp_user_TA = User(first_name="Ryan",
#                          last_name="Reynolds",
#                          username="login2",
#                          password="password2",
#                          email="<ja@gmail.com>",
#                          phone_number="3141234567",
#                          address="UWM Campus",
#                          role="TA")
#         self.temp_user_TA2 = User(first_name="Blake",
#                          last_name="Shelton",
#                          username="login3",
#                          password="password4",
#                          email="<blake@gmail.com>",
#                          phone_number="9141234567",
#                          address="UWM Street",
#                          role="TA")
#
#         self.temp_user.save()
#         self.temp_user_TA.save()
#         self.temp_user_TA2.save()
#         self.temp_course = Course(name="CS361")
#         self.temp_course.save()
#         self.temp_course.users.add(self.temp_user)
#
#         # self.temp_course2 = Course("CS535", self.temp_user)
#         self.temp_course2 = Course(name="CS535")
#         self.temp_course2.save()
#         self.temp_course2.users.add(self.temp_user)
#
#         # self.temp_course3 = Course("CS537", self.temp_user)
#         self.temp_course3 = Course(name="")
#         self.temp_course3.save()
#         self.temp_course3.users.add(self.temp_user)
#
#         self.temp_lab = Section(name="Lab001", course=self.temp_course, ta=self.temp_user_TA)
#
#         self.temp_lab.save()
#         self.temp_course.save()
#         self.temp_course2.save()
#         self.temp_course3.save()
#
#
#
#     def test_unit_EditLabName(self):
#         response = self.client.post('/configure_course.html', {'lab_id': self.temp_lab.id,
#                                                          'form_name' : "edit_lab",
#                                                          'lab': "Lab002",
#                                                          "course":self.temp_course.id,
#                                                          'ta': self.temp_user_TA.id})
#         self.temp_lab.refresh_from_db()
#         self.assertEqual(self.temp_lab.name, "Lab002","The lab name was not successfully changed")
#
#     def test_unit_EditLabNameInvalid(self):
#         response = self.client.post('/configureCourse', {'lab_id': self.temp_lab.id,
#                                                          'form_name': "edit_lab",
#                                                          'lab': "123",
#                                                          "course": self.temp_course.id,
#                                                          'ta': self.temp_user_TA.id})
#         self.temp_lab.refresh_from_db()
#         self.assertEqual(self.temp_lab.name, "Lab001","This is an invalid lab name")
#
#     def test_unit_EditLabNameBlank(self):
#         response = self.client.post('/configureCourse', {'lab_id': self.temp_lab.id,
#                                                          'form_name': "edit_lab",
#                                                          'lab': "",
#                                                          "course": self.temp_course.id,
#                                                          'ta': self.temp_user_TA.id})
#         self.temp_lab.refresh_from_db()
#         self.assertEqual(self.temp_lab.name, "Lab001", "The lab name was changed to blank")
#
#     def test_unit_EditLabCourses(self):
#         response = self.client.post('/configure_course.html', {'lab_id': self.temp_lab.id,
#                                                          'form_name': "edit_lab",
#                                                          'lab': "Lab001",
#                                                          "course":self.temp_course2.id,
#                                                          'ta': self.temp_user_TA.id})
#         self.temp_lab.refresh_from_db()
#         self.assertEqual(self.temp_lab.course.name,"CS535" ,"The course of the lab was not successfully changed")
#
#     def test_unit_EditLabTA(self):
#
#         response = self.client.post('/configure_course.html', {'lab_id': self.temp_lab.id,
#                                                          'form_name': "edit_lab",
#                                                          'lab': "Lab001",
#                                                          "course":self.temp_course.id,
#                                                          'ta': self.temp_user_TA2.id})
#         self.temp_lab.refresh_from_db()
#         self.assertEqual(self.temp_lab.ta.first_name, "Blake")
        #self.assertEqual(response.ta.first_name, self.temp_user_TA2.first_name,"The lab TA did not change")


# class test_acceptance_lab_edit(TestCase):
#     def setUp(self):
#         self.client = Client()
#         self.temp_user = User(first_name="Jason",
#                               last_name="Rock",
#                               username="login1",
#                               password="password1",
#                               email="<jason@gmail.com>",
#                               phone_number="4141234567",
#                               address="UWM Campus",
#                               role="Instructor")
#
#         self.temp_user_TA = User(first_name="Ryan",
#                                  last_name="Reynolds",
#                                  username="login2",
#                                  password="password2",
#                                  email="<ja@gmail.com>",
#                                  phone_number="3141234567",
#                                  address="UWM Campus",
#                                  role="TA")
#         self.temp_user_TA2 = User(first_name="Blake",
#                                   last_name="Shelton",
#                                   username="login3",
#                                   password="password4",
#                                   email="<blake@gmail.com>",
#                                   phone_number="9141234567",
#                                   address="UWM Street",
#                                   role="TA")
#
#         self.temp_user.save()
#         self.temp_user_TA.save()
#         self.temp_user_TA2.save()
#         self.temp_course = Course(name="CS361")
#         self.temp_course.save()
#         self.temp_course.instructors.add(self.temp_user)
#
#         # self.temp_course2 = Course("CS535", self.temp_user)
#         self.temp_course2 = Course(name="CS535")
#         self.temp_course2.save()
#         self.temp_course2.instructors.add(self.temp_user)
#
#         # self.temp_course3 = Course("CS537", self.temp_user)
#         self.temp_course3 = Course(name="")
#         self.temp_course3.save()
#         self.temp_course3.instructors.add(self.temp_user)
#
#         self.temp_lab = Lab(name="Lab001", course=self.temp_course, ta=self.temp_user_TA)
#
#         self.temp_lab.save()
#         self.temp_course.save()
#         self.temp_course2.save()
#         self.temp_course3.save()
#
#
#     def test_acceptance_lab_EditName(self):
#         response = self.client.post('/configure_course.html', {'lab_id': self.temp_lab.id,
#                                                          'form_name': "edit_lab",
#                                                          'lab': "Lab002",
#                                                          "course":self.temp_course.id,
#                                                          'ta': self.temp_user_TA.id})
#         self.temp_lab.refresh_from_db()
#         self.assertEqual(self.temp_lab.name, "Lab002","The lab name was not successfully changed")
#         self.assertEqual(Lab.objects.count(),1)
#         self.assertIn('message', response.context)
#         self.assertEqual(response.context['message'],"Lab \'Lab002\' updated successfully.")
#
#     def test_acceptance_lab_EditNameInvalid(self):
#
#         response = self.client.post('/configure_course.html', {'lab_id': self.temp_lab.id,
#                                                          'form_name': "edit_lab",
#                                                          'lab': "",
#                                                          "course": self.temp_course.id,
#                                                          'ta': self.temp_user_TA.id})
#         self.temp_lab.refresh_from_db()
#         self.assertEqual(self.temp_lab.name, "Lab001", "This is an invalid lab name")
#         self.assertEqual(Lab.objects.count(), 1)
#         self.assertEqual(response.context['message'], "Failed to update lab. Please check your inputs and try again.")
#
#     def test_acceptance_lab_EditCourse(self):
#         response = self.client.post('/configure_course.html', {'lab_id': self.temp_lab.id,
#                                                          'form_name': "edit_lab",
#                                                          'lab': "Lab001",
#                                                          "course": self.temp_course2.id,
#                                                          'ta': self.temp_user_TA.id})
#         self.temp_lab.refresh_from_db()
#         self.assertEqual(self.temp_lab.course.name, "CS535", "The course of the lab was not successfully changed")
#         self.assertEqual(Lab.objects.count(), 1)
#         self.assertEqual(response.context['message'], "Lab \'Lab001\' updated successfully.")
#
#     def test_acceptance_lab_EditLabTA(self):
#
#         response = self.client.post('/configure_course.html', {'lab_id': self.temp_lab.id,
#                                                          'form_name': "edit_lab",
#                                                          'lab': "Lab001",
#                                                          "course": self.temp_course.id,
#                                                          'ta': self.temp_user_TA2.id})
#         self.temp_lab.refresh_from_db()
#         self.assertEqual(self.temp_lab.ta.first_name, "Blake")
#         self.assertEqual(Lab.objects.count(), 1)
#         self.assertEqual(response.context['message'], "Lab 'Lab001' updated successfully.")