import uuid
from datetime import time

from django.test import TestCase, Client
from djangoProject1.MethodFiles.Administrator import EditSection
from djangoProject1.models import User, Course, Section

class EditSectionUnitTest(TestCase):
    def setUp(self):
        #create some users
        self.llama = Client()
        self.ta = User(username="ta1", first_name="TA", last_name="Joe", role="TA")
        self.instructor = User(username="instructor1", first_name="Instructor", last_name="Jake", role="Instructor")
        self.ta2 = User(username="ta2", first_name="TA", last_name="Josh", role="TA")
        self.instructor2 = User(username="instructor2", first_name="Instructor", last_name="Jane", role="Instructor")
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
        self.course2.users.add(self.instructor2)
        self.course2.users.add(self.ta2)

        self.lab = Section(name="Lab 01", course=self.course, days=["Monday", "Wednesday"], time=time(9, 30),
                           location="Building 123", user=self.ta)
        self.lecture = Section(name="Lecture 01", course=self.course, days=["Tuesday", "Thursday"],
                               time=time(11, 45),location="Building 456", user=self.instructor)
        self.lab.save()
        self.lecture.save()

    #section name tests
    def test_edit_section_name(self):
        response = self.llama.post("/configure_course.html",{'form_name':"edit_section",
                                   'section_id': self.lab.id, 'section_name':"Lab 02",'section_course':self.course,
                                   'section_days' : ["Monday", "Wednesday"], 'section_time': time(9, 30),
                                   'section_location': "Building 123", 'section_user':self.ta.id})
        self.lab.refresh_from_db()
        self.assertEqual(self.lab.name,"Lab 02")
        self.assertEqual(self.lab.course, self.course)
        self.assertEqual(self.lab.days,["Monday", "Wednesday"])
        self.assertEqual(self.lab.time,time(9, 30))
        self.assertEqual(self.lab.location,"Building 123")
        self.assertEqual(self.lab.user, self.ta)

    #don't change anything if the section type and user type don't match
    def test_edit_section_type_and_not_user(self):
        response = self.llama.post("/configure_course.html",{'form_name':"edit_section",
                                   'section_id': self.lab.id, 'section_name':"Lecture 02",'section_course':self.course,
                                   'section_days' : ["Monday", "Wednesday"], 'section_time': time(9, 30),
                                   'section_location': "Building 123", 'section_user':self.ta.id})
        self.lab.refresh_from_db()
        self.assertEqual(self.lab.name, "Lab 01")
        self.assertEqual(self.lab.course, self.course)
        self.assertEqual(self.lab.days, ["Monday", "Wednesday"])
        self.assertEqual(self.lab.time, time(9, 30))
        self.assertEqual(self.lab.location, "Building 123")
        self.assertEqual(self.lab.user, self.ta)

    def test_edit_section_type_and_remove_user(self):
        response = self.llama.post("/configure_course.html",{'form_name':"edit_section",
                                   'section_id': self.lab.id, 'section_name':"Lecture 02",'section_course':self.course,
                                   'section_days' : ["Monday", "Wednesday"], 'section_time': time(9, 30),
                                   'section_location': "Building 123", 'section_user':""})
        self.lab.refresh_from_db()
        self.assertEqual(self.lab.name, "Lecture 02")
        self.assertEqual(self.lab.course, self.course)
        self.assertEqual(self.lab.days, ["Monday", "Wednesday"])
        self.assertEqual(self.lab.time, time(9, 30))
        self.assertEqual(self.lab.location, "Building 123")
        self.assertEqual(self.lab.user, None)

    def test_edit_section_type_and_user(self):
        response = self.llama.post("/configure_course.html",{'form_name':"edit_section",
                                   'section_id': self.lab.id, 'section_name':"Lecture 02",'section_course':self.course,
                                   'section_days' : ["Monday", "Wednesday"], 'section_time': time(9, 30),
                                   'section_location': "Building 123", 'section_user': self.instructor.id})
        self.lab.refresh_from_db()
        self.assertEqual(self.lab.name, "Lecture 02")
        self.assertEqual(self.lab.course, self.course)
        self.assertEqual(self.lab.days, ["Monday", "Wednesday"])
        self.assertEqual(self.lab.time, time(9, 30))
        self.assertEqual(self.lab.location, "Building 123")
        self.assertEqual(self.lab.user, self.instructor)

    #don't change anything
    def test_blank_name(self):
        response = self.llama.post("/configure_course.html", {'form_name': "edit_section",
                                   'section_id': self.lab.id, 'section_name': "", 'section_course': self.course,
                                   'section_days': ["Monday", "Wednesday"], 'section_time': time(9, 30),
                                   'section_location': "Building 123", 'section_user': self.ta.id})
        self.lab.refresh_from_db()
        self.assertEqual(self.lab.name, "Lab 01")
        self.assertEqual(self.lab.course, self.course)
        self.assertEqual(self.lab.days, ["Monday", "Wednesday"])
        self.assertEqual(self.lab.time, time(9, 30))
        self.assertEqual(self.lab.location, "Building 123")
        self.assertEqual(self.lab.user, self.ta)

    def test_invalid_name(self):
        response = self.llama.post("/configure_course.html", {'form_name': "edit_section",
                                                               'section_id': self.lab.id, 'section_name': "section name",
                                                               'section_course': self.course,
                                                               'section_days': ["Monday", "Wednesday"],
                                                               'section_time': time(9, 30),
                                                               'section_location': "Building 123",
                                                               'section_user': self.ta.id})
        self.lab.refresh_from_db()
        self.assertEqual(self.lab.name, "Lab 01")
        self.assertEqual(self.lab.course, self.course)
        self.assertEqual(self.lab.days, ["Monday", "Wednesday"])
        self.assertEqual(self.lab.time, time(9, 30))
        self.assertEqual(self.lab.location, "Building 123")
        self.assertEqual(self.lab.user, self.ta)

    def test_multiple_types(self):
        response = self.llama.post("/configure_course.html", {'form_name': "edit_section",
                                                               'section_id': self.lab.id,
                                                               'section_name': "Lab Lecture 1",
                                                               'section_course': self.course,
                                                               'section_days': ["Monday", "Wednesday"],
                                                               'section_time': time(9, 30),
                                                               'section_location': "Building 123",
                                                               'section_user': self.ta.id})
        self.lab.refresh_from_db()
        self.assertEqual(self.lab.name, "Lab 01")
        self.assertEqual(self.lab.course, self.course)
        self.assertEqual(self.lab.days, ["Monday", "Wednesday"])
        self.assertEqual(self.lab.time, time(9, 30))
        self.assertEqual(self.lab.location, "Building 123")
        self.assertEqual(self.lab.user, self.ta)


    #edit course tests
    def test_edit_course_and_remove_user(self):
        response = self.llama.post("/configure_course.html", {'form_name': "edit_section",
                                                               'section_id': self.lab.id,
                                                               'section_name': "Lab 01",
                                                               'section_course': self.course2,
                                                               'section_days': ["Monday", "Wednesday"],
                                                               'section_time': time(9, 30),
                                                               'section_location': "Building 123",
                                                               'section_user': ""})
        self.lab.refresh_from_db()
        self.assertEqual(self.lab.name, "Lab 01")
        self.assertEqual(self.lab.course, self.course2)
        self.assertEqual(self.lab.days, ["Monday", "Wednesday"])
        self.assertEqual(self.lab.time, time(9, 30))
        self.assertEqual(self.lab.location, "Building 123")
        self.assertEqual(self.lab.user, None)

    def test_edit_course_and_keep_user(self):
        response = self.llama.post("/configure_course.html", {'form_name': "edit_section",
                                                               'section_id': self.lab.id,
                                                               'section_name': "Lab 01",
                                                               'section_course': self.course2,
                                                               'section_days': ["Monday", "Wednesday"],
                                                               'section_time': time(9, 30),
                                                               'section_location': "Building 123",
                                                               'section_user': self.ta.id})
        self.lab.refresh_from_db()
        self.assertEqual(self.lab.name, "Lab 01")
        self.assertEqual(self.lab.course, self.course) #ta is not in course2
        self.assertEqual(self.lab.days, ["Monday", "Wednesday"])
        self.assertEqual(self.lab.time, time(9, 30))
        self.assertEqual(self.lab.location, "Building 123")
        self.assertEqual(self.lab.user, self.ta)

    def test_no_course(self):
        response = self.llama.post("/configure_course.html", {'form_name': "edit_section",
                                                               'section_id': self.lab.id,
                                                               'section_name': "Lab 01",
                                                               'section_course': "",
                                                               'section_days': ["Monday", "Wednesday"],
                                                               'section_time': time(9, 30),
                                                               'section_location': "Building 123",
                                                               'section_user': self.ta.id})
        self.lab.refresh_from_db()
        self.assertEqual(self.lab.name, "Lab 01")
        self.assertEqual(self.lab.course, self.course)
        self.assertEqual(self.lab.days, ["Monday", "Wednesday"])
        self.assertEqual(self.lab.time, time(9, 30))
        self.assertEqual(self.lab.location, "Building 123")
        self.assertEqual(self.lab.user, self.ta)

    def test_change_course_and_user(self):
        response = self.llama.post("/configure_course.html", {'form_name': "edit_section",
                                                              'section_id': self.lab.id,
                                                              'section_name': "Lab 01",
                                                              'section_course': self.course2,
                                                              'section_days': ["Monday", "Wednesday"],
                                                              'section_time': time(9, 30),
                                                              'section_location': "Building 123",
                                                              'section_user': self.ta2.id})
        self.lab.refresh_from_db()
        self.assertEqual(self.lab.name, "Lab 01")
        self.assertEqual(self.lab.course, self.course2)
        self.assertEqual(self.lab.days, ["Monday", "Wednesday"])
        self.assertEqual(self.lab.time, time(9, 30))
        self.assertEqual(self.lab.location, "Building 123")
        self.assertEqual(self.lab.user, self.ta2)

    #edit days tests
    def test_remove_one_day(self):
        response = self.llama.post("/configure_course.html", {'form_name': "edit_section",
                                                              'section_id': self.lab.id,
                                                              'section_name': "Lab 01",
                                                              'section_course': self.course,
                                                              'section_days': ["Monday"],
                                                              'section_time': time(9, 30),
                                                              'section_location': "Building 123",
                                                              'section_user': self.ta.id})
        self.lab.refresh_from_db()
        self.assertEqual(self.lab.name, "Lab 01")
        self.assertEqual(self.lab.course, self.course)
        self.assertEqual(self.lab.days, ["Monday"])
        self.assertEqual(self.lab.time, time(9, 30))
        self.assertEqual(self.lab.location, "Building 123")
        self.assertEqual(self.lab.user, self.ta)

    def test_remove_all_days(self):
        response = self.llama.post("/configure_course.html", {'form_name': "edit_section",
                                                              'section_id': self.lab.id,
                                                              'section_name': "Lab 01",
                                                              'section_course': self.course,
                                                              'section_days': [],
                                                              'section_time': time(9, 30),
                                                              'section_location': "Building 123",
                                                              'section_user': self.ta.id})
        self.lab.refresh_from_db()
        self.assertEqual(self.lab.name, "Lab 01")
        self.assertEqual(self.lab.course, self.course)
        self.assertEqual(self.lab.days, [])
        self.assertEqual(self.lab.time, time(9, 30))
        self.assertEqual(self.lab.location, "Building 123")
        self.assertEqual(self.lab.user, self.ta)

    def test_add_days(self):
        response = self.llama.post("/configure_course.html", {'form_name': "edit_section",
                                                              'section_id': self.lab.id,
                                                              'section_name': "Lab 01",
                                                              'section_course': self.course,
                                                              'section_days': ["Monday", "Wednesday", "Friday"],
                                                              'section_time': time(9, 30),
                                                              'section_location': "Building 123",
                                                              'section_user': self.ta.id})
        self.lab.refresh_from_db()
        self.assertEqual(self.lab.name, "Lab 01")
        self.assertEqual(self.lab.course, self.course)
        self.assertEqual(self.lab.days, ["Monday", "Wednesday", "Friday"])
        self.assertEqual(self.lab.time, time(9, 30))
        self.assertEqual(self.lab.location, "Building 123")
        self.assertEqual(self.lab.user, self.ta)

    def test_invalid_day_name(self):
        response = self.llama.post("/configure_course.html", {'form_name': "edit_section",
                                                              'section_id': self.lab.id,
                                                              'section_name': "Lab 01",
                                                              'section_course': self.course,
                                                              'section_days': ["Monday", "Wednesday", "friday"],
                                                              'section_time': time(9, 30),
                                                              'section_location': "Building 123",
                                                              'section_user': self.ta.id})
        self.lab.refresh_from_db()
        self.assertEqual(self.lab.name, "Lab 01")
        self.assertEqual(self.lab.course, self.course)
        self.assertEqual(self.lab.days, ["Monday", "Wednesday"])
        self.assertEqual(self.lab.time, time(9, 30))
        self.assertEqual(self.lab.location, "Building 123")
        self.assertEqual(self.lab.user, self.ta)

    #change time tests
    def test_change_time(self):
        response = self.llama.post("/configure_course.html", {'form_name': "edit_section",
                                                              'section_id': self.lab.id,
                                                              'section_name': "Lab 01",
                                                              'section_course': self.course,
                                                              'section_days': ["Monday", "Wednesday"],
                                                              'section_time': time(12, 0),
                                                              'section_location': "Building 123",
                                                              'section_user': self.ta.id})
        self.lab.refresh_from_db()
        self.assertEqual(self.lab.name, "Lab 01")
        self.assertEqual(self.lab.course, self.course)
        self.assertEqual(self.lab.days, ["Monday", "Wednesday"])
        self.assertEqual(self.lab.time, time(12, 0))
        self.assertEqual(self.lab.location, "Building 123")
        self.assertEqual(self.lab.user, self.ta)

    def test_no_time(self):
        response = self.llama.post("/configure_course.html", {'form_name': "edit_section",
                                                              'section_id': self.lab.id,
                                                              'section_name': "Lab 01",
                                                              'section_course': self.course,
                                                              'section_days': ["Monday", "Wednesday"],
                                                              'section_time': "",
                                                              'section_location': "Building 123",
                                                              'section_user': self.ta.id})
        self.lab.refresh_from_db()
        self.assertEqual(self.lab.name, "Lab 01")
        self.assertEqual(self.lab.course, self.course)
        self.assertEqual(self.lab.days, ["Monday", "Wednesday"])
        self.assertEqual(self.lab.time, None)
        self.assertEqual(self.lab.location, "Building 123")
        self.assertEqual(self.lab.user, self.ta)

    #change location tests
    def test_change_location(self):
        response = self.llama.post("/configure_course.html", {'form_name': "edit_section",
                                                              'section_id': self.lab.id,
                                                              'section_name': "Lab 01",
                                                              'section_course': self.course,
                                                              'section_days': ["Monday", "Wednesday"],
                                                              'section_time': time(9, 30),
                                                              'section_location': "Building 555",
                                                              'section_user': self.ta.id})
        self.lab.refresh_from_db()
        self.assertEqual(self.lab.name, "Lab 01")
        self.assertEqual(self.lab.course, self.course)
        self.assertEqual(self.lab.days, ["Monday", "Wednesday"])
        self.assertEqual(self.lab.time, time(9, 30))
        self.assertEqual(self.lab.location, "Building 555")
        self.assertEqual(self.lab.user, self.ta)

    def test_no_room_number(self):
        response = self.llama.post("/configure_course.html", {'form_name': "edit_section",
                                                              'section_id': self.lab.id,
                                                              'section_name': "Lab 01",
                                                              'section_course': self.course,
                                                              'section_days': ["Monday", "Wednesday"],
                                                              'section_time': time(9, 30),
                                                              'section_location': "Building",
                                                              'section_user': self.ta.id})
        self.lab.refresh_from_db()
        self.assertEqual(self.lab.name, "Lab 01")
        self.assertEqual(self.lab.course, self.course)
        self.assertEqual(self.lab.days, ["Monday", "Wednesday"])
        self.assertEqual(self.lab.time, time(9, 30))
        self.assertEqual(self.lab.location, "Building 123")
        self.assertEqual(self.lab.user, self.ta)

    def test_no_building_name(self):
        response = self.llama.post("/configure_course.html", {'form_name': "edit_section",
                                                              'section_id': self.lab.id,
                                                              'section_name': "Lab 01",
                                                              'section_course': self.course,
                                                              'section_days': ["Monday", "Wednesday"],
                                                              'section_time': time(9, 30),
                                                              'section_location': "",
                                                              'section_user': self.ta.id})
        self.lab.refresh_from_db()
        self.assertEqual(self.lab.name, "Lab 01")
        self.assertEqual(self.lab.course, self.course)
        self.assertEqual(self.lab.days, ["Monday", "Wednesday"])
        self.assertEqual(self.lab.time, time(9, 30))
        self.assertEqual(self.lab.location, "")
        self.assertEqual(self.lab.user, self.ta)

    #edit user tests that weren't already covered above
    def test_edit_user(self):
        response = self.llama.post("/configure_course.html", {'form_name': "edit_section",
                                                              'section_id': self.lab.id,
                                                              'section_name': "Lab 01",
                                                              'section_course': self.course,
                                                              'section_days': ["Monday", "Wednesday"],
                                                              'section_time': time(9, 30),
                                                              'section_location': "Building 123",
                                                              'section_user': self.ta2.id})
        self.lab.refresh_from_db()
        self.assertEqual(self.lab.name, "Lab 01")
        self.assertEqual(self.lab.course, self.course)
        self.assertEqual(self.lab.days, ["Monday", "Wednesday"])
        self.assertEqual(self.lab.time, time(9, 30))
        self.assertEqual(self.lab.location, "Building 123")
        self.assertEqual(self.lab.user, self.ta2)

    def test_user_type_mismatch(self):
        response = self.llama.post("/configure_course.html", {'form_name': "edit_section",
                                                              'section_id': self.lab.id,
                                                              'section_name': "Lab 01",
                                                              'section_course': self.course,
                                                              'section_days': ["Monday", "Wednesday"],
                                                              'section_time': time(9, 30),
                                                              'section_location': "Building 123",
                                                              'section_user': self.instructor.id})
        self.lab.refresh_from_db()
        self.assertEqual(self.lab.name, "Lab 01")
        self.assertEqual(self.lab.course, self.course)
        self.assertEqual(self.lab.days, ["Monday", "Wednesday"])
        self.assertEqual(self.lab.time, time(9, 30))
        self.assertEqual(self.lab.location, "Building 123")
        self.assertEqual(self.lab.user, self.ta)

    #misc tests
    def test_matching_name_and_course(self):
        response = self.llama.post("/configure_course.html", {'form_name': "edit_section",
                                                              'section_id': self.lab.id,
                                                              'section_name': "Lecture 01",
                                                              'section_course': self.course,
                                                              'section_days': ["Monday", "Wednesday"],
                                                              'section_time': time(9, 30),
                                                              'section_location': "Building 123",
                                                              'section_user': self.instructor.id})
        self.lab.refresh_from_db()
        self.assertEqual(self.lab.name, "Lab 01")
        self.assertEqual(self.lab.course, self.course)
        self.assertEqual(self.lab.days, ["Monday", "Wednesday"])
        self.assertEqual(self.lab.time, time(9, 30))
        self.assertEqual(self.lab.location, "Building 123")
        self.assertEqual(self.lab.user, self.ta)

    #a section can have the same name as another if it is in a different course
    def test_matching_name_different_course(self):
        response = self.llama.post("/configure_course.html", {'form_name': "edit_section",
                                                              'section_id': self.lab.id,
                                                              'section_name': "Lecture 01",
                                                              'section_course': self.course2,
                                                              'section_days': ["Monday", "Wednesday"],
                                                              'section_time': time(9, 30),
                                                              'section_location': "Building 123",
                                                              'section_user': self.instructor2.id})
        self.lab.refresh_from_db()
        self.assertEqual(self.lab.name, "Lecture 01")
        self.assertEqual(self.lab.course, self.course2)
        self.assertEqual(self.lab.days, ["Monday", "Wednesday"])
        self.assertEqual(self.lab.time, time(9, 30))
        self.assertEqual(self.lab.location, "Building 123")
        self.assertEqual(self.lab.user, self.instructor2)

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