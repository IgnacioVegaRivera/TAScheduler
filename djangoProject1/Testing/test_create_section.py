from django.test import TestCase, Client
from djangoProject1.MethodFiles.Administrator import CreateSection
from djangoProject1.models import User, Course, Section
from datetime import time

class CreateSectionUnitTest(TestCase):
    def setUp(self):
        self.ta = User(first_name="(no", last_name="ta)", role="TA")
        self.ta.save()
        self.course = Course()
        self.course.save()
        self.instructor = User(username="instruct", role="Instructor")
        self.instructor.save()
        self.course.users.add(self.instructor)
        self.course.users.add(self.ta)
        self.time = time(9, 30)

    #every section is either a Lecture, Lab, or Discussion
    def test_create_lecture_section(self):
        section = CreateSection.create_section("Lecture 001", self.course, self.instructor, "Monday",
                                               self.time, "Chem 110")
        self.assertEqual(section.name, "Lecture 001")
        self.assertEqual(section.course, self.course)
        self.assertEqual(section.user, self.instructor)
        self.assertEqual(section.day, "Monday")
        self.assertEqual(section.time.hour, 9)
        self.assertEqual(section.time.minute, 30)
        self.assertEqual(section.location, "Chem 110")

    def test_create_lab_section(self):
        section = CreateSection.create_section("Lab 001", self.course, self.ta, "Thursday",
                                               self.time, "KIRC 1130")
        self.assertEqual(section.name, "Lab 001")
        self.assertEqual(section.course, self.course)
        self.assertEqual(section.user, self.ta)
        self.assertEqual(section.day, "Thursday")
        self.assertEqual(section.time.hour, 9)
        self.assertEqual(section.time.minute, 30)
        self.assertEqual(section.location, "KIRC 1130")

    def test_create_discussion_section(self):
        section = CreateSection.create_section("Discussion 001", self.course, self.ta, "Tuesday",
                                               self.time, "EMS 119")
        self.assertEqual(section.name, "Discussion 001")
        self.assertEqual(section.course, self.course)
        self.assertEqual(section.user, self.ta)
        self.assertEqual(section.day, "Tuesday")
        self.assertEqual(section.time.hour, 9)
        self.assertEqual(section.time.minute, 30)
        self.assertEqual(section.location, "EMS 119")

    #name tests
    def test_no_name(self):
        section = CreateSection.create_section("", self.course, self.instructor, "Monday",
                                               self.time, "Chem 110")
        self.assertEqual(section, None)

    # section should contain "Lab", "Lecture", or "Discussion" in its name
    def test_no_section_type_in_name(self):
        section = CreateSection.create_section("name", self.course, self.instructor, "Monday",
                                               self.time, "Chem 110")
        self.assertEqual(section, None)

    def test_multiple_section_type_in_name(self):
        section = CreateSection.create_section("Lab Lecture Discussion", self.course, self.instructor,
                                               "Monday", self.time, "Chem 110")
        self.assertEqual(section, None)

    def test_wrong_type_name(self):
        section = CreateSection.create_section(123, self.course, self.instructor, "Monday",
                                               self.time, "Chem 110")
        self.assertEqual(section, None)


    #course tests
    def test_no_course(self):
        section = CreateSection.create_section("Lab 001", None, self.ta, "Thursday",
                                               self.time, "KIRC 1130")
        self.assertEqual(section, None)

    def test_wrong_type_course(self):
        section = CreateSection.create_section("Lecture 001", "Comp Sci 361", self.instructor, "Monday",
                                           self.time, "Chem 110")
        self.assertEqual(section, None)


    #user tests
    def test_no_user(self):
        section = CreateSection.create_section("Lab 001", self.course, None, "Thursday",
                                           self.time, "KIRC 1130")
        self.assertEqual(section, None)

    def test_wrong_type_user(self):
        section = CreateSection.create_section("Lab 001", self.course, "TA Joe", "Thursday",
                                               self.time, "KIRC 1130")
        self.assertEqual(section, None)

    def test_ta_assigned_to_lecture(self):
        section = CreateSection.create_section("Lecture 001", self.course, self.ta,
                                               "Monday", self.time, "Chem 110")
        self.assertEqual(section, None)

    def test_instructor_assigned_to_lab(self):
        section = CreateSection.create_section("Lab 001", self.course, self.instructor,
                                               "Thursday", self.time, "KIRC 1130")
        self.assertEqual(section, None)

    def test_instructor_assigned_to_discussion(self):
        section = CreateSection.create_section("Discussion 001", self.course, self.instructor,
                                               "Tuesday", self.time, "EMS 119")
        self.assertEqual(section, None)

    #day tests
    def test_blank_day(self):
        section = CreateSection.create_section("Discussion 001", self.course, self.ta,
                                               "", self.time, "EMS 119")
        self.assertEqual(section, None)

    def test_no_day(self):
        section = CreateSection.create_section("Discussion 001", self.course, self.ta,
                                               None, self.time, "EMS 119")
        self.assertEqual(section, None)

    #days should be case-sensitive
    def test_invalid_day(self):
        section = CreateSection.create_section("Discussion 001", self.course, self.ta,
                                               "tuesday", self.time, "Chem 110")
        self.assertEqual(section, None)


    #time tests
    def test_no_time(self):
        section = CreateSection.create_section("Discussion 001", self.course, self.ta,
                                               "Tuesday", None, "EMS 119")
        self.assertEqual(section, None)

    def test_wrong_type_time(self):
        section = CreateSection.create_section("Discussion 001", self.course, self.ta,
                                               "Tuesday", "9:30", "EMS 119")
        self.assertEqual(section, None)

    #location tests
    def test_no_building_name(self):
        section = CreateSection.create_section("Discussion 001", self.course, self.ta,
                                               "Tuesday", self.time, "119")
        self.assertEqual(section, None)

    def test_no_room_number(self):
        section = CreateSection.create_section("Discussion 001", self.course, self.ta,
                                               "Tuesday", self.time, "EMS")
        self.assertEqual(section, None)

    def test_blank_location(self):
        section = CreateSection.create_section("Discussion 001", self.course, self.ta,
                                               "Tuesday", self.time, "")
        self.assertEqual(section, None)

    def test_wrong_type_location(self):
        section = CreateSection.create_section("Discussion 001", self.course, self.ta,
                                               "Tuesday", self.time, 123)
        self.assertEqual(section, None)

    #duplicate test
    def test_lab_already_exists(self):
        #create a section
        section = CreateSection.create_section("Lab 001", self.course, self.ta, "Thursday",
                                               self.time, "KIRC 1130")

        #try to create a section with the same parameters
        section2 = CreateSection.create_section("Lab 001", self.course, self.ta, "Thursday",
                                               self.time, "KIRC 1130")
        self.assertEqual(section2, None)


#need to work on
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
        response = self.donkey.post("/configure_course.html",
            {"tas": User.objects.filter(role="TA"), "ta": self.valid,
            "lab_name": "lab name", "course":self.validcourse, "form_name": "create_lab"}, follow=True)
        self.assertEqual(Lab.objects.count(), 1)
        self.assertIn('message', response.context)
        self.assertEqual(response.context["message"], "The lab \"lab name\" has been created")

    def test_invalid_role(self):
        response = self.donkey.post("/configure_course.html",
            {"tas": User.objects.filter(role="TA"), "ta": self.instructor,
            "lab_name": "lab name", "course": self.validcourse, "form_name": "create_lab"}, follow=True)
        self.assertEqual(Lab.objects.count(), 0)
        self.assertIn('message', response.context)
        self.assertEqual(response.context["message"], "Something went wrong when creating the lab \"lab name\"")

    def test_invalid_name(self):
        response = self.donkey.post("/configure_course.html",
            {"tas": User.objects.filter(role="TA"), "ta": self.valid,
            "lab_name": "", "course": self.validcourse, "form_name": "create_lab"}, follow=True)
        self.assertEqual(Lab.objects.count(), 0)
        self.assertIn('message', response.context)
        self.assertEqual(response.context["message"], "Something went wrong when creating the lab \"\"")

    def test_invalid_course(self):
        response = self.donkey.post("/configure_course.html",
            {"tas": User.objects.filter(role="TA"), "ta": self.valid,
            "lab_name": "lab name", "course": self.invalidcourse, "form_name": "create_lab"}, follow=True)
        self.assertEqual(Lab.objects.count(), 0)
        self.assertIn('message', response.context)
        self.assertEqual(response.context["message"], "Something went wrong when creating the lab \"lab name\"")

    def test_no_ta_selected(self):
        response = self.donkey.post("/configure_course.html",
            {"tas": User.objects.filter(role="TA"), "ta": "",
            "lab_name": "lab name", "course": self.validcourse, "form_name": "create_lab"}, follow=True)
        self.assertEqual(Lab.objects.count(), 0)
        self.assertIn('message', response.context)
        self.assertEqual(response.context["message"], "Something went wrong when creating the lab \"lab name\"")

    def test_no_course_selected(self):
        response = self.donkey.post("/configure_course.html",
            {"tas": User.objects.filter(role="TA"), "ta": self.valid,
            "lab_name": "lab name", "course": "", "form_name": "create_lab"}, follow=True)
        self.assertEqual(Lab.objects.count(), 0)
        self.assertIn('message', response.context)
        self.assertEqual(response.context["message"], "Something went wrong when creating the lab \"lab name\"")

    def test_invalid_form(self):
        response = self.donkey.post("/configure_course.html",
            {"tas": User.objects.filter(role="TA"), "ta": self.valid,
            "lab_name": "lab name", "course": self.validcourse, "form_name": "fake_form"}, follow=True)
        self.assertEqual(Lab.objects.count(), 0)
        self.assertIn('message', response.context)
        self.assertEqual(response.context["message"], "Something went wrong when fetching the form, please try again.")