from django.test import TestCase, Client
from djangoProject1.models import User, Course, Lab


class IntegrationTests(TestCase):
    def setUp(self):
        self.donkey = Client()

    def test_create_and_view_user(self):
        #create the user
        response = self.donkey.post("/configureUser.html", {"first_name": "Administrator",
                                    "last_name": "Smith", "username": "login1",
                                    "password": "password1",
                                    "email": "EMAIL1@email.com", "phone_number": "1141234567",
                                    "address": "UWM1",
                                    "role": "TA", "form_name": "create_user"}, follow=True)
        self.assertEqual(User.objects.count(), 1, "The amount of users do not match")
        self.assertIn('message', response.context)
        self.assertEqual(response.context['message'], "The user \"Administrator Smith\" has been created")

        #check that it shows up properly
        self.assertContains(response, "Administrator Smith")
        self.assertContains(response, "TA")
        self.assertContains(response, "No Labs.")
        self.assertContains(response, "EMAIL1@email.com")
        self.assertContains(response, "1141234567")


    def test_create_and_view_edited_user(self):
        #create the user
        response = self.donkey.post("/configureUser.html", {"first_name": "Administrator",
                                    "last_name": "Smith", "username": "login1","password": "password1",
                                    "email": "EMAIL1@email.com", "phone_number": "1141234567", "address": "UWM1",
                                    "role": "TA", "form_name": "create_user"}, follow=True)
        self.assertEqual(User.objects.count(), 1, "The amount of users do not match")
        self.assertIn('message', response.context)
        self.assertEqual(response.context['message'],"The user \"Administrator Smith\" has been created")

        #edit that user we created and check that it was edited properly
        user = User.objects.get(username='login1')
        response = self.client.post('/configureUser.html', {'id': user.id, 'first_name': 'Jane',
                                    "form_name": "edit_user", 'last_name': 'Doe', 'email': 'johndoe@example.com',
                                    'username': 'login1','phone_number': '1234567890', 'role': 'Instructor'})
        user.refresh_from_db()
        self.assertEqual(user.first_name, "Jane")
        self.assertEqual(user.last_name, "Doe")
        self.assertEqual(user.email, "johndoe@example.com")
        self.assertEqual(user.phone_number, "1234567890")
        self.assertEqual(user.role, "Instructor")
        self.assertEqual(User.objects.count(), 1)
        self.assertIn('message', response.context)
        self.assertEqual(response.context['message'], 'The user has been successfully updated')

        #everything shows up on the page properly
        self.assertContains(response, "Jane Doe")
        self.assertContains(response, "Instructor")
        self.assertContains(response, "No Courses.")
        self.assertContains(response, "johndoe@example.com")
        self.assertContains(response, "1234567890")



    def test_create_user_and_add_to_course(self):
        #create user
        response = self.donkey.post("/configureUser.html", {"first_name": "Instruct",
                                        "last_name": "Joe", "username": "login1",
                                        "password": "password1",
                                        "email": "EMAIL1@email.com", "phone_number": "1141234567",
                                        "address": "UWM1",
                                        "role": "Instructor", "form_name": "create_user"}, follow=True)
        self.assertEqual(User.objects.count(), 1, "The amount of users do not match")
        self.assertIn('message', response.context)
        self.assertEqual(response.context['message'], "The user \"Instruct Joe\" has been created")

        #add the user we created to a course that we create
        user = User.objects.get(username='login1')
        response = self.donkey.post("/configureCourse.html", {"form_name": "create_course",
            "instructors": User.objects.filter(role="Instructor"), "instructor": user, "course_name": "new_course"})
        self.assertEqual(Course.objects.count(), 1, "The amount of courses do not match")
        self.assertIn('message', response.context)
        self.assertEqual(response.context['message'], "The course \"new_course\" has been created")

        #test that it displays the course correctly
        self.assertContains(response, "new_course")
        self.assertContains(response, "Instructors")
        self.assertContains(response, "Instruct Joe")
        self.assertContains(response, "Edit Course")

    def test_create_user_and_course_and_add_to_lab(self):
        response = self.donkey.post("/configureUser.html", {"first_name": "Instruct",
                                    "last_name": "Joe", "username": "login1","password": "password1",
                                    "email": "EMAIL1@email.com", "phone_number": "1141234567","address": "UWM1",
                                    "role": "Instructor", "form_name": "create_user"}, follow=True)

        response = self.donkey.post("/configureUser.html", {"first_name": "TA",
                                    "last_name": "Jake", "username": "login2",
                                    "password": "password2","email": "EMAIL2@email.com", "phone_number": "1141234568",
                                    "address": "UWM2", "role": "TA", "form_name": "create_user"}, follow=True)

        self.assertEqual(User.objects.count(), 2, "The amount of users do not match")
        self.assertIn('message', response.context)
        self.assertEqual(response.context['message'], "The user \"TA Jake\" has been created")

        # add the user we created to a course that we create
        instructor = User.objects.get(username='login1')
        ta = User.objects.get(username='login2')
        response = self.donkey.post("/configureCourse.html", {"form_name": "create_course",
                                    "instructors": User.objects.filter(role="Instructor"),"instructor": instructor,
                                    "course_name": "new_course"})
        self.assertEqual(Course.objects.count(), 1, "The amount of courses do not match")
        self.assertIn('message', response.context)
        self.assertEqual(response.context['message'], "The course \"new_course\" has been created")

        course = Course.objects.get(name="new_course")

        response = self.donkey.post("/configureCourse.html", {"form_name": "create_lab",
                                                              "tas": User.objects.filter(role="TA"),
                                                              "ta": ta, "course":course ,"lab_name": "lab"})
        self.assertEqual(Lab.objects.count(), 1, "The amount of labs do not match")
        self.assertIn('message', response.context)
        self.assertEqual(response.context["message"], "The lab \"lab\" has been created")
        self.assertContains(response, "TAs and Labs")
        self.assertContains(response, "TA Jake (Teaching Assistant)")
        self.assertContains(response, "lab_name")
        self.assertContains(response, "Edit Lab")

    def test_change_assigned_instructor_role(self):
        response = self.donkey.post("/configureUser.html", {"first_name": "Instruct",
                                    "last_name": "Joe", "username": "login1",
                                    "password": "password1",
                                    "email": "EMAIL1@email.com", "phone_number": "1141234567",
                                    "address": "UWM1",
                                    "role": "Instructor", "form_name": "create_user"},follow=True)
        self.assertEqual(User.objects.count(), 1, "The amount of users do not match")
        self.assertIn('message', response.context)
        self.assertEqual(response.context['message'], "The user \"Instruct Joe\" has been created")

        # add the user we created to a course that we create
        instructor = User.objects.get(username='login1')
        response = self.donkey.post("/configureCourse.html", {"form_name": "create_course",
                                                              "instructors": User.objects.filter(role="Instructor"),
                                                              "instructor": instructor,
                                                              "course_name": "new_course"})
        self.assertEqual(Course.objects.count(), 1, "The amount of courses do not match")
        self.assertIn('message', response.context)
        self.assertEqual(response.context['message'], "The course \"new_course\" has been created")

        response = self.donkey.post("/configureUser.html", {"first_name": "Instructor",
                                    "last_name": "Joe", "username": "login1",
                                    "email": "EMAIL1@email.com",
                                    "phone_number": "1141234567",
                                    "role": "Admin","form_name": "edit_user"}, follow=True)

        response = self.donkey.get("/configureCourse.html")
        self.assertContains(response, "new_course")
        self.assertContains(response, "Instructors")
        self.assertContains(response, "No Instructor Assigned")
        self.assertContains(response, "Edit Course")

    def test_change_assigned_ta_role(self):
        response = self.donkey.post("/configureUser.html", {"first_name": "Instruct",
                                    "last_name": "Joe", "username": "login1",
                                    "password": "password1",
                                    "email": "EMAIL1@email.com", "phone_number": "1141234567",
                                    "address": "UWM1",
                                    "role": "Instructor", "form_name": "create_user"},follow=True)

        response = self.donkey.post("/configureUser.html", {"first_name": "TA",
                                    "last_name": "Jake", "username": "login2",
                                    "password": "password2", "email": "EMAIL2@email.com",
                                    "phone_number": "1141234568",
                                    "address": "UWM2", "role": "TA",
                                    "form_name": "create_user"}, follow=True)

        self.assertEqual(User.objects.count(), 2, "The amount of users do not match")
        self.assertIn('message', response.context)
        self.assertEqual(response.context['message'], "The user \"TA Jake\" has been created")

        # add the user we created to a course that we create
        instructor = User.objects.get(username='login1')
        ta = User.objects.get(username='login2')
        response = self.donkey.post("/configureCourse.html", {"form_name": "create_course",
                                                              "instructors": User.objects.filter(role="Instructor"),
                                                              "instructor": instructor,
                                                              "course_name": "new_course"})
        self.assertEqual(Course.objects.count(), 1, "The amount of courses do not match")
        self.assertIn('message', response.context)
        self.assertEqual(response.context['message'], "The course \"new_course\" has been created")

        course = Course.objects.get(name="new_course")

        response = self.donkey.post("/configureCourse.html", {"form_name": "create_lab",
                                                              "tas": User.objects.filter(role="TA"),
                                                              "ta": ta, "course": course, "lab_name": "lab"})
        self.assertEqual(Lab.objects.count(), 1, "The amount of labs do not match")

        response = self.donkey.post("/configureUser.html", {"first_name": "TA",
                                    "last_name": "Jake", "username": "login2",
                                    "email": "EMAIL2@email.com",
                                    "phone_number": "1141234568",
                                    "role": "Instructor","form_name": "edit_user"}, follow=True)

        response = self.donkey.get("/configureCourse.html")
        self.assertContains(response, "TAs and Labs")
        self.assertContains(response, "No TA Assigned")
        self.assertContains(response, "lab_name")
        self.assertContains(response, "Edit Lab")

    #integration tests still needed to write

    # all the filter tests for course directory
    def test_create_courses_and_filter(self):
        pass

    def test_create_labs_and_filter(self):
        pass

    def test_change_course_assignments_and_filter(self):
        pass

    def test_change_lab_assignments_and_filter(self):
        pass

    def test_change_user_role_and_filter(self):
        pass

    def test_filter_display_add_course_and_filter_again(self):
        pass

    #edit user and then their view in user directory

    def test_edited_user_display_in_user_directory(self):
        pass

    def test_edited_user_name_display_in_course_directory(self):
        pass

    # admin created then they are changed from admin so they can no longer access the admin home
    def test_create_admin_change_role_and_access_admin_home(self):
        pass

    # test for the unimplemented methods (edit course and edit lab)
    def test_create_course_edit_course_and_filter(self):
        pass

    def test_create_lab_and_course_edit_course_labs_and_filter(self):
        pass

    def test_create_lab_edit_lab_and_filter(self):
        pass



    #more that I might be missing?