"""
URL configuration for djangoProject1 project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from djangoProject1.views import LoginPage, HomePage, AdminHomePage, ConfigureUserPage, UserDirectoryPage, \
    CourseDirectoryPage, ConfigureCoursePage, ProfilePage

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', LoginPage.as_view()),
    path('home.html',HomePage.as_view()),
    path('user_directory.html', UserDirectoryPage.as_view()),

    path('course_directory.html', CourseDirectoryPage.as_view()),

    path('profile_page.html', ProfilePage.as_view(), name='profile_page'),
    path('configure_user.html', ConfigureUserPage.as_view(), name='configure_user'),
    path('configure_course.html', ConfigureCoursePage.as_view(), name='configure_course'),
    path('admin_home.html', AdminHomePage.as_view())

]
