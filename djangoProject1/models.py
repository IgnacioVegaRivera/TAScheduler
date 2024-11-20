from django.db import models


class User(models.Model): # basic for now
    name = models.CharField(max_length=50)
    # email = models.CharField(max_length=100)
    # phoneNumber = models.CharField(max_length=100)
    # userName = models.CharField(max_length=100)
    # passWord = models.CharField(max_length=100)
    # address = models.CharField(max_length=100)

    def __str__(self):
        return self.name

