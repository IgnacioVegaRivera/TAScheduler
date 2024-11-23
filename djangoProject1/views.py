from django.shortcuts import render, redirect
from django.views import View

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
        return render(request, "configureUser.html", {})

    def post(self, request):
        return redirect('/home/')

class UserDirectoryPage(View):
    def get(self, request):
        return render(request, "user_Directory.html", {})

    def post(self, request):
        return redirect('/home/')

class CourseDirectoryPage(View):
    def get(self, request):
        return render(request, "course_Directory.html", {})

    def post(self, request):
        return redirect('/home/')

class HomePage(View):
    def get(self, request):
        return render(request, "home.html", {})

class AdminHomePage(View):
    def get(self, request):
        return render(request, "admin_Home.html", {})