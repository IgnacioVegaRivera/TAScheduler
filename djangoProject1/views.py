from django.shortcuts import render, redirect
from django.views import View



class LoginPage(View):
    def get(self, request):
        return render(request, "login.html", {})

    def post(self, request):
        return redirect("home.html")


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