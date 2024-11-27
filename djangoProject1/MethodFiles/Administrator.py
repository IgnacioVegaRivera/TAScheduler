# file for Admin methods
from djangoProject1.MethodFiles.Interfaces import CreateCourseInterface, CreateLabInterface, CheckPermissionInterface, EditUserInterface, CreateUserInterface

from djangoProject1.models import Course, User

class CreateUser(CreateUserInterface):
    @staticmethod
    def create_user(user_name, user_email, user_password, user_first_name, user_last_name, user_phone_number, user_address, user_role):
        if User.objects.filter(username=user_name).exists():
            return None

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

class CheckPermission(CheckPermissionInterface):
    @staticmethod
    def check_admin(user):
        pass

    @staticmethod
    def check_instructor(self, user):
        pass

class EditUser(EditUserInterface):
    @staticmethod
    def edit_user(self, user):
        pass