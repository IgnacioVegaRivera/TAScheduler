from sys import set_coroutine_origin_tracking_depth

from django.shortcuts import render, redirect
from django.views import View

from djangoProject1.MethodFiles.Administrator import CreateCourse, CreateUser, CreateSection, EditUser, EditCourse, EditLab
from djangoProject1.MethodFiles.GeneralMethods import GetUser, CheckPermission
from djangoProject1.models import User, Course, Section, DAYS_OF_WEEK
from datetime import time


class LoginPage(View):
    def get(self, request):
        if GetUser.get_user(request) is not None:
            del request.session['cur_user_name']
        return render(request, "login.html", {})

    def post(self, request):
        #get the entered username and password in the form
        username = request.POST['username']
        password = request.POST['password']

        #filters to see if the user of the specified username is within the database
        user = User.objects.filter(username=username)

        #if we find a match then we proceed to check if the password matches
        if user.exists():
            #check for valid password, if valid then redirect to home page, if not then show the error message on login page
            if user[0].password == password:
                #if we have a match this stores the user's username this can be used to access the current user's data
                #in all the other pages using this: user = GetUser.get_user(request)
                request.session['cur_user_name'] = user[0].username
                return redirect("home.html")
            else:
                message = "Username or Password is incorrect"
                return render(request, "login.html", {'message': message})

        #If we have an invalid username then print this message on the login page
        else:
            message = "Username or Password is incorrect"
            return render(request, "login.html", {'message': message})



class ConfigureUserPage(View):
    def get(self, request):
        users = User.objects.all()

        #Display the courses assigned to that user, if the user is a instructor
        user = GetUser.get_user(request)
        if not user:
            return redirect('/')


        return render(request, "configure_user.html",
                      {"roles": User.ROLE_CHOICES, "users": users})

    def post(self, request):
        #filter to see which form is being accessed:
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
            return self.addUserHelper(username, email, password, firstname, lastname, phone, address, role, request)
        elif form == "edit_user":
            firstname = request.POST['first_name']
            lastname = request.POST['last_name']
            username = request.POST['username']
            # course= request.POST['name']
            email = request.POST['email']
            phone = request.POST['phone_number']
            role = request.POST['role']
            return self.editUserHelper(request, username, firstname, lastname, phone, email, role, users)
        elif form == "remove_user":
            user_id = request.POST['user_id']
            return render(request, "configure_user.html", {"roles": User.ROLE_CHOICES, "users": users,
                                                           'message': "Something went wrong when fetching the form, please try again"})
        else:
            return render(request, "configure_user.html", {"roles": User.ROLE_CHOICES, "users": users,
                                        'message': "Something went wrong when fetching the form, please try again"})

    #helper class to enable the addition of user
    def addUserHelper(self, username, email, password, firstname, lastname, phone, address, role, request):

        # course_name = request.POST['name']

        name = firstname + " " + lastname

        # Create user:
        user = CreateUser.create_user(username, email, password, firstname, lastname, phone, address, role)

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

    #Helper class to save/edit the user
    def editUserHelper(self,request, username, firstname, lastname, phone, email, role, users):
        user = EditUser.edit_user(request, username, firstname, lastname, phone, email, role)
        if user is None:
            return render(request, "configure_user.html",
                          {"roles": User.ROLE_CHOICES, "users": users,
                           "message": "Something went wrong when updating the user"})
        else:
            return render(request, "configure_user.html",
                          {"roles": User.ROLE_CHOICES, "users": users,
                           "message": "The user has been successfully updated"})

class UserDirectoryPage(View):
    def get(self, request):
        users = User.objects.all()
        courses = Course.objects.all()
        return render(request, "user_directory.html", {"users": users, "courses": courses})

    def post(self, request):
        return redirect('/home/')

class CourseDirectoryPage(View):
    def get(self, request):
        # Get the logged-in user
        user = GetUser.get_user(request)
        if user is None:
            return redirect('/')  # Redirect to login if no user session exists

        # Check for filtering in the query parameters
        filter_assigned = request.GET.get('filter') == 'assigned'

        # Default to all courses
        courses = Course.objects.all()

        # Apply filtering based on role
        if filter_assigned:
            if user.role == 'TA':
                # Get labs assigned to the TA and their parent courses
                labs = Section.objects.filter(ta=user)
                courses = Course.objects.filter(labs__in=labs).distinct()
            elif user.role == 'Instructor':
                # Get courses assigned to the instructor
                courses = user.courses.all()

        return render(request, "course_directory.html", {'courses': courses, 'user': user, 'filter_assigned': filter_assigned})

    def post(self, request):
        courses = Course.objects.all()
        return render(request, "course_directory.html", {'courses': courses})

class ProfilePage(View):
    def get(self, request):
        return render(request, "profile_page.html", {})

class HomePage(View):
    def get(self, request):
        return render(request, "home.html", {})

class AdminHomePage(View):
    def get(self, request):
        user = GetUser.get_user(request)
        can_access = CheckPermission.check_admin(user)
        if can_access:
            return render(request, "admin_home.html", {})
        else:
            return render(request, "home.html", {'message':"You cannot access this page."})

class ConfigureCoursePage(View):
    def get(self, request):
        #make this into a method
        courses = Course.objects.all()
        instructors = User.objects.filter(role="Instructor")
        tas = User.objects.filter(role="TA")
        sections = Section.objects.all()
        users = User.objects.all()
        return render(request, "configure_course.html", {"instructors": instructors, "tas": tas, "courses": courses, 'sections':sections, 'days': DAYS_OF_WEEK, 'users': users})

    def post(self, request):
        #this is to filter based on which form is being accessed
        form = request.POST.get('form_name')
        course_name = request.POST.get('name')
        course_id = request.POST.get('course_id')
        courses = Course.objects.all()
        #get the list of the instructors so that we can show it
        instructors = User.objects.filter(role="Instructor")
        tas = User.objects.filter(role="TA")
        sections = Section.objects.all()


        if form == "create_course":
            return self.add_course_helper(courses, instructors, tas, sections, request)
        elif form == "create_section":
            return self.add_section_helper(request, courses, instructors, tas, sections)
        elif form == "edit_course":
            return self.edit_course_helper(course_id, request)
        elif form == "edit_lab":
            return self.edit_lab_helper(None, tas, sections, instructors, courses, request)
        else:
            return render(request, "configure_course.html", {"instructors": instructors, "tas": tas,
                'courses':courses, 'message': "Something went wrong when fetching the form, please try again."})


    def add_course_helper(self, courses, instructors, tas, sections, request):
        # this gets the first and last name of the instructor as well as their role
        instructor_name = request.POST['instructor']

        # checks if the no instructor option was selected, course must be initialized with an instructor
        if instructor_name != "":
            # splits first and last name into 2 separate strings, also the role in () but that's not necessary here
            names = instructor_name.split(" ")
            instructor = User.objects.get(first_name=names[0], last_name=names[1])
        else:
            instructor = None

        # get the instructor by finding a user with the same first and last name
        # no need to filter role because the create_course method already does that
        cname = request.POST['course_name']

        #will return None if the creation failed, will return a course and save it to the database if it succeeded
        course = CreateCourse.create_course(cname, instructor)
        if course is None:
            return render(request, "configure_course.html", {"instructors": instructors, "tas": tas,
                'courses': courses, 'sections':sections, 'message': "Something went wrong when creating the course \"" + cname + "\""})
        else:
            return render(request, "configure_course.html", {"instructors": instructors, "tas": tas,
                'courses': courses, 'sections':sections, 'message': "The course \"" + cname + "\" has been created"})


    def add_section_helper(self, request, courses, instructors, tas, sections):
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
            return render(request, "configure_course.html", {'courses': courses, 'sections':sections,
                'tas':tas, 'instructors':instructors, 'message': "Something went wrong when creating the section \"" + section_name + "\""})
        else:
            return render(request, "configure_course.html", {'courses': courses, 'sections':sections,
                'tas':tas, 'instructors':instructors,'message': "The section \"" + section_name + "\" has been created"})

    def edit_course_helper(self, course_id,request):
        updated_course = EditCourse.edit_course(course_id, request)
        if updated_course:
            message = f"Course '{updated_course.name}' was updated successfully."
        else:
            message = "Failed to update course. Please check your inputs and try again."

        return redirect('configure_course')

    def edit_lab_helper(self,lab_id, tas, sections, instructors, courses, request):
        updated_lab = EditLab.edit_lab(lab_id, request)
        if updated_lab is not None:
            message = f"Lab '{updated_lab.name}' updated successfully."
        else:
            message = "Failed to update lab. Please check your inputs and try again."

        return render(request, "configure_course.html", {
            "instructors": instructors,
            "courses": courses,
            "tas": tas,
            "sections":sections,
            "message": message
        })
