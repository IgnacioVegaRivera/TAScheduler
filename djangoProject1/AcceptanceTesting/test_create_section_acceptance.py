from django.test import TestCase, Client
from datetime import time
from djangoProject1.models import User, Course, Section

class CreateLabAcceptanceTest(TestCase):
    def setUp(self):
        self.llama = Client()
        self.ta = User(first_name="(no", last_name="ta)", role="TA")
        self.ta.save()
        self.course = Course()
        self.course.save()
        self.instructor = User(username="instruct", role="Instructor")
        self.instructor.save()
        self.course.users.add(self.instructor)
        self.course.users.add(self.ta)
        self.time = time(9, 30)

    def test_valid_section(self):
        response = self.llama.post("/configure_course.html", {"section_name":"Lab 001", "section_course": self.course,
                                                               "section_days" : ["Monday", "Wednesday"], "section_time": self.time,
                                                               "section_location":"KIRC 1130", "section_user": self.ta.id,
                                                               "form_name": "create_section"})
        self.assertEqual(Section.objects.count(), 1)
        self.assertIn('message', response.context)
        self.assertEqual(response.context["message"], "The section \"Lab 001\" has been created")

    def test_invalid_section_name(self):
        response = self.llama.post("/configure_course.html", {"section_name": "name", "section_course": self.course,
                                                              "section_days": ["Monday", "Wednesday"],
                                                              "section_time": self.time,
                                                              "section_location": "KIRC 1130",
                                                              "section_user": self.ta.id,
                                                              "form_name": "create_section"})
        self.assertEqual(Section.objects.count(), 0)
        self.assertIn('message', response.context)
        self.assertEqual(response.context["message"], "Something went wrong when creating the section \"name\"")

    def test_no_section_course(self):
        response = self.llama.post("/configure_course.html", {"section_name": "Lab 001", "section_course": "",
                                                              "section_days": ["Monday", "Wednesday"],
                                                              "section_time": self.time,
                                                              "section_location": "KIRC 1130",
                                                              "section_user": self.ta.id,
                                                              "form_name": "create_section"})
        self.assertEqual(Section.objects.count(), 0)
        self.assertIn('message', response.context)
        self.assertEqual(response.context["message"], "Something went wrong when creating the section \"Lab 001\"")

    def test_no_days(self):
        response = self.llama.post("/configure_course.html", {"section_name": "Lab 001", "section_course": self.course,
                                                              "section_days": [],
                                                              "section_time": self.time,
                                                              "section_location": "KIRC 1130",
                                                              "section_user": self.ta.id,
                                                              "form_name": "create_section"})
        self.assertEqual(Section.objects.count(), 1)
        self.assertIn('message', response.context)
        self.assertEqual(response.context["message"], "The section \"Lab 001\" has been created")

    def test_no_time(self):
        response = self.llama.post("/configure_course.html", {"section_name": "Lab 001", "section_course": self.course,
                                                              "section_days": ["Monday", "Wednesday"],
                                                              "section_time": "",
                                                              "section_location": "KIRC 1130",
                                                              "section_user": self.ta.id,
                                                              "form_name": "create_section"})
        self.assertEqual(Section.objects.count(), 1)
        self.assertIn('message', response.context)
        self.assertEqual(response.context["message"], "The section \"Lab 001\" has been created")

    def test_no_location(self):
        response = self.llama.post("/configure_course.html", {"section_name": "Lab 001", "section_course": self.course,
                                                              "section_days": ["Monday", "Wednesday"],
                                                              "section_time": self.time,
                                                              "section_location": "",
                                                              "section_user": self.ta.id,
                                                              "form_name": "create_section"})
        self.assertEqual(Section.objects.count(), 1)
        self.assertIn('message', response.context)
        self.assertEqual(response.context["message"], "The section \"Lab 001\" has been created")

    def test_no_user(self):
        response = self.llama.post("/configure_course.html", {"section_name": "Lab 001", "section_course": self.course,
                                                              "section_days": ["Monday", "Wednesday"],
                                                              "section_time": self.time,
                                                              "section_location": "KIRC 1130",
                                                              "section_user": "",
                                                              "form_name": "create_section"})
        self.assertEqual(Section.objects.count(), 1)
        self.assertIn('message', response.context)
        self.assertEqual(response.context["message"], "The section \"Lab 001\" has been created")

    def test_invalid_user_role(self):
        response = self.llama.post("/configure_course.html", {"section_name": "Lab 001", "section_course": self.course,
                                                              "section_days": ["Monday", "Wednesday"],
                                                              "section_time": self.time,
                                                              "section_location": "KIRC 1130",
                                                              "section_user": self.instructor.id,
                                                              "form_name": "create_section"})
        self.assertEqual(Section.objects.count(), 0)
        self.assertIn('message', response.context)
        self.assertEqual(response.context["message"], "Something went wrong when creating the section \"Lab 001\"")

    def test_invalid_form_name(self):
        response = self.llama.post("/configure_course.html", {"section_name": "Lab 001", "section_course": self.course,
                                                              "section_days": ["Monday", "Wednesday"],
                                                              "section_time": self.time,
                                                              "section_location": "KIRC 1130",
                                                              "section_user": self.ta.id,
                                                              "form_name": "invalid_form"})
        self.assertEqual(Section.objects.count(), 0)
        self.assertIn('message', response.context)
        self.assertEqual(response.context["message"], "Something went wrong when fetching the form, please try again.")

    # def test_valid_lab(self):
    #     response = self.donkey.post("/configure_course.html",
    #         {"tas": User.objects.filter(role="TA"), "ta": self.valid,
    #         "lab_name": "lab name", "course":self.validcourse, "form_name": "create_lab"}, follow=True)
    #     self.assertEqual(Section.objects.count(), 1)
    #     self.assertIn('message', response.context)
    #     self.assertEqual(response.context["message"], "The lab \"lab name\" has been created")
    #
    # def test_invalid_role(self):
    #     response = self.donkey.post("/configure_course.html",
    #         {"tas": User.objects.filter(role="TA"), "ta": self.instructor,
    #         "lab_name": "lab name", "course": self.validcourse, "form_name": "create_lab"}, follow=True)
    #     self.assertEqual(Section.objects.count(), 0)
    #     self.assertIn('message', response.context)
    #     self.assertEqual(response.context["message"], "Something went wrong when creating the lab \"lab name\"")
    #
    # def test_invalid_name(self):
    #     response = self.donkey.post("/configure_course.html",
    #         {"tas": User.objects.filter(role="TA"), "ta": self.valid,
    #         "lab_name": "", "course": self.validcourse, "form_name": "create_lab"}, follow=True)
    #     self.assertEqual(Section.objects.count(), 0)
    #     self.assertIn('message', response.context)
    #     self.assertEqual(response.context["message"], "Something went wrong when creating the lab \"\"")
    #
    # def test_invalid_course(self):
    #     response = self.donkey.post("/configure_course.html",
    #         {"tas": User.objects.filter(role="TA"), "ta": self.valid,
    #         "lab_name": "lab name", "course": self.invalidcourse, "form_name": "create_lab"}, follow=True)
    #     self.assertEqual(Section.objects.count(), 0)
    #     self.assertIn('message', response.context)
    #     self.assertEqual(response.context["message"], "Something went wrong when creating the lab \"lab name\"")
    #
    # def test_no_ta_selected(self):
    #     response = self.donkey.post("/configure_course.html",
    #         {"tas": User.objects.filter(role="TA"), "ta": "",
    #         "lab_name": "lab name", "course": self.validcourse, "form_name": "create_lab"}, follow=True)
    #     self.assertEqual(Section.objects.count(), 0)
    #     self.assertIn('message', response.context)
    #     self.assertEqual(response.context["message"], "Something went wrong when creating the lab \"lab name\"")
    #
    # def test_no_course_selected(self):
    #     response = self.donkey.post("/configure_course.html",
    #         {"tas": User.objects.filter(role="TA"), "ta": self.valid,
    #         "lab_name": "lab name", "course": "", "form_name": "create_lab"}, follow=True)
    #     self.assertEqual(Section.objects.count(), 0)
    #     self.assertIn('message', response.context)
    #     self.assertEqual(response.context["message"], "Something went wrong when creating the lab \"lab name\"")
    #
    # def test_invalid_form(self):
    #     response = self.donkey.post("/configure_course.html",
    #         {"tas": User.objects.filter(role="TA"), "ta": self.valid,
    #         "lab_name": "lab name", "course": self.validcourse, "form_name": "fake_form"}, follow=True)
    #     self.assertEqual(Section.objects.count(), 0)
    #     self.assertIn('message', response.context)
    #     self.assertEqual(response.context["message"], "Something went wrong when fetching the form, please try again.")