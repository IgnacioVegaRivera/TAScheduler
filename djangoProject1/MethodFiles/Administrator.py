# file for Admin methods
from djangoProject1.MethodFiles.Interfaces import CreateCourseInterface, CreateLabInterface,EditUserInterface, CreateUserInterface

from djangoProject1.models import Course, User, Lab


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
    def create_lab(lab_name, course, ta):
        if not isinstance(ta, User) or not isinstance(lab_name, str) or not isinstance(course, Course):
            return None

        # if any of the inputs are none then return None
        if lab_name == None or lab_name == "" or ta == None or course == None or course.instructors.first() == None:
            return None

        # if the role isn't TA then we can't assign to a lab so we return None
        if ta.role != "TA":
            return None

        # if a lab of the same name already exists then return None
        if Lab.objects.filter(name=lab_name).exists():
            return None

        # if everything is fine then we can create the lab no problem
        lab = Lab(name=lab_name, course=course, ta=ta)
        lab.save()

        return lab

class EditUser(EditUserInterface):
    @staticmethod
    def edit_user(self, user):
        pass