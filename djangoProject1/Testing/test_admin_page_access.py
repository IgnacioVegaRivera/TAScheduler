from django.shortcuts import render, redirect
from django.views import View

from djangoProject1.MethodFiles.Administrator import CheckPermission
from djangoProject1.models import User