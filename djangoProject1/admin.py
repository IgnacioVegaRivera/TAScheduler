from django.contrib import admin

from djangoProject1.models import User
from djangoProject1.models import Course
from djangoProject1.models import Lab

admin.site.register(User)
admin.site.register(Course)
admin.site.register(Lab)