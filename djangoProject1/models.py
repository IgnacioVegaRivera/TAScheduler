from django.db import models
import uuid

class User(models.Model): # basic for now
    ROLE_CHOICES = [
        ('TA', 'Teaching Assistant'),
        ('Instructor', 'Instructor'),
        ('Admin', 'Administrator'),
    ]


    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False) #unique id
    first_name = models.CharField(max_length=50, default="DefaultFirst") #first name of user
    last_name = models.CharField(max_length=50, default="DefaultLast") #last name of user
    username = models.CharField(max_length=50, unique=True, default="Default_Username")  #unique username (ISSUES LATER ON, default AND unique doesn't work well)
    password = models.CharField(max_length=128, default="Default_Password")  #stored password (128 for hash(? idk documentation recommended it))
    email = models.EmailField(default="default@example.com")  #unique email address (cant run unless blank by default
    phone_number = models.CharField(max_length=20, blank=True, null=True)  #optional phone number (can make required later)
    address = models.TextField(blank=True, null=True)  #optional home address (can make required later)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='TA')  #role of the user (TA, Instructor, Admin)

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.get_role_display()})"

class Course(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False) #unique id
    name = models.CharField(max_length=100, default="Default Course Name") #course name
    instructors = models.ManyToManyField(User, limit_choices_to={'role': 'Instructor'}, related_name='courses', blank=True)
    #only instructors can be a part of a course
    #can access courses via 'courses'

    def __str__(self):
        return self.name

class Lab(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False) #unique id
    name = models.CharField(max_length=100, default="Default Lab Name") #lab name
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='labs')  #link to the course, ForeignKey is basically one-to-many relationship
    ta = models.ForeignKey(User, null=True, blank=True, limit_choices_to={'role': 'TA'}, on_delete=models.SET_NULL, related_name='labs')
    #foreign keys are kinda weird, must specifically declare that a TA isn't required when making a lab (makes it easier to instantiate a lab for now)

    def __str__(self):
        return f"{self.name} ({self.course.name})"