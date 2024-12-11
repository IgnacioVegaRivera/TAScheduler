from django.test import TestCase, Client

from djangoProject1.models import User, Course, Section

class TestConfigureCourseUnit(TestCase):
    def setUp(self):
        #create instructors
        self.inst = User.objects.create(username="inst", role="Instructor", first_name="Inst", last_name="User", skills="Good at teaching at concepts")
        self.ructor = User.objects.create(username="ructor", role="Instructor", first_name="Ructor", last_name="User", skills="Good at teaching coding")
        self.ructor.save()
        self.inst.save()

        #create tas
        self.t = User.objects.create(username="t", role="TA", first_name="T", last_name="User", skills="proficient in java")
        self.a = User.objects.create(username="a", role="TA", first_name="A", last_name="User", skills="proficient in python ")
        self.t.save()
        self.a.save()

        # Create courses and labs
        self.course1 = Course.objects.create(name="Course 1")
        self.course2 = Course.objects.create(name="Course 2")
        self.course3 = Course.objects.create(name="Course 3")
        self.course1.save()
        self.course2.save()
        self.course3.save()

        # Assign instructors to courses
        self.course1.users.add(self.ructor)
        self.course1.users.add(self.inst)
        self.course2.users.add(self.ructor)
        self.course3.users.add(self.inst)
        # self.course1.instructors.add(self.ructor)
        # self.course1.instructors.add(self.inst)
        # self.course2.instructors.add(self.ructor)
        # self.course3.instructors.add(self.inst)


        # Create labs and assign TAs
        self.lab1 = Section.objects.create(name="Lab 1", course=self.course1, user=self.t)
        self.lab2 = Section.objects.create(name="Lab 2", course=self.course2, user=self.a)
        self.lab3 = Section.objects.create(name="Lab 3", course=self.course2, user=self.a)
        self.lab1.save()
        self.lab2.save()
        self.lab3.save()
        # self.lab1 = Section.objects.create(name="Lab 1", course=self.course1, ta=self.t)
        # self.lab2 = Section.objects.create(name="Lab 2", course=self.course2, ta=self.a)
        # self.lab3 = Section.objects.create(name="Lab 3", course=self.course2, ta=self.a)
        # self.lab1.save()
        # self.lab2.save()
        # self.lab3.save()


    def test_course_list(self):
        courses = Course.objects.all()
        self.assertEqual(courses.count(), 3)
        self.assertIn(self.course1, courses)
        self.assertIn(self.course2, courses)
        self.assertIn(self.course3, courses)

    def test_lab_list(self):
        labs = Section.objects.all()
        self.assertEqual(labs.count(), 3)
        self.assertIn(self.lab1, labs)
        self.assertIn(self.lab2, labs)
        self.assertIn(self.lab3, labs)

    def test_instructor_list(self):
        instructors = User.objects.filter(role="Instructor")
        self.assertEqual(instructors.count(), 2)
        self.assertIn(self.inst, instructors)
        self.assertIn(self.ructor, instructors)

    def test_ta_list(self):
        tas = User.objects.filter(role="TA")
        self.assertEqual(tas.count(), 2)
        self.assertIn(self.t, tas)
        self.assertIn(self.a, tas)

    def test_inst_courses(self):
        courses = Course.objects.filter(users=self.inst)
        self.assertEqual(courses.count(), 2)
        self.assertIn(self.course1, courses)
        self.assertIn(self.course3, courses)

    def test_ructor_courses(self):
        courses = Course.objects.filter(users=self.ructor)
        self.assertEqual(courses.count(), 2)
        self.assertIn(self.course1, courses)
        self.assertIn(self.course2, courses)

    def test_inst_ructor_courses(self):
        courses = Course.objects.filter(users=self.inst).filter(users=self.ructor)
        self.assertEqual(courses.count(), 1)
        self.assertIn(self.course1, courses)
        self.assertEqual(self.course1.users.count(), 2)

    def test_t_labs(self):
        labs = Section.objects.filter(user=self.t)
        self.assertEqual(labs.count(), 1)
        self.assertIn(self.lab1, labs)

    def test_a_labs(self):
        labs = Section.objects.filter(user=self.a)
        self.assertEqual(labs.count(), 2)
        self.assertIn(self.lab2, labs)
        self.assertIn(self.lab3, labs)

    def test_one_lab(self):
        labs = Section.objects.filter(course=self.course1)
        self.assertEqual(labs.count(), 1)
        self.assertIn(self.lab1, labs)

    def test_two_labs(self):
        labs = Section.objects.filter(course=self.course2)
        self.assertEqual(labs.count(), 2)
        self.assertIn(self.lab2, labs)
        self.assertIn(self.lab3, labs)

    def test_no_labs(self):
        labs = Section.objects.filter(course=self.course3)
        self.assertEqual(labs.count(), 0)


# class TestConfigureCourseAcceptance(TestCase):
#     def setUp(self):
#         self.donkey = Client()
#
#     #course with 2 instructors
#     def course1(self):
#         self.inst = User.objects.create(username="inst", role="Instructor", first_name="Inst", last_name="User")
#         self.ructor = User.objects.create(username="ructor", role="Instructor", first_name="Ructor", last_name="User")
#         self.ructor.save()
#         self.inst.save()
#
#         self.t = User.objects.create(username="t", role="TA", first_name="T", last_name="User")
#         self.t.save()
#
#         self.course1 = Course.objects.create(name="Course 1")
#         self.course1.save()
#
#         self.course1.instructors.add(self.ructor)
#         self.course1.instructors.add(self.inst)
#
#         self.lab1 = Lab.objects.create(name="Lab 1", course=self.course1, ta=self.t)
#         self.lab1.save()
#
#     #course with 1 instructor and 1 lab
#     def course2(self):
#         self.course2 = Course.objects.create(name="Course 2")
#         self.course2.save()
#
#         self.ructor = User.objects.create(username="ructor", role="Instructor", first_name="Ructor", last_name="User")
#         self.ructor.save()
#
#         self.a = User.objects.create(username="a", role="TA", first_name="A", last_name="User")
#         self.a.save()
#
#         self.course2.instructors.add(self.ructor)
#
#         self.lab2 = Lab.objects.create(name="Lab 2", course=self.course2, ta=self.a)
#         self.lab2.save()
#
#     #course with 2 labs
#     def course3(self):
#         self.course3 = Course.objects.create(name="Course 3")
#         self.course3.save()
#
#         self.inst = User.objects.create(username="inst", role="Instructor", first_name="Inst", last_name="User")
#         self.inst.save()
#
#         self.t = User.objects.create(username="t", role="TA", first_name="T", last_name="User")
#         self.t.save()
#         self.a = User.objects.create(username="a", role="TA", first_name="A", last_name="User")
#         self.a.save()
#
#         self.course3.instructors.add(self.inst)
#
#         self.lab3 = Lab.objects.create(name="Lab 3", course=self.course3, ta=self.a)
#         self.lab4 = Lab.objects.create(name="Lab 4", course=self.course3, ta=self.t)
#         self.lab3.save()
#         self.lab4.save()
#
#     #course with no labs
#     def course4(self):
#         self.course4 = Course.objects.create(name="Course 4")
#         self.course4.save()
#
#         self.ructor = User.objects.create(username="ructor", role="Instructor", first_name="Ructor", last_name="User")
#         self.ructor.save()
#         self.course4.instructors.add(self.ructor)
#
#     def test_course1_shows(self):
#         self.course1()
#         response = self.donkey.get("/configure_course.html")
#         self.assertContains(response, "Course 1")
#         self.assertContains(response, "Ructor User (Instructor)")
#         self.assertContains(response, "Inst User (Instructor)")
#         self.assertContains(response, "Lab 1")
#         self.assertContains(response, "T User (Teaching Assistant)")
#         self.assertContains(response, "Edit") #each course should have an edit button on this page
#
#     def test_course2_shows(self):
#         self.course2()
#         response = self.donkey.get("/configure_course.html")
#         self.assertContains(response, "Course 2")
#         self.assertContains(response, "Ructor User (Instructor)")
#         self.assertContains(response, "Lab 2")
#         self.assertContains(response, "A User (Teaching Assistant)")
#         self.assertContains(response, "Edit")
#
#     def test_course3_shows(self):
#         self.course3()
#         response = self.donkey.get("/configure_course.html")
#         self.assertContains(response, "Course 3")
#         self.assertContains(response, "Inst User (Instructor)")
#         self.assertContains(response, "Lab 3")
#         self.assertContains(response, "A User (Teaching Assistant)")
#         self.assertContains(response, "Lab 4")
#         self.assertContains(response, "T User (Teaching Assistant)")
#         self.assertContains(response, "Edit")
#
#     def test_course4_shows(self):
#         self.course4()
#         response = self.donkey.get("/configure_course.html")
#         self.assertContains(response, "Course 4")
#         self.assertContains(response, "Ructor User (Instructor)")
#         self.assertNotContains(response, "(Teaching Assistant)") #no lab so no teaching assistant shows up
#         self.assertContains(response, "Edit")