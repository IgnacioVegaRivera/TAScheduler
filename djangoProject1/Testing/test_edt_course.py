from django.test import TestCase, Client

from djangoProject1.MethodFiles.Administrator import EditCourse
from djangoProject1.models import User, Course


class test_unit_edit_course(TestCase):
    def setUp(self):
        self.client = Client()
        self.temp_user = User(first_name="Jason",
                         last_name="Rock",
                         username="login1",
                         password="password1",
                         email="<jason@gmail.com>",
                         phone_number="4141234567",
                         address="UWM Campus",
                         role="Instructor")

        self.temp_user2 = User(first_name="Bob",
                              last_name="Sorenson",
                              username="login2",
                              password="password2",
                              email="<bob@gmail.com>",
                              phone_number="4141234568",
                              address="UWM Campus Road",
                              role="Instructor")
        self.temp_course = Course("CS361", self.temp_user)
        self.temp_user.save()
        self.temp_user2.save()
        self.temp_course.save()

    def test_unit_editCourseName(self):
        response = self.client.post('/configureCourse', {'id': self.temp_course.id,
                                                         'course':"CS431",
                                                         'instructor': self.temp_user})

        self.temp_course.refresh_from_db()
        self.assertEqual(self.temp_course.name, "CS431","Not the correct changed name")

    def test_unit_editCourseNameBlank(self):
        response = self.client.post('/configureCourse', {'id': self.temp_course.id,
                                                         'course':"",
                                                         'instructor': self.temp_user})
        self.temp_course.refresh_from_db()
        self.assertEqual(self.temp_course.name, "CS361", "Blank Course Name")

    def test_unit_editCourseNameInvalid(self):
        response = self.client.post('/configureCourse', {'id': self.temp_course.id,
                                                         'course':"123",
                                                         'instructor': self.temp_user})
        self.temp_course.refresh_from_db()
        self.assertEqual(self.temp_course.name, "CS361", "Not the correct changed name")


    def test_unit_editInstructorName(self):
        response = self.client.post('/configureCourse', {'id': self.temp_course.id,
                                                         'course':"CS361",
                                                         'instructor': self.temp_user2})

        self.temp_course.refresh_from_db()
        self.assertEqual(self.temp_course.instructors,self.temp_user2,"Not the correct changed instructor(s)")

    def test_unit_editInstructorNameInvalid(self):
        response = self.client.post('/configureCourse', {'id': self.temp_course.id,
                                                         'course':"",
                                                         'instructor': self.temp_user2})

        self.temp_course.refresh_from_db()
        self.assertEqual(self.temp_course.instructors,self.temp_user,"Not the correct changed instructor(s)")

class test_acceptance_edit_course(TestCase):
    def setUp(self):
        self.client = Client()
        self.temp_user = User(first_name="Jason",
                         last_name="Rock",
                         username="login1",
                         password="password1",
                         email="<jason@gmail.com>",
                         phone_number="4141234567",
                         address="UWM Campus",
                         role="Instructor")

        self.temp_user2 = User(first_name="Bob",
                              last_name="Sorenson",
                              username="login2",
                              password="password2",
                              email="<bob@gmail.com>",
                              phone_number="4141234568",
                              address="UWM Campus Road",
                              role="Instructor")
        self.temp_course = Course("CS361", self.temp_user)
        self.temp_user.save()
        self.temp_user2.save()
        self.temp_course.save()

    def test_acceptance_editCourseName(self):
        response = self.client.post('/configureCourse', {'id': self.temp_course.id,
                                                         'course': "CS431",
                                                         'instructor': self.temp_user})

        self.temp_course.refresh_from_db()
        self.assertEqual(self.temp_course.name, "CS431", "Not the correct changed name")
        self.assertEqual(Course.objects.count(),1)
        self.assertEqual(response.context['message'], "Failed to update course. Please check your inputs and try again.")

    def test_acceptance_editCourseNameInvalid(self):
        response = self.client.post('/configureCourse', {'id': self.temp_course.id,
                                                         'course': "123",
                                                         'instructor': self.temp_user})
        self.temp_course.refresh_from_db()
        self.assertEqual(self.temp_course.name, "CS361", "Not the correct changed name")
        self.assertEqual(Course.objects.count(), 0)
        self.assertEqual(response.context['message'], "Failed to update course. Please check your inputs and try again.")

    def test_acceptance_editCourseInstructor(self):
        response = self.client.post('/configureCourse', {'id': self.temp_course.id,
                                                         'course':"CS361",
                                                         'instructor': self.temp_user2})

        self.temp_course.refresh_from_db()
        self.assertEqual(self.temp_course.instructors,self.temp_user2,"Not the correct changed instructor(s)")
        self.assertEqual(Course.objects.count(), 1)
        self.assertEqual(response.context['message'],
                         "Failed to update course. Please check your inputs and try again.")

    def test_acceptance_editCourseInstructorInvalid(self):
        response = self.client.post('/configureCourse', {'id': self.temp_course.id,
                                                         'course': "",
                                                         'instructor': self.temp_user2})

        self.temp_course.refresh_from_db()
        self.assertEqual(self.temp_course.instructors, self.temp_user, "Not the correct changed instructor(s)")
        self.assertEqual(Course.objects.count(), 0)
        self.assertEqual(response.context['message'],
                         "Failed to update course. Please check your inputs and try again.")