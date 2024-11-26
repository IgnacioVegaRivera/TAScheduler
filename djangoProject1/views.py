from django.shortcuts import render, redirect
from django.views import View

from djangoProject1.MethodFiles.Administrator import CreateCourse
from djangoProject1.models import User, Course, Lab

#this is for when we log in we have the current user
curUser = None

class LoginPage(View):
    def get(self, request):
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
                #in all the other pages using this: user = User.objects.filter(username=request.session['cur_user_name'])
                request.session['cur_user_name'] = user[0].username
                return redirect("home.html")
            else:
                message = "Username or Password is incorrect"
                return render(request, "login.html", {'message': message})

        #If we have an invalid username then print this message on the login page
        else:
            message = "User does not exist"
            return render(request, "login.html", {'message': message})



class ConfigureUserPage(View):
    def get(self, request):
        users = User.objects.all()
        return render(request, "configureUser.html", {"roles": User.ROLE_CHOICES, "users": users})

    def post(self, request):
        #Get the required fields for creating a user
        firstname = request.POST['first_name']
        lastname = request.POST['last_name']
        username = request.POST['username']
        password=request.POST['password']
        #course= request.POST['name']
        email = request.POST['email']
        phone = request.POST['phone_number']
        address = request.POST['address']
        role = request.POST['role']
        #course_name = request.POST['name']

        #Create users:
        User.objects.create(first_name=firstname, last_name=lastname, username=username,
                                    password=password, email=email, phone_number=phone, address=address, role=role)

        #Display users list:
        users = User.objects.filter(first_name=firstname, last_name=lastname, role=role,
                                    email=email, phone_number=phone)
        users_info = []
        for user in users:
            users_info.append({
                "firstname": user.first_name,
                "lastname": user.last_name,
                "role": user.role,
                "email": user.email,
                "phone_number": user.phone_number,
            })

        return render(request, "configureUser.html", {"roles": User.ROLE_CHOICES, "users": users_info})

class UserDirectoryPage(View):
    def get(self, request):
        users = User.objects.all()
        courses = Course.objects.all()
        return render(request, "user_Directory.html", {"users": users, "courses": courses})

    def post(self, request):
        return redirect('/home/')

class CourseDirectoryPage(View):
    def get(self, request):
        courses = Course.objects.all()
        return render(request, "course_Directory.html", {'courses': courses})

    def post(self, request):
        return redirect('/home/')

class HomePage(View):
    def get(self, request):
        return render(request, "home.html", {})

class AdminHomePage(View):
    def get(self, request):
        return render(request, "admin_Home.html", {})

class ConfigureCoursePage(View):
    def get(self, request):
        #make this into a method
        courses = Course.objects.all()
        instructors = User.objects.filter(role="Instructor")
        return render(request, "configureCourse.html", {"instructors": instructors, "courses": courses})

    def post(self, request):
        #this is to filter based on which form is being accessed
        form = request.POST.get('form_name')

        #get the list of the instructors so that we can show it
        instructors = User.objects.filter(role="Instructor")

        if form == "create_course":
            # this gets the first and last name of the instructor as well as their role
            instructor_name = request.POST['instructor']

            #checks if the no instructor option was selected, course must be initialized with an instructor
            if instructor_name != "":
                # splits first and last into 2 separate strings
                names = instructor_name.split(" ")
                instructor = User.objects.get(first_name=names[0], last_name=names[1])
            else:
                instructor = None

            #get the instructor by finding a user with the same first and last name
            #no need to filter role because the create_course method already does that
            cname = request.POST['course_name']

            course = CreateCourse.create_course(cname, instructor)
            if course is None:
                return render(request, "configureCourse.html",
        {"instructors": instructors, 'message': "Something went wrong when creating the course \"" + cname + "\""})
            else:
                return render(request, "configureCourse.html",
        {"instructors": instructors, 'message': "The course \"" + cname +"\" has been created"})

        else:
            return render(request, "configureCourse.html",
        {"instructors": instructors, 'message': "Something went wrong when fetching the form, please try again."})
