from django.shortcuts import render, redirect
from django.views import View

from djangoProject1.MethodFiles.Administrator import CreateLab
from djangoProject1.models import User, Course, Lab