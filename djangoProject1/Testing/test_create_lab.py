from django.test import TestCase, Client
from djangoProject1.MethodFiles.Administrator import CreateLab
from djangoProject1.models import User, Course, Lab

class CreateLabUnitTest(TestCase):
    def setUp(self):
        self.user = User(first_name="(no", last_name="ta)", role="TA")
        self.user.save()
        self.course = Course()
        self.course.save()
        self.instructor = User(username="instruct", role="Instructor")
        self.instructor.save()
        self.course.instructors.add(self.instructor)


    def test_create_lab(self):
        lab = CreateLab.create_lab("name", self.course, self.user)
        self.assertEqual(lab.name, "name")
        self.assertEqual(lab.course, self.course)
        self.assertEqual(lab.ta, self.user)

    def test_no_name(self):
        lab = CreateLab.create_lab("", self.course, self.user)
        self.assertEqual(lab, None)

    def test_no_course(self):
        lab = CreateLab.create_lab("name", None, self.user)
        self.assertEqual(lab, None)

    def test_no_ta(self):
        lab = CreateLab.create_lab("name", self.course, None)
        self.assertEqual(lab, None)

    def test_not_a_ta(self):
        lab = CreateLab.create_lab("name", self.course, self.instructor)
        self.assertEqual(lab, None)

    def test_invalid_name_type(self):
        lab = CreateLab.create_lab(123, self.course,self.user)
        self.assertEqual(lab, None)

    def test_invalid_course_type(self):
        lab = CreateLab.create_lab("name", "course", self.user)
        self.assertEqual(lab, None)

    def test_invalid_user_type(self):
        lab = CreateLab.create_lab("name", self.course, "ta")
        self.assertEqual(lab, None)

    def test_lab_already_exists(self):
        lab = CreateLab.create_lab("name", self.course, self.user)
        self.assertEqual(lab.name, "name")
        self.assertEqual(lab.course, self.course)
        self.assertEqual(lab.ta, self.user)

        lab2 = CreateLab.create_lab("name", self.course, self.user)
        self.assertEqual(lab2, None)

class CreateLabAcceptanceTest(TestCase):
    def setUp(self):
        self.donkey = Client()

        self.valid = User(username= "valid", first_name="(no", last_name="ta)", role="TA")
        self.valid.save()

        self.instructor = User(username="instruct", role="Instructor")
        self.instructor.save()

        self.validcourse = Course(name="valid")
        self.validcourse.save()
        self.validcourse.instructors.add(self.instructor)
        self.invalidcourse = Course(name="invalid")
        self.invalidcourse.save()

    def test_valid_lab(self):
        response = self.donkey.post("/configureCourse.html",
            {"tas": User.objects.filter(role="TA"), "ta": self.valid,
            "lab_name": "lab name", "course":self.validcourse, "form_name": "create_lab"}, follow=True)
        self.assertEqual(Lab.objects.count(), 1)
        self.assertIn('message', response.context)
        self.assertEqual(response.context["message"], "The lab \"lab name\" has been created")

    def test_invalid_role(self):
        response = self.donkey.post("/configureCourse.html",
            {"tas": User.objects.filter(role="TA"), "ta": self.instructor,
            "lab_name": "lab name", "course": self.validcourse, "form_name": "create_lab"}, follow=True)
        self.assertEqual(Lab.objects.count(), 0)
        self.assertIn('message', response.context)
        self.assertEqual(response.context["message"], "Something went wrong when creating the lab \"lab name\"")

    def test_invalid_name(self):
        response = self.donkey.post("/configureCourse.html",
            {"tas": User.objects.filter(role="TA"), "ta": self.valid,
            "lab_name": "", "course": self.validcourse, "form_name": "create_lab"}, follow=True)
        self.assertEqual(Lab.objects.count(), 0)
        self.assertIn('message', response.context)
        self.assertEqual(response.context["message"], "Something went wrong when creating the lab \"\"")

    def test_invalid_course(self):
        response = self.donkey.post("/configureCourse.html",
            {"tas": User.objects.filter(role="TA"), "ta": self.valid,
            "lab_name": "lab name", "course": self.invalidcourse, "form_name": "create_lab"}, follow=True)
        self.assertEqual(Lab.objects.count(), 0)
        self.assertIn('message', response.context)
        self.assertEqual(response.context["message"], "Something went wrong when creating the lab \"lab name\"")

    def test_no_ta_selected(self):
        response = self.donkey.post("/configureCourse.html",
            {"tas": User.objects.filter(role="TA"), "ta": "",
            "lab_name": "lab name", "course": self.validcourse, "form_name": "create_lab"}, follow=True)
        self.assertEqual(Lab.objects.count(), 0)
        self.assertIn('message', response.context)
        self.assertEqual(response.context["message"], "Something went wrong when creating the lab \"lab name\"")

    def test_no_course_selected(self):
        response = self.donkey.post("/configureCourse.html",
            {"tas": User.objects.filter(role="TA"), "ta": self.valid,
            "lab_name": "lab name", "course": "", "form_name": "create_lab"}, follow=True)
        self.assertEqual(Lab.objects.count(), 0)
        self.assertIn('message', response.context)
        self.assertEqual(response.context["message"], "Something went wrong when creating the lab \"lab name\"")

    def test_invalid_form(self):
        response = self.donkey.post("/configureCourse.html",
            {"tas": User.objects.filter(role="TA"), "ta": self.valid,
            "lab_name": "lab name", "course": self.validcourse, "form_name": "fake_form"}, follow=True)
        self.assertEqual(Lab.objects.count(), 0)
        self.assertIn('message', response.context)
        self.assertEqual(response.context["message"], "Something went wrong when fetching the form, please try again.")