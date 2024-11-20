from django.shortcuts import render
from django.views import View


class LoginPage(View):
    def get(self, request):
        return render(request, "login.html", {})


class ConfigureUserPage(View):
    def get(self, request):
        return render(request, "configureUser.html", {})

class HomePage(View):
    def get(self, request):
        return render(request, "home.html", {})