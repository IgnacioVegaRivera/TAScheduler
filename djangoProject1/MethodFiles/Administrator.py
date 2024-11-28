# file for Admin methods
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
import re
from djangoProject1.MethodFiles.Interfaces import CreateCourseInterface, CreateLabInterface,EditUserInterface, CreateUserInterface

from djangoProject1.models import Course, User

class CreateUser(CreateUserInterface):
    @staticmethod
    def create_user(user_name, user_email, user_password, user_first_name, user_last_name, user_phone_number, user_address, user_role):
        #Check if the username already exists
        if User.objects.filter(username=user_name).exists():
            raise ValueError("User with that name already exists")

        #Validation of user_email
        try:
            validate_email(user_email)
        except ValidationError:
            raise ValueError("Invalid email address")

        #Username should only have alphabetical characters
        if not user_first_name.isalpha():
            raise ValueError("First name must contain only alphabetical characters")

        if not user_last_name.isalpha():
            raise ValueError("Last name must contain only alphabetical characters")

        if not re.match(r'^\d{10,15}$', user_phone_number):
            raise ValueError("Phone number must contain only digits and must be between 10 to 15 digits")

        if not user_address:
            raise ValueError("Address cannot be empty")


        user = User(username=user_name, email=user_email, password=user_password,
                    first_name=user_first_name, last_name=user_last_name, phone_number=user_phone_number,
                    address=user_address, role=user_role)
        user.save()
        return user
class CreateCourse(CreateCourseInterface):
    @staticmethod
    def create_course(name, instructor):
        #if name or instructor are the wrong type return None
        if not isinstance(instructor, User) or not isinstance(name, str):
            return None

        #if any of the inputs are none then return None
        if name == None or name == "" or instructor == None:
            return None

        #if the role isn't instructor then we can't assign to a course so we return None
        if instructor.role != "Instructor":
            return None

        #if the course already exists then return None
        if Course.objects.filter(name=name).exists():
            return None


        #if everything is fine then we can create the course no problem
        course = Course(name=name)
        course.save()
        course.instructors.add(instructor)

        return course

class CreateLab(CreateLabInterface):
    @staticmethod
    def create_lab(name, instructor):
        pass

class EditUser(EditUserInterface):
    @staticmethod
    def edit_user(self, user):
        pass