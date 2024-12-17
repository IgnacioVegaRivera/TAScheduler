from django.test import TestCase, Client

from djangoProject1.MethodFiles.Administrator import EditCourse
from djangoProject1.models import User, Course, Section


class test_unit_edit_course(TestCase):
    def setUp(self):
        self.client = Client()
        self.temp_user = User(first_name="Jason",
                         last_name="Rock",
                         username="login1",
                         password="password1",
                         email="jason@gmail.com",
                         phone_number="4141234567",
                         address="UWM Campus 123",
                         role="Instructor")

        self.temp_user2 = User(first_name="Bob",
                              last_name="Sorenson",
                              username="login2",
                              password="password2",
                              email="bob@gmail.com",
                              phone_number="4141234568",
                              address="UWM Campus Road 123",
                              role="Instructor")

        self.ta = User(first_name="Akash",
                              last_name="Jammula",
                              username="login3",
                              password="password3",
                              email="akash@gmail.com",
                              phone_number="4141234569",
                              address="UWM Campus Drive 123",
                              role="TA")
        self.temp_user.save()
        self.temp_user2.save()
        self.ta.save()
        self.temp_course = Course(name="CS361")
        self.temp_course.save()
        self.temp_course.users.add(self.temp_user)
        self.temp_course.users.add(self.ta)
        self.lecture = Section(name="Lecture 1", course=self.temp_course, user=self.temp_user)
        self.lab = Section(name="Lab 1", course=self.temp_course, user=self.temp_user)
        self.lecture.save()
        self.lab.save()

        self.temp_course2 = Course(name="CS362")
        self.temp_course2.save()


    def test_unit_editCourseName(self):
        response = self.client.post('/configure_course.html', {'course_id': self.temp_course.id,
                                                         'form_name': 'edit_course',
                                                         'name':"CS431",
                                                         'instructors': [self.temp_user.id],
                                                         'tas':[self.ta.id]})

        self.temp_course.refresh_from_db()
        self.assertEqual(self.temp_course.name, "CS431","Not the correct changed name")

    def test_unit_editCourseNameBlank(self):
        response = self.client.post('/configureCourse', {'course_id': self.temp_course.id,
                                                         'form_name': 'edit_course',
                                                         'name':"",
                                                         'instructors': [self.temp_user.id],
                                                         'tas':[self.ta.id]})
        self.temp_course.refresh_from_db()
        self.assertEqual(self.temp_course.name, "CS361", "Blank Course Name")

    def test_unit_addInstructor(self):
        response = self.client.post('/configure_course.html', {'course_id': self.temp_course.id,
                                                         'form_name': 'edit_course',
                                                         'name':"CS361",
                                                         'instructors': [self.temp_user.id, self.temp_user2.id],
                                                         'tas':[self.ta.id]})
        self.temp_course.refresh_from_db()
        self.assertIn(self.temp_user2, self.temp_course.users.all())
        self.assertEqual(self.lecture.user, self.temp_user, "Blank Instructor Name")
        self.assertIn(self.temp_user, self.temp_course.users.all())
        self.assertIn(self.temp_user2, self.temp_course.users.all())
        self.assertIn(self.ta, self.temp_course.users.all())
        self.assertEqual(len(self.temp_course.users.all()), 3)

    def test_unit_editInstructorName(self):
        response = self.client.post('/configure_course.html', {'course_id': self.temp_course.id,
                                                         'form_name': 'edit_course',
                                                         'name':"CS361",
                                                         'instructors': [self.temp_user2.id],
                                                         'tas':[self.ta.id]})

        self.temp_course.refresh_from_db()
        self.lecture.refresh_from_db()
        self.assertIn(self.temp_user2, self.temp_course.users.all())
        self.assertEqual(self.lecture.user, None, "Blank Instructor Name")
        self.assertIn(self.ta, self.temp_course.users.all())
        self.assertEqual(len(self.temp_course.users.all()), 2)

    def test_remove_all_users(self):
        response = self.client.post('/configure_course.html', {'course_id': self.temp_course.id,
                                                               'form_name': 'edit_course',
                                                               'name': "CS361",
                                                               'instructors': [],
                                                               'tas': []})
        self.temp_course.refresh_from_db()
        self.lecture.refresh_from_db()
        self.lab.refresh_from_db()
        self.assertNotIn(self.temp_user.id, self.temp_course.users.all())
        self.assertNotIn(self.ta, self.temp_course.users.all())
        self.assertEqual(len(self.temp_course.users.all()), 0)
        self.assertEqual(self.lecture.user, None, "Blank Instructor Name")
        self.assertEqual(self.lab.user, None, "Blank TA Name")


