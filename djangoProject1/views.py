from django.shortcuts import render, redirect
from django.views import View



class LoginPage(View):
    def get(self, request):
        return render(request, "login.html", {})


class ConfigureUserPage(View):
    def get(self, request):
        return render(request, "configureUser.html", {})

    def post(self, request):
        return redirect('/home/')

class HomePage(View):
    def get(self, request):
        return render(request, "home.html", {})

class AdminHomePage(View):
        def get(self, request):
            return render(request, "admin_Home.html", {})