from sys import set_coroutine_origin_tracking_depth

from django.shortcuts import render, redirect
from django.views import View

from djangoProject1.MethodFiles.Administrator import CreateCourse, CreateUser, CreateSection, EditUser, EditCourse, \
    EditSection, RemoveUser, EditPersonalUser
from djangoProject1.MethodFiles.GeneralMethods import GetUser, CheckPermission
from djangoProject1.models import User, Course, Section, DAYS_OF_WEEK
from datetime import time


class LoginPage(View):
    def get(self, request):
        if GetUser.get_user(request) is not None:
            del request.session['cur_user_name']
        return render(request, "login.html", {})

    def post(self, request):
        # get the entered username and password in the form
        username = request.POST['username']
        password = request.POST['password']

        # filters to see if the user of the specified username is within the database
        user = User.objects.filter(username=username)

        # if we find a match then we proceed to check if the password matches
        if user.exists():
            # check for valid password, if valid then redirect to home page, if not then show the error message on login page
            if user[0].password == password:
                # if we have a match this stores the user's username this can be used to access the current user's data
                # in all the other pages using this: user = GetUser.get_user(request)
                request.session['cur_user_name'] = user[0].username
                return redirect("home.html")
            else:
                message = "Username or Password is incorrect"
                return render(request, "login.html", {'message': message})

        # If we have an invalid username then print this message on the login page
        else:
            message = "Username or Password is incorrect"
            return render(request, "login.html", {'message': message})


class ConfigureUserPage(View):
    def get(self, request):
        users = User.objects.all()

        # Display the courses assigned to that user, if the user is a instructor
        user = GetUser.get_user(request)
        if not user:
            return redirect('/')

        return render(request, "configure_user.html",
                      {"roles": User.ROLE_CHOICES, "users": users})

    def post(self, request):
        # filter to see which form is being accessed:
        form = request.POST.get('form_name')
        # Get the required fields for creating a user

        # course_name = request.POST['name']

        users = User.objects.all()
        if form == "create_user":
            firstname = request.POST['first_name']
            lastname = request.POST['last_name']
            username = request.POST['username']
            # course= request.POST['name']
            email = request.POST['email']
            phone = request.POST['phone_number']
            role = request.POST['role']
            password = request.POST['password']
            address = request.POST['address']
            skills = request.POST['skills']
            return self.addUserHelper(username, email, password, firstname, lastname, phone, address, role, skills, request)

        elif form == "edit_user":
            firstname = request.POST['first_name']
            lastname = request.POST['last_name']
            username = request.POST['username']
            email = request.POST['email']
            phone = request.POST['phone_number']
            role = request.POST['role']
            address = request.POST['address']
            skills = request.POST['skills']
            return self.editUserHelper(request, username, firstname, lastname, phone, email, role, address, skills, users)

        elif form == "remove_user":
            user_id = request.POST['user_id']
            return self.removeUserHelper(request, user_id)
        else:
            return render(request, "configure_user.html", {"roles": User.ROLE_CHOICES, "users": users,
                                                           'message': "Something went wrong when fetching the form, please try again"})

    # helper class to enable the addition of user
    def addUserHelper(self, username, email, password, firstname, lastname, phone, address, role, skills, request):

        # course_name = request.POST['name']

        name = firstname + " " + lastname

        # Create user:
        user = CreateUser.create_user(username, email, password, firstname, lastname, phone, address, role, skills)

        # Get all users to pass to the templateDesign
        all_users = User.objects.all()

        if user is None:
            return render(request, "configure_user.html", {
                "roles": User.ROLE_CHOICES,
                "users": all_users,
                'message': "Something went wrong when creating the user \"" + name + "\""})
        else:
            return render(request, "configure_user.html", {
                "roles": User.ROLE_CHOICES,
                "users": all_users,
                'message': "The user \"" + name + "\" has been created"})

    # Helper class to save/edit the user
    def editUserHelper(self, request, username, firstname, lastname, phone, email, role, address, skills, users,):
        user = EditUser.edit_user(request, username, firstname, lastname, phone, email, role, address, skills)
        if user is None:
            return render(request, "configure_user.html",
                          {"roles": User.ROLE_CHOICES, "users": users,
                           "message": "Something went wrong when updating the user"})
        else:
            return render(request, "configure_user.html",
                          {"roles": User.ROLE_CHOICES, "users": users,
                           "message": "The user has been successfully updated"})

    # Helper class to remove the user
    def removeUserHelper(self, request, user_id):
        user_id = request.POST.get('user_id')
        message = RemoveUser.remove_user(user_id)
        users = User.objects.all()
        return render(request, "configure_user.html", {
            "roles": User.ROLE_CHOICES,
            "users": users,
            "message": message
        })

class UserDirectoryPage(View):
    def get(self, request):
        users = User.objects.all()
        courses = Course.objects.all()
        sections = Section.objects.all()
        return render(request, "user_directory.html", {"users": users, "courses": courses, "sections": sections})

    def post(self, request):
        return redirect('/home/')


class CourseDirectoryPage(View):
    def get(self, request):
        # pull logged-in user
        user = GetUser.get_user(request)
        if user is None:
            return redirect('/')  # Redirect to login if no user session exists

        # check for filtering in the query parameters
        filter_assigned = request.GET.get('filter') == 'assigned'

        # default to all courses
        courses = Course.objects.all()

        # apply filtering based on role
        if filter_assigned:
            if user.role == 'TA' or user.role == 'Instructor':
                courses = Course.objects.filter(users=user)

        return render(request, "course_directory.html",
                      {'courses': courses, 'user': user, 'filter_assigned': filter_assigned})

    def post(self, request):
        courses = Course.objects.all()
        return render(request, "course_directory.html", {'courses': courses})


class ProfilePage(View):
    def get(self, request):
        users = User.objects.all()
        user = GetUser.get_user(request)
        if not user:
            return redirect('/')

        return render(request, "profile_page.html",
                      {"roles": User.ROLE_CHOICES, "users": users})

    def post(self, request):
        form = request.POST.get('form_name')

        users = User.objects.all()
        if form == "edit_user":
            firstname = request.POST['first_name']
            lastname = request.POST['last_name']
            username = request.POST['username']
            password = request.POST['password']
            email = request.POST['email']
            phone = request.POST['phone_number']
            role = request.POST['role']
            address = request.POST['address']
            skills = request.POST['skills']
            return self.editPersonalInfoHelper(request, username, firstname, lastname, phone, email, role, address, skills,
                                       users)
        else:
            return render(request, "profile_page.html", {"roles": User.ROLE_CHOICES, "users": users,})

    def editPersonalInfoHelper(self, request, username, firstname, lastname, phone, email, role, address, skills,
                                       users):
        user = EditPersonalUser.edit_personal_user(request, username, firstname, lastname, phone, email, role, address, skills,
                                       users)
        if user is None:
            return render(request, "profile_page.html",
                          {"roles": User.ROLE_CHOICES, "users": users,
                           "message": "Something went wrong when updating your info"})
        else:
            return render(request, "configure_user.html",
                          {"roles": User.ROLE_CHOICES, "users": users,
                           "message": "Your information has been successfully updated"})

class HomePage(View):
    def get(self, request):
        return render(request, "home.html", {})


class AdminHomePage(View):
    def get(self, request):
        user = GetUser.get_user(request)
        can_access = CheckPermission.check_admin(user)
        if not can_access:
            return render(request, "home.html", {'message': "You cannot access this page."})

        # database selection
        selected_db = request.GET.get('database', 'users')  # default to users
        data = None
        if selected_db == 'users':
            data = User.objects.all()
        elif selected_db == 'courses':
            data = Course.objects.all()
        elif selected_db == 'sections':
            data = Section.objects.all()

        return render(request, "admin_home.html", {'selected_db': selected_db, 'data': data})


class ConfigureCoursePage(View):
    def get(self, request):
        # make this into a method
        courses = Course.objects.all()
        instructors = User.objects.filter(role="Instructor")
        tas = User.objects.filter(role="TA")
        sections = Section.objects.all()
        users = User.objects.all()
        return render(request, "configure_course.html",
                      {"instructors": instructors, "tas": tas, "courses": courses, 'sections': sections,
                       'days': DAYS_OF_WEEK, 'users': users})

    def post(self, request):
        # this is to filter based on which form is being accessed
        form = request.POST.get('form_name')
        course_name = request.POST.get('name')
        course_id = request.POST.get('course_id')
        courses = Course.objects.all()
        # get the list of the instructors so that we can show it
        instructors = User.objects.filter(role="Instructor")
        tas = User.objects.filter(role="TA")
        sections = Section.objects.all()
        users = User.objects.all()

        if form == "create_course":
            return self.add_course_helper(courses, instructors, tas, sections, request)
        elif form == "create_section":
            return self.add_section_helper(request, courses, instructors, tas, sections, users)
        elif form == "edit_course":
            return self.edit_course_helper(course_id, request)
        elif form == "edit_section":
            return self.edit_section_helper(request, courses, instructors, tas, sections, users)
        else:
            return render(request, "configure_course.html", {"instructors": instructors, "tas": tas,
                                                             'courses': courses,
                                                             'message': "Something went wrong when fetching the form, please try again."})

    def add_course_helper(self, courses, instructors, tas, sections, request):
        instructor_ids = request.POST.getlist('instructors')
        ta_ids = request.POST.getlist('tas')
        cname = request.POST['course_name']

        selected_instructors = list(User.objects.filter(id__in=instructor_ids))
        selected_tas = list(User.objects.filter(id__in=ta_ids))

        users = []
        for instructor in selected_instructors:
            users.append(instructor)

        for ta in selected_tas:
            users.append(ta)


        # will return None if the creation failed, will return a course and save it to the database if it succeeded
        course = CreateCourse.create_course(cname, users)
        if course is None:
            return render(request, "configure_course.html", {"instructors": instructors, "tas": tas,
                                                             'courses': courses, 'sections': sections,
                                                             'message': "Something went wrong when creating the course \"" + cname + "\""})
        else:
            #* unpacks the instructors and tas list so it adds individual objects
            return render(request, "configure_course.html", {"instructors": instructors, "tas": tas,
                                                             'courses': courses, 'sections': sections,
                                                             'message': "The course \"" + cname + "\" has been created"})

    def add_section_helper(self, request, courses, instructors, tas, sections, users):
        # get all of the variables we will need to create the course
        section_name = request.POST['section_name']
        course_name = request.POST['section_course']
        user_id = request.POST['section_user']
        section_days = request.POST.getlist('section_days')  # must getlist otherwise it just gives 1 day
        section_time = request.POST['section_time']
        section_location = request.POST['section_location']

        # convert the values course, user, and scheduled_time to be the way that we want them to be
        if course_name != "":
            course = Course.objects.get(name=course_name)
        else:
            course = None

        if user_id != "":
            user = User.objects.get(id=user_id)
        else:
            user = None

        if ":" in section_time:
            time_parts = section_time.split(":")
            scheduled_time = time(int(time_parts[0]), int(time_parts[1]))
        else:
            scheduled_time = None

        # create the section with the parameters, returns None on failure, returns the new created section and saves it on success
        section = CreateSection.create_section(section_name, course, user, section_days, scheduled_time,
                                               section_location)
        # section_id = request.POST.get('section_id')
        # days_selected = request.POST.getlist('days')  # Get list of days from the form
        # section = Section.objects.get(id=section_id)
        # section.days = days_selected  # Assign the selected days to the section
        # section.save()
        sections = Section.objects.all()
        if section is None:
            return render(request, "configure_course.html", {'courses': courses, 'sections': sections,
                                                             'users': users, 'tas': tas, 'instructors': instructors,
                                                             'days': DAYS_OF_WEEK,
                                                             'message': "Something went wrong when creating the section \"" + section_name + "\""})
        else:
            return render(request, "configure_course.html", {'courses': courses, 'sections': sections,
                                                             'users': users, 'tas': tas, 'instructors': instructors,
                                                             'days': DAYS_OF_WEEK,
                                                             'message': "The section \"" + section_name + "\" has been created"})

    def edit_course_helper(self, courses, instructors, tas, sections, request):
        instructor_ids = request.POST.getlist('instructors')
        ta_ids = request.POST.getlist('tas')
        cname = request.POST['course_name']

        selected_instructors = User.objects.filter(id__in=instructor_ids)
        selected_tas = User.objects.filter(id__in=ta_ids)

        updated_course = EditCourse.edit_course(cname, list(selected_instructors), list(selected_tas))
        if updated_course:
            message = f"Course '{updated_course.name}' was updated successfully."
        else:
            message = "Failed to update course. Please check your inputs and try again."

        return redirect('configure_course')


    def edit_section_helper(self, request, courses, instructors, tas, sections, users):
        # get all of the data we need
        section_id = request.POST['section_id']
        section_name = request.POST['section_name']
        course_name = request.POST['section_course']
        user_id = request.POST['section_user']
        section_days = request.POST.getlist('section_days')
        section_time = request.POST['section_time']
        section_location = request.POST['section_location']

        # convert the course, user, and time to be the way that we want them to be
        if course_name != "":
            section_course = Course.objects.get(name=course_name)
        else:
            section_course = None

        if user_id != "":
            section_user = User.objects.get(id=user_id)
        else:
            section_user = None

        if ":" in section_time:
            time_parts = section_time.split(":")
            section_time = time(int(time_parts[0]), int(time_parts[1]))
        else:
            section_time = None

        edited_section = EditSection.edit_section(request, section_id, section_name, section_course, section_user,
                                                  section_days, section_time, section_location)

        # return things the way we would like to
        if edited_section is not None:
            return render(request, "configure_course.html", {'courses': courses, 'sections': sections,
                                                             'users': users, 'tas': tas, 'instructors': instructors,
                                                             'days': DAYS_OF_WEEK,
                                                             'message': "The section has been successfully edited"})
        else:
            return render(request, "configure_course.html", {'courses': courses, 'sections': sections,
                                                             'users': users, 'tas': tas, 'instructors': instructors,
                                                             'days': DAYS_OF_WEEK,
                                                             'message': "Something went wrong when editing the section"})


class EditSectionAssignmentPage(View):
    def get(self, request):
        return render(request, "edit_section_assignment.html", {})