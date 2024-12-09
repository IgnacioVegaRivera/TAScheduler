from django.db import models
import uuid

# Predefined choices for days of the week
DAYS_OF_WEEK = [
    ('Monday', 'Monday'),
    ('Tuesday', 'Tuesday'),
    ('Wednesday', 'Wednesday'),
    ('Thursday', 'Thursday'),
    ('Friday', 'Friday'),
    ('Saturday', 'Saturday'),
    ('Sunday', 'Sunday'),
]

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
    phone_number = models.CharField(max_length=10, blank=True, null=True)  #optional phone number (can make required later)
    address = models.TextField(blank=True, null=True)  #optional home address (can make required later)
    skills = models.TextField(blank=True, null=True)  #apparently we need skills? okay here's an open text field for it
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='TA')  #role of the user (TA, Instructor, Admin)

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.get_role_display()})"

class Course(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False) #unique id
    name = models.CharField(max_length=100, default="Default Course Name") #course name
    users = models.ManyToManyField(User, limit_choices_to={'role__in': ['TA', 'Instructor']}, related_name='courses', blank=True)
    # only instructors and TAs can be assigned to a course

    def __str__(self):
        return self.name

class Section(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False) #unique id
    name = models.CharField(max_length=100, default="Default Section Name") #section name
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='sections') #link to course
    day = models.CharField(max_length=20, choices=DAYS_OF_WEEK, blank=True, null=True)  #day of the week
    time = models.TimeField(blank=True, null=True)  #specific time of day
    location = models.CharField(max_length=100, blank=True, null=True) #location
    user = models.ForeignKey(User, null=True, blank=True, limit_choices_to={'role__in': ['TA', 'Instructor']}, on_delete=models.SET_NULL, related_name='sections')
    # only TAs and Instructors can be added to a section
    # one ta/instructor per section
    # ONLY USERS IN course.users WILL BE CORRECTLY SAVED TO THE SECTION
    # # Only when using the save() method, which does NOT get called when directly editing the database. It IS called when using forms

    def __str__(self):
        return f"{self.name} ({self.course.name})"

    def save(self, *args, **kwargs):
        # ensure users in a section are part of the course's users.
        # if not, remove the user (set to None).
        if self.user and self.user not in self.course.users.all():
            self.user = None  # remove the invalid user assignment
        super().save(*args, **kwargs)