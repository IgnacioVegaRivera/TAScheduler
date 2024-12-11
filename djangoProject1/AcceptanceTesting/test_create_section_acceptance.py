from django.test import TestCase, Client

from djangoProject1.models import User, Course, Section

class CreateLabAcceptanceTest(TestCase):
    def setUp(self):
        self.donkey = Client()

        self.valid = User(username= "valid", first_name="(no", last_name="ta)", role="TA")
        self.valid.save()

        self.instructor = User(username="instruct", role="Instructor")
        self.instructor.save()

        self.validcourse = Course(name="valid")
        self.validcourse.save()
        self.validcourse.users.add(self.instructor)
        self.invalidcourse = Course(name="invalid")
        self.invalidcourse.save()

    def test_valid_lab(self):
        response = self.donkey.post("/configure_course.html",
            {"tas": User.objects.filter(role="TA"), "ta": self.valid,
            "lab_name": "lab name", "course":self.validcourse, "form_name": "create_lab"}, follow=True)
        self.assertEqual(Section.objects.count(), 1)
        self.assertIn('message', response.context)
        self.assertEqual(response.context["message"], "The lab \"lab name\" has been created")

    def test_invalid_role(self):
        response = self.donkey.post("/configure_course.html",
            {"tas": User.objects.filter(role="TA"), "ta": self.instructor,
            "lab_name": "lab name", "course": self.validcourse, "form_name": "create_lab"}, follow=True)
        self.assertEqual(Section.objects.count(), 0)
        self.assertIn('message', response.context)
        self.assertEqual(response.context["message"], "Something went wrong when creating the lab \"lab name\"")

    def test_invalid_name(self):
        response = self.donkey.post("/configure_course.html",
            {"tas": User.objects.filter(role="TA"), "ta": self.valid,
            "lab_name": "", "course": self.validcourse, "form_name": "create_lab"}, follow=True)
        self.assertEqual(Section.objects.count(), 0)
        self.assertIn('message', response.context)
        self.assertEqual(response.context["message"], "Something went wrong when creating the lab \"\"")

    def test_invalid_course(self):
        response = self.donkey.post("/configure_course.html",
            {"tas": User.objects.filter(role="TA"), "ta": self.valid,
            "lab_name": "lab name", "course": self.invalidcourse, "form_name": "create_lab"}, follow=True)
        self.assertEqual(Section.objects.count(), 0)
        self.assertIn('message', response.context)
        self.assertEqual(response.context["message"], "Something went wrong when creating the lab \"lab name\"")

    def test_no_ta_selected(self):
        response = self.donkey.post("/configure_course.html",
            {"tas": User.objects.filter(role="TA"), "ta": "",
            "lab_name": "lab name", "course": self.validcourse, "form_name": "create_lab"}, follow=True)
        self.assertEqual(Section.objects.count(), 0)
        self.assertIn('message', response.context)
        self.assertEqual(response.context["message"], "Something went wrong when creating the lab \"lab name\"")

    def test_no_course_selected(self):
        response = self.donkey.post("/configure_course.html",
            {"tas": User.objects.filter(role="TA"), "ta": self.valid,
            "lab_name": "lab name", "course": "", "form_name": "create_lab"}, follow=True)
        self.assertEqual(Section.objects.count(), 0)
        self.assertIn('message', response.context)
        self.assertEqual(response.context["message"], "Something went wrong when creating the lab \"lab name\"")

    def test_invalid_form(self):
        response = self.donkey.post("/configure_course.html",
            {"tas": User.objects.filter(role="TA"), "ta": self.valid,
            "lab_name": "lab name", "course": self.validcourse, "form_name": "fake_form"}, follow=True)
        self.assertEqual(Section.objects.count(), 0)
        self.assertIn('message', response.context)
        self.assertEqual(response.context["message"], "Something went wrong when fetching the form, please try again.")