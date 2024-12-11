from django.test import TestCase, Client
from djangoProject1.models import User, Course, Section


class IntegrationTests(TestCase):
    def setUp(self):
        self.donkey = Client()

    def test_create_and_view_user(self):
        #create the user
        response = self.donkey.post("/configure_user.html", {"first_name": "Administrator",
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
        response = self.donkey.post("/configure_user.html", {"first_name": "Administrator",
                                    "last_name": "Smith", "username": "login1","password": "password1",
                                    "email": "EMAIL1@email.com", "phone_number": "1141234567", "address": "UWM1",
                                    "role": "TA", "form_name": "create_user"}, follow=True)
        self.assertEqual(User.objects.count(), 1, "The amount of users do not match")
        self.assertIn('message', response.context)
        self.assertEqual(response.context['message'],"The user \"Administrator Smith\" has been created")

        #edit that user we created and check that it was edited properly
        user = User.objects.get(username='login1')
        response = self.donkey.post('/configure_user.html', {'id': user.id, 'first_name': 'Jane',
                                    "form_name": "edit_user", 'last_name': 'Doe', 'email': 'johndoe@example.com',
                                    'username': 'login1','phone_number': '1234567890', 'role': 'Instructor'})
        user.refresh_from_db()
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
        response = self.donkey.post("/configure_user.html", {"first_name": "Instruct",
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
        response = self.donkey.post("/configure_course.html", {"form_name": "create_course",
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
        response = self.donkey.post("/configure_user.html", {"first_name": "Instruct",
                                    "last_name": "Joe", "username": "login1","password": "password1",
                                    "email": "EMAIL1@email.com", "phone_number": "1141234567","address": "UWM1",
                                    "role": "Instructor", "form_name": "create_user"}, follow=True)

        response = self.donkey.post("/configure_user.html", {"first_name": "TA",
                                    "last_name": "Jake", "username": "login2",
                                    "password": "password2","email": "EMAIL2@email.com", "phone_number": "1141234568",
                                    "address": "UWM2", "role": "TA", "form_name": "create_user"}, follow=True)

        self.assertEqual(User.objects.count(), 2, "The amount of users do not match")
        self.assertIn('message', response.context)
        self.assertEqual(response.context['message'], "The user \"TA Jake\" has been created")

        # add the user we created to a course that we create
        instructor = User.objects.get(username='login1')
        ta = User.objects.get(username='login2')
        response = self.donkey.post("/configure_course.html", {"form_name": "create_course",
                                    "instructors": User.objects.filter(role="Instructor"),"instructor": instructor,
                                    "course_name": "new_course"})
        self.assertEqual(Course.objects.count(), 1, "The amount of courses do not match")
        self.assertIn('message', response.context)
        self.assertEqual(response.context['message'], "The course \"new_course\" has been created")

        course = Course.objects.get(name="new_course")

        response = self.donkey.post("/configure_course.html", {"form_name": "create_lab",
                                                              "tas": User.objects.filter(role="TA"),
                                                              "ta": ta, "course":course ,"lab_name": "lab"})
        self.assertEqual(Section.objects.count(), 1, "The amount of labs do not match")
        self.assertIn('message', response.context)
        self.assertEqual(response.context["message"], "The lab \"lab\" has been created")
        self.assertContains(response, "TAs and Labs")
        self.assertContains(response, "TA Jake (Teaching Assistant)")
        self.assertContains(response, "lab_name")
        self.assertContains(response, "Edit Lab")

    def test_change_assigned_instructor_role(self):
        response = self.donkey.post("/configure_user.html", {"first_name": "Instruct",
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
        response = self.donkey.post("/configure_course.html", {"form_name": "create_course",
                                                              "instructors": User.objects.filter(role="Instructor"),
                                                              "instructor": instructor,
                                                              "course_name": "new_course"})
        self.assertEqual(Course.objects.count(), 1, "The amount of courses do not match")
        self.assertIn('message', response.context)
        self.assertEqual(response.context['message'], "The course \"new_course\" has been created")

        response = self.donkey.post("/configure_user.html", {"first_name": "Instructor",
                                    "last_name": "Joe", "username": "login1",
                                    "email": "EMAIL1@email.com",
                                    "phone_number": "1141234567",
                                    "role": "Admin","form_name": "edit_user"}, follow=True)

        response = self.donkey.get("/configure_course.html")
        self.assertContains(response, "new_course")
        self.assertContains(response, "Instructors")
        self.assertContains(response, "No Instructor Assigned")
        self.assertContains(response, "Edit Course")

    def test_change_assigned_ta_role(self):
        response = self.donkey.post("/configure_user.html", {"first_name": "Instruct",
                                    "last_name": "Joe", "username": "login1",
                                    "password": "password1",
                                    "email": "EMAIL1@email.com", "phone_number": "1141234567",
                                    "address": "UWM1",
                                    "role": "Instructor", "form_name": "create_user"},follow=True)

        response = self.donkey.post("/configure_user.html", {"first_name": "TA",
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
        response = self.donkey.post("/configure_course.html", {"form_name": "create_course",
                                                              "instructors": User.objects.filter(role="Instructor"),
                                                              "instructor": instructor,
                                                              "course_name": "new_course"})
        self.assertEqual(Course.objects.count(), 1, "The amount of courses do not match")
        self.assertIn('message', response.context)
        self.assertEqual(response.context['message'], "The course \"new_course\" has been created")

        course = Course.objects.get(name="new_course")

        response = self.donkey.post("/configure_course.html", {"form_name": "create_lab",
                                                              "tas": User.objects.filter(role="TA"),
                                                              "ta": ta, "course": course, "lab_name": "lab"})
        self.assertEqual(Section.objects.count(), 1, "The amount of labs do not match")

        response = self.donkey.post("/configure_user.html", {"first_name": "TA",
                                    "last_name": "Jake", "username": "login2",
                                    "email": "EMAIL2@email.com",
                                    "phone_number": "1141234568",
                                    "role": "Instructor","form_name": "edit_user"}, follow=True)

        response = self.donkey.get("/configure_course.html")
        self.assertContains(response, "TAs and Labs")
        self.assertContains(response, "No TA Assigned")
        self.assertContains(response, "lab_name")
        self.assertContains(response, "Edit Lab")

    #integration tests still needed to write

    # all the filter tests for course directory
    def test_create_courses_and_filter(self):

        # create users
        response = self.donkey.post("/configure_user.html", {"first_name": "Instruct",
                                    "last_name": "Joe", "username": "login1",
                                    "password": "password1",
                                    "email": "EMAIL1@email.com", "phone_number": "1141234567",
                                    "address": "UWM1",
                                    "role": "Instructor", "form_name": "create_user"},follow=True)
        response = self.donkey.post("/configure_user.html", {"first_name": "Ructor",
                                    "last_name": "Jack", "username": "login2",
                                    "password": "password2",
                                    "email": "EMAIL2@email.com", "phone_number": "4141234567",
                                    "address": "UWM2",
                                    "role": "Instructor", "form_name": "create_user"},follow=True)
        self.assertEqual(User.objects.count(), 2, "The amount of users do not match")

        # add the user we created to a course that we create
        user1 = User.objects.get(username='login1')
        response = self.donkey.post("/configure_course.html", {"form_name": "create_course",
                                    "instructors": User.objects.filter(role="Instructor"),
                                    "instructor": user1, "course_name": "new_course1"})

        user2 = User.objects.get(username='login2')
        response = self.donkey.post("/configure_course.html", {"form_name": "create_course",
                                    "instructors": User.objects.filter(role="Instructor"),
                                    "instructor": user2, "course_name": "new_course2"})
        self.assertEqual(Course.objects.count(), 2, "The amount of courses do not match")


        #login as one of the instructors
        response = self.donkey.post("/", {"username":"login1", "password":"password1"}, follow=True)
        response = self.donkey.get("/course_directory.html")
        self.assertContains(response, "new_course1")
        self.assertContains(response, "Instruct Joe (Instructor)")
        self.assertContains(response, "No labs available.")
        self.assertContains(response, "new_course2")
        self.assertContains(response, "Ructor Jack (Instructor)")

        #apply the filter and check if it changes properly
        response = self.donkey.get("/course_directory.html?filter=assigned")
        self.assertContains(response, "new_course1")
        self.assertContains(response, "Instruct Joe (Instructor)")
        self.assertContains(response, "No labs available.")
        self.assertNotContains(response, "new_course2")
        self.assertNotContains(response, "Ructor Jack (Instructor)")


    def test_create_labs_and_filter(self):
        # create users, 1 Instructor, 2 TAs
        response = self.donkey.post("/configure_user.html", {"first_name": "Instruct",
                                    "last_name": "Joe", "username": "login1",
                                    "password": "password1",
                                    "email": "EMAIL1@email.com", "phone_number": "1141234567",
                                    "address": "UWM1",
                                    "role": "Instructor", "form_name": "create_user"},
                                    follow=True)
        response = self.donkey.post("/configure_user.html", {"first_name": "T",
                                    "last_name": "Jack", "username": "login2",
                                    "password": "password2",
                                    "email": "EMAIL2@email.com", "phone_number": "4141234567",
                                    "address": "UWM2",
                                    "role": "TA", "form_name": "create_user"},follow=True)

        response = self.donkey.post("/configure_user.html", {"first_name": "A",
                                    "last_name": "Kash", "username": "login3",
                                    "password": "password3",
                                    "email": "EMAIL3@email.com", "phone_number": "7141234567",
                                    "address": "UWM3",
                                    "role": "TA", "form_name": "create_user"}, follow=True)

        self.assertEqual(User.objects.count(), 3, "The amount of users do not match")

        # add the user we created to a course that we create
        user1 = User.objects.get(username='login1')
        response = self.donkey.post("/configure_course.html", {"form_name": "create_course",
                                                              "instructors": User.objects.filter(role="Instructor"),
                                                              "instructor": user1, "course_name": "new_course1"})

        response = self.donkey.post("/configure_course.html", {"form_name": "create_course",
                                                              "instructors": User.objects.filter(role="Instructor"),
                                                              "instructor": user1, "course_name": "new_course2"})
        self.assertEqual(Course.objects.count(), 2, "The amount of courses do not match")

        # add the tas and courses to new labs we create
        course1 = Course.objects.get(name="new_course1")
        user2 = User.objects.get(username='login2')
        response = self.donkey.post("/configure_course.html",
                                    {"tas": User.objects.filter(role="TA"), "ta": user2,
                                    "lab_name": "new_lab1", "course": course1, "form_name": "create_lab"},
                                    follow=True)

        course2 = Course.objects.get(name="new_course2")
        user3 = User.objects.get(username='login3')
        response = self.donkey.post("/configure_course.html",
                                    {"tas": User.objects.filter(role="TA"), "ta": user3,
                                     "lab_name": "new_lab2", "course": course2, "form_name": "create_lab"},
                                    follow=True)
        self.assertEqual(Section.objects.count(), 2, "The amount of labs do not match")

        # login as ta then filter
        response = self.donkey.post("/", {"username": "login2", "password": "password2"}, follow=True)
        response = self.donkey.get("/course_directory.html")
        self.assertContains(response, "new_course1")
        self.assertContains(response, "Instruct Joe (Instructor)")
        self.assertContains(response, "Lab: new_lab1")
        self.assertContains(response, "new_course2")
        self.assertContains(response, "Lab: new_lab2")

        # apply filter
        response = self.donkey.get("/course_directory.html?filter=assigned")
        self.assertContains(response, "new_course1")
        self.assertContains(response, "Instruct Joe (Instructor)")
        self.assertContains(response, "Lab: new_lab1")
        self.assertNotContains(response, "new_course2")
        self.assertNotContains(response, "Lab: new_lab2")

    def test_change_user_role_and_filter(self):
        response = self.donkey.post("/configure_user.html", {"first_name": "Instruct",
                                    "last_name": "Joe", "username": "login1",
                                    "password": "password1",
                                    "email": "EMAIL1@email.com", "phone_number": "1141234567",
                                    "address": "UWM1",
                                    "role": "Instructor", "form_name": "create_user"},
                                    follow=True)
        response = self.donkey.post("/configure_user.html", {"first_name": "Ructor",
                                    "last_name": "Jack", "username": "login2",
                                    "password": "password2",
                                    "email": "EMAIL2@email.com", "phone_number": "4141234567",
                                    "address": "UWM2",
                                    "role": "Instructor", "form_name": "create_user"},
                                    follow=True)
        self.assertEqual(User.objects.count(), 2, "The amount of users do not match")

        # add the user we created to a course that we create
        user1 = User.objects.get(username='login1')
        response = self.donkey.post("/configure_course.html", {"form_name": "create_course",
                                  "instructors": User.objects.filter(role="Instructor"),
                                  "instructor": user1, "course_name": "new_course1"})

        user2 = User.objects.get(username='login2')
        response = self.donkey.post("/configure_course.html", {"form_name": "create_course",
                                  "instructors": User.objects.filter(role="Instructor"),
                                  "instructor": user2, "course_name": "new_course2"})
        self.assertEqual(Course.objects.count(), 2, "The amount of courses do not match")

        #change the user's role
        response = self.donkey.post('/configure_user.html',
                                    {'id': user1.id, 'first_name': 'Instruct',
                                     "form_name": "edit_user",'last_name': 'Joe',
                                     "email": "EMAIL1@email.com", "phone_number": "1141234567",
                                     "address": "UWM1","role": "Admin",'username': 'login1'})
        user1.refresh_from_db()

        #login to see after role change
        response = self.donkey.post("/", {"username": "login1", "password": "password1"}, follow=True)
        response = self.donkey.get("/course_directory.html")
        self.assertContains(response, "new_course1")
        self.assertContains(response, "No instructors assigned.")
        self.assertContains(response, "No labs available.")
        self.assertContains(response, "new_course2")
        self.assertContains(response, "Ructor Jack (Instructor)")

        # apply filter
        response = self.donkey.get("/course_directory.html?filter=assigned")
        self.assertContains(response, "new_course1")
        self.assertContains(response, "No instructors assigned.")
        self.assertContains(response, "No labs available.")
        self.assertContains(response, "new_course2")
        self.assertContains(response, "Ructor Jack (Instructor)")




    def test_filter_display_add_course_and_filter_again(self):
        response = self.donkey.post("/configure_user.html", {"first_name": "Instruct",
                                    "last_name": "Joe", "username": "login1",
                                    "password": "password1",
                                    "email": "EMAIL1@email.com", "phone_number": "1141234567",
                                    "address": "UWM1",
                                    "role": "Instructor", "form_name": "create_user"},
                                    follow=True)

        user1 = User.objects.get(username='login1')
        response = self.donkey.post("/configure_course.html", {"form_name": "create_course",
                                    "instructors": User.objects.filter(role="Instructor"),
                                    "instructor": user1, "course_name": "new_course1"})

        # login as one of the instructors to check view
        response = self.donkey.post("/", {"username": "login1", "password": "password1"}, follow=True)
        response = self.donkey.get("/course_directory.html")
        self.assertContains(response, "new_course1")
        self.assertContains(response, "Instruct Joe (Instructor)")
        self.assertContains(response, "No labs available.")

        # apply the filter and check if it changes properly
        response = self.donkey.get("/course_directory.html?filter=assigned")
        self.assertContains(response, "new_course1")
        self.assertContains(response, "Instruct Joe (Instructor)")
        self.assertContains(response, "No labs available.")

        response = self.donkey.post("/configure_user.html", {"first_name": "Ructor",
                                    "last_name": "Jack", "username": "login2",
                                    "password": "password2",
                                    "email": "EMAIL2@email.com", "phone_number": "4141234567",
                                    "address": "UWM2",
                                    "role": "Instructor", "form_name": "create_user"},
                                    follow=True)
        user2 = User.objects.get(username='login2')
        response = self.donkey.post("/configure_course.html", {"form_name": "create_course",
                                                              "instructors": User.objects.filter(role="Instructor"),
                                                              "instructor": user2, "course_name": "new_course2"})

        # login as one of the instructors
        response = self.donkey.post("/", {"username": "login1", "password": "password1"}, follow=True)
        response = self.donkey.get("/course_directory.html")
        self.assertContains(response, "new_course1")
        self.assertContains(response, "Instruct Joe (Instructor)")
        self.assertContains(response, "No labs available.")
        self.assertContains(response, "new_course2")
        self.assertContains(response, "Ructor Jack (Instructor)")

        # apply the filter and check if it changes properly
        response = self.donkey.get("/course_directory.html?filter=assigned")
        self.assertContains(response, "new_course1")
        self.assertContains(response, "Instruct Joe (Instructor)")
        self.assertContains(response, "No labs available.")
        self.assertNotContains(response, "new_course2")
        self.assertNotContains(response, "Ructor Jack (Instructor)")

    #edit user and then their view in user directory

    def test_edited_user_display_in_user_directory(self):
        # create the user
        response = self.donkey.post("/configure_user.html", {"first_name": "Administrator",
                                    "last_name": "Smith", "username": "login1",
                                    "password": "password1",
                                    "email": "EMAIL1@email.com", "phone_number": "1141234567",
                                    "address": "UWM1",
                                    "role": "TA", "form_name": "create_user"}, follow=True)
        self.assertEqual(User.objects.count(), 1, "The amount of users do not match")
        self.assertIn('message', response.context)
        self.assertEqual(response.context['message'], "The user \"Administrator Smith\" has been created")

        # edit that user we created and check that it was edited properly
        user = User.objects.get(username='login1')
        response = self.donkey.post('/configure_user.html', {'id': user.id, 'first_name': 'Jane',
                                    "form_name": "edit_user", 'last_name': 'Doe',
                                    'email': 'johndoe@example.com',
                                    'username': 'login1', 'phone_number': '1234567890',
                                    'role': 'Instructor'})
        user.refresh_from_db()
        self.assertIn('message', response.context)
        self.assertEqual(response.context['message'], 'The user has been successfully updated')

        # everything shows up user directory properly
        response = self.donkey.post("/", {"username": "login1", "password": "password1"}, follow=True)
        response = self.donkey.get("/user_directory.html")
        self.assertContains(response, "Jane Doe")
        self.assertContains(response, "Instructor")
        self.assertContains(response, "No courses assigned.")
        self.assertContains(response, "johndoe@example.com")
        self.assertContains(response, "1234567890")

    def test_edited_user_name_display_in_course_directory(self):
        # create the instructor
        response = self.donkey.post("/configure_user.html", {"first_name": "Instructor",
                                    "last_name": "Smith", "username": "login1",
                                    "password": "password1",
                                    "email": "EMAIL1@email.com", "phone_number": "1141234567",
                                    "address": "UWM1",
                                    "role": "Instructor", "form_name": "create_user"}, follow=True)
        self.assertEqual(User.objects.count(), 1, "The amount of users do not match")
        self.assertIn('message', response.context)
        self.assertEqual(response.context['message'], "The user \"Instructor Smith\" has been created")

        #create a course for the instructor
        user = User.objects.get(username='login1')
        response = self.donkey.post("/configure_course.html", {"form_name": "create_course",
                                    "instructors": User.objects.filter(role="Instructor"),
                                    "instructor": user, "course_name": "new_course"})
        self.assertEqual(Course.objects.count(), 1, "The amount of courses do not match")
        self.assertIn('message', response.context)
        self.assertEqual(response.context['message'], "The course \"new_course\" has been created")

        # edit that users name and check how it shows up in the course directory
        user = User.objects.get(username='login1')
        response = self.donkey.post('/configure_user.html', {'id': user.id, 'first_name': 'Jane',
                                    "form_name": "edit_user", 'last_name': 'Doe',
                                    'email': 'EMAIL1@email.com', 'phone_number': '1141234567',
                                    'username': 'login1',
                                    'role': 'Instructor'})
        user.refresh_from_db()
        self.assertIn('message', response.context)
        self.assertEqual(response.context['message'], 'The user has been successfully updated')

        # check how they show up in the course directory
        response = self.donkey.post("/", {"username": "login1", "password": "password1"}, follow=True)
        response = self.donkey.get("/course_directory.html")
        self.assertContains(response, "new_course")
        self.assertContains(response, "Jane Doe (Instructor)")
        self.assertContains(response, "No labs available.")



    # admin created then they are changed from admin so they can no longer access the admin home
    def test_create_admin_change_role_and_access_admin_home(self):
        response = self.donkey.post("/configure_user.html", {"first_name": "Administrator",
                                    "last_name": "Smith", "username": "login1",
                                    "password": "password1",
                                    "email": "EMAIL1@email.com", "phone_number": "1141234567",
                                    "address": "UWM1",
                                    "role": "Admin", "form_name": "create_user"},
                                    follow=True)

        user = User.objects.get(username='login1')
        response = self.donkey.post('/configure_user.html', {'id': user.id, 'first_name': 'Administrator',
                                                            "form_name": "edit_user", 'last_name': 'Smith',
                                                            'email': 'EMAIL1@email.com',
                                                            'username': 'login1', 'phone_number': '1141234567',
                                                            'role': 'Instructor'})
        user.refresh_from_db()

        response = self.donkey.post("/", {"username": "login1", "password": "password1"}, follow=True)
        response = self.donkey.get("/admin_home.html")
        self.assertEqual(response.status_code, 200)
        self.assertIn("message", response.context)
        self.assertEqual(response.context["message"], "You cannot access this page.")
        self.assertTemplateUsed(response, "home.html")

    def test_change_course_instructor_assignments_and_filter(self):
        pass

    def test_change_lab_ta_assignments_and_filter(self):
        pass

    def test_create_course_edit_course_and_filter(self):
        pass

    def test_create_lab_and_course_edit_course_labs_and_filter(self):
        pass

    def test_create_lab_edit_lab_and_filter(self):
        pass
