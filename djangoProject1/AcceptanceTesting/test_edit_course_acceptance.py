from django.test import TestCase, Client

from djangoProject1.models import User, Course, Section

class test_acceptance_edit_course(TestCase):
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

    def test_acceptance_editCourseInstructor(self):
        response = self.client.post('/configure_course.html', {'course_id': self.temp_course.id,
                                                        'form_name': 'edit_course',
                                                         'name':"CS361",
                                                         'instructors': [self.temp_user2.id],
                                                         'tas': [self.ta.id]})

        self.temp_course.refresh_from_db()
        self.assertIn(self.temp_user2, self.temp_course.users.all())
        self.assertIn(self.ta, self.temp_course.users.all())
        self.assertEqual(len(self.temp_course.users.all()), 2)
        self.assertEqual(Course.objects.count(), 1)

        self.assertIn('message', response.context)
        self.assertEqual(response.context['message'], "Course 'CS361' was updated successfully.")


    def test_acceptance_editCourseNameInvalid(self):
        response = self.client.post('/configure_course.html', {'course_id': self.temp_course.id,
                                                         'form_name': 'edit_course',
                                                         'name': "",
                                                         'instructors': [self.temp_user2.id],
                                                         'tas': [self.ta.id]})

        self.temp_course.refresh_from_db()
        self.assertIn(self.temp_user, self.temp_course.users.all())
        self.assertIn(self.ta, self.temp_course.users.all())
        self.assertEqual(len(self.temp_course.users.all()), 2)
        self.assertEqual(Course.objects.count(), 1)

        self.assertIn('message', response.context)
        self.assertEqual(response.context['message'], "Failed to update course. Please check your inputs and try again.")

