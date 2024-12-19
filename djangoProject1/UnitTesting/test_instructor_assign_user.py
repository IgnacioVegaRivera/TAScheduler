from django.test import TestCase, Client
from djangoProject1.models import User, Course, Section

class TestInstructorAssignUserUnit(TestCase):
    def setUp(self):
        self.donkey = Client()
        self.admin = User.objects.create(first_name='Ad', last_name='Min', username='admin', password='password',
            email='admin@uwm.edu', phone_number="1234567890", address='313 W Street', skills='Admin skills', role='Admin')
        self.instructor = User.objects.create(first_name='Inst', last_name='Ructor', username='instructor',
            password='password',email='instructor@uwm.edu', phone_number="0123456789",address='404 Your Moms House',
            skills='Good at teaching', role='Instructor')
        self.ta = User.objects.create(first_name='T', last_name='A', username='ta', password='password', email='ta@uwm.edu',
            phone_number='6061912020', address='909 Next Door', skills='Proficient in java', role='TA')
        self.ta2 = User.objects.create(first_name='Tee', last_name='Aye', username='ta2', password='password',
                                      email='ta2@uwm.edu',
                                      phone_number='6161912020', address='919 Next Door', skills='Proficient in js',
                                      role='TA')

        # Save Users
        self.admin.save()
        self.instructor.save()
        self.ta.save()
        self.ta2.save()

        # Create courses for testing
        self.courseOne = Course.objects.create(name="Course1")
        self.courseTwo = Course.objects.create(name="Course2")
        self.courseThree = Course.objects.create(name="Course3")

        # Save courses
        self.courseOne.save()
        self.courseTwo.save()
        self.courseThree.save()

        # Create labs and assign TAs
        self.courseOne.users.add(self.instructor)
        self.courseOne.users.add(self.ta)
        self.courseOne.users.add(self.ta2)
        self.courseTwo.users.add(self.instructor)
        self.courseThree.users.add(self.ta)

        self.lectureOne = Section.objects.create(name="Lecture 1", course=self.courseTwo)
        self.lectureTwo = Section.objects.create(name="Lecture 2", course=self.courseThree)

        self.labOne = Section.objects.create(name="Lab 1", course=self.courseOne, days="Monday", time="3:00",
                                             location="EMS", user=None)
        self.labTwo = Section.objects.create(name="Lab 2", course=self.courseTwo, days="Wednesday", time="12:00",
                                             location="Kenwood", user=None)
        self.labThree = Section.objects.create(name="Lab 3", course=self.courseThree, days="Thursday", time="2:30",
                                               location="Physics", user=None)

        # Assign instructors to courses
        # Save labs
        self.labOne.save()
        self.labTwo.save()
        self.labThree.save()

    def login_as(self, username):
        self.client.post("/", {"username": username, "password": "password"})


    def test_assign_TA_user_to_lab_in_course(self):
        self.login_as("instructor")
        response = self.donkey.post('/edit_section_assignment.html', {"form_name": "edit_section_assignment", "section_id": self.labOne.id,
                                                                      "section_user": self.ta.id}, follow=True)
        self.labOne.refresh_from_db()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.labOne.user, self.ta)

    def test_assign_TA_user_to_lab_not_in_course(self):
        self.login_as("instructor")
        response = self.donkey.post('/edit_section_assignment.html', {"form_name": "edit_section_assignment", "section_id": self.labTwo.id,
                                                                      "section_user": self.ta.id}, follow=True)
        self.labOne.refresh_from_db()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.labTwo.user, None)

    def test_assign_instructor_user_to_lecture(self):
        self.login_as("instructor")
        response = self.donkey.post('/edit_section_assignment.html', {"form_name": "edit_section_assignment", "section_id": self.lectureOne.id,
                                                                      "section_user": self.instructor.id}, follow=True)
        self.lectureOne.refresh_from_db()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.lectureOne.user, self.instructor)

    def test_assign_instructor_user_to_lecture_not_in_course(self):
        self.login_as("instructor")
        response = self.donkey.post('/edit_section_assignment.html', {"form_name": "edit_section_assignment", "section_id": self.lectureTwo.id,
                                                                      "section_user": self.instructor.id}, follow=True)
        self.lectureTwo.refresh_from_db()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.lectureTwo.user, None)

    def test_assign_TA_to_lecture(self):
        self.login_as("instructor")
        response = self.donkey.post('/edit_section_assignment.html', {"form_name": "edit_section_assignment", "section_id": self.lectureTwo.id,
                                                                      "section_user": self.ta.id}, follow=True)
        self.lectureTwo.refresh_from_db()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.lectureTwo.user, None)

    def test_assign_instructor_to_lab(self):
        self.login_as("instructor")
        response = self.donkey.post('/edit_section_assignment.html', {"form_name": "edit_section_assignment", "section_id": self.labOne.id,
                                                                      "section_user": self.instructor.id}, follow=True)
        self.labOne.refresh_from_db()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.labOne.user, None)

    def test_change_user_success(self):
        self.login_as("instructor")
        response = self.donkey.post('/edit_section_assignment.html', {"form_name": "edit_section_assignment", "section_id": self.labOne.id,
                                                                      "section_user": self.ta.id}, follow=True)
        self.labOne.refresh_from_db()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.labOne.user, self.ta)


        response = self.donkey.post('/edit_section_assignment.html', {"form_name": "edit_section_assignment", "section_id": self.labOne.id,
                                                                      "section_user": self.ta2.id}, follow=True)
        self.labOne.refresh_from_db()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.labOne.user, self.ta2)

    def test_change_user_fail(self):
        self.login_as("instructor")
        response = self.donkey.post('/edit_section_assignment.html', {"form_name": "edit_section_assignment", "section_id": self.labOne.id,
                                                                      "section_user": self.ta.id}, follow=True)
        self.labOne.refresh_from_db()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.labOne.user, self.ta)

        response = self.donkey.post('/edit_section_assignment.html', {"form_name": "edit_section_assignment", "section_id": self.labOne.id,
                                                                      "section_user": self.instructor.id}, follow=True)
        self.labOne.refresh_from_db()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.labOne.user, self.ta)