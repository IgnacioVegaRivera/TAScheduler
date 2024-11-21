from django.db import models


class User(models.Model): # basic for now
    name = models.CharField(max_length=100)
