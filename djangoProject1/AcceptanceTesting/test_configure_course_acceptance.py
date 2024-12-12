from django.test import TestCase, Client

from djangoProject1.models import User, Course, Section

class TestConfigureCourseAcceptance(TestCase):
    def setUp(self):
        self.donkey = Client()

    #course with 2 instructors
    def course1(self):
        self.inst = User.objects.create(username="inst", role="Instructor", first_name="Inst", last_name="User")
        self.ructor = User.objects.create(username="ructor", role="Instructor", first_name="Ructor", last_name="User")
        self.ructor.save()
        self.inst.save()

        self.t = User.objects.create(username="t", role="TA", first_name="T", last_name="User")
        self.t.save()

        self.course1 = Course.objects.create(name="Course 1")
        self.course1.save()

        self.course1.users.add(self.ructor)
        self.course1.users.add(self.inst)

        self.lab1 = Section.objects.create(name="Lab 1", course=self.course1, user=self.t)
        self.lab1.save()

    #course with 1 instructor and 1 lab
    def course2(self):
        self.course2 = Course.objects.create(name="Course 2")
        self.course2.save()

        self.ructor = User.objects.create(username="ructor", role="Instructor", first_name="Ructor", last_name="User")
        self.ructor.save()

        self.a = User.objects.create(username="a", role="TA", first_name="A", last_name="User")
        self.a.save()

        self.course2.users.add(self.ructor)

        self.lab2 = Section.objects.create(name="Lab 2", course=self.course2, user=self.a)
        self.lab2.save()

    #course with 2 labs
    def course3(self):
        self.course3 = Course.objects.create(name="Course 3")
        self.course3.save()

        self.inst = User.objects.create(username="inst", role="Instructor", first_name="Inst", last_name="User")
        self.inst.save()

        self.t = User.objects.create(username="t", role="TA", first_name="T", last_name="User")
        self.t.save()
        self.a = User.objects.create(username="a", role="TA", first_name="A", last_name="User")
        self.a.save()

        self.course3.users.add(self.inst)

        self.lab3 = Section.objects.create(name="Lab 3", course=self.course3, user=self.a)
        self.lab4 = Section.objects.create(name="Lab 4", course=self.course3, user=self.t)
        self.lab3.save()
        self.lab4.save()

    #course with no labs
    def course4(self):
        self.course4 = Course.objects.create(name="Course 4")
        self.course4.save()

        self.ructor = User.objects.create(username="ructor", role="Instructor", first_name="Ructor", last_name="User")
        self.ructor.save()
        self.course4.users.add(self.ructor)

    def test_course1_shows(self):
        self.course1()
        response = self.donkey.get("/configure_course.html")
        self.assertContains(response, "Course 1")
        self.assertContains(response, "Ructor User (Instructor)")
        self.assertContains(response, "Inst User (Instructor)")
        self.assertContains(response, "Lab 1")
        self.assertContains(response, "T User (Teaching Assistant)")
        self.assertContains(response, "Edit") #each course should have an edit button on this page

    def test_course2_shows(self):
        self.course2()
        response = self.donkey.get("/configure_course.html")
        self.assertContains(response, "Course 2")
        self.assertContains(response, "Ructor User (Instructor)")
        self.assertContains(response, "Lab 2")
        self.assertContains(response, "A User (Teaching Assistant)")
        self.assertContains(response, "Edit")

    def test_course3_shows(self):
        self.course3()
        response = self.donkey.get("/configure_course.html")
        self.assertContains(response, "Course 3")
        self.assertContains(response, "Inst User (Instructor)")
        self.assertContains(response, "Lab 3")
        self.assertContains(response, "A User (Teaching Assistant)")
        self.assertContains(response, "Lab 4")
        self.assertContains(response, "T User (Teaching Assistant)")
        self.assertContains(response, "Edit")

    def test_course4_shows(self):
        self.course4()
        response = self.donkey.get("/configure_course.html")
        self.assertContains(response, "Course 4")
        self.assertContains(response, "Ructor User (Instructor)")
        self.assertNotContains(response, "(Teaching Assistant)") #no lab so no teaching assistant shows up
        self.assertContains(response, "Edit")