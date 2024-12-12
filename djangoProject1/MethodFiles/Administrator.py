# file for Admin methods
from abc import ABC

from django.core.exceptions import ValidationError
from django.core.validators import validate_email
import re

from django.template.context_processors import static

from djangoProject1.MethodFiles.Interfaces import CreateCourseInterface, CreateSectionInterface, EditUserInterface, \
    CreateUserInterface, EditCourseInterface, EditLabInterface, RemoveUserInterface

from djangoProject1.models import Course, User, Section


class CreateUser(CreateUserInterface):
    @staticmethod
    def create_user(user_name, user_email, user_password, user_first_name, user_last_name, user_phone_number,
                    user_address, user_role):
        # Check if the username already exists and if it is valid
        if User.objects.filter(username=user_name).exists() or user_name == '':
            return None

        # check for valid role
        valid_role = False
        for role in User.ROLE_CHOICES:
            if role[0] == user_role or role[1] == user_role:
                valid_role = True

        if not valid_role:
            return None

        # First name should only have alphabetical characters
        if not user_first_name.isalpha() or user_first_name == '':
            return None

        # Last name should only have alphabetical characters
        if not user_last_name.isalpha() or user_last_name == '':
            return None

        # Phone can only have digits and must be between 10 and 15 digits
        if not re.match(r'^\d{10}$', user_phone_number):
            return None

        # Address cannot be empty
        if not user_address:
            return None

        # email cannot be empty
        if user_email == '':
            return None

        # password should not be empty
        if user_password == '':
            return None

        user = User(username=user_name, email=user_email, password=user_password,
                    first_name=user_first_name, last_name=user_last_name, phone_number=user_phone_number,
                    address=user_address, role=user_role)
        user.save()
        return user


class CreateCourse(CreateCourseInterface):
    @staticmethod
    def create_course(name, instructor):
        # if name or instructor are the wrong type return None
        if not isinstance(instructor, User) or not isinstance(name, str):
            return None

        # if any of the inputs are none then return None
        if name == None or name == "" or instructor == None:
            return None

        # if the role isn't instructor then we can't assign to a course so we return None
        if instructor.role != "Instructor":
            return None

        # if the course already exists then return None
        if Course.objects.filter(name=name).exists():
            return None

        # if everything is fine then we can create the course no problem
        course = Course(name=name)
        course.save()
        course.instructors.add(instructor)

        return course


class CreateSection(CreateSectionInterface):

    # need to update this eventually to reflect the changes from labs to sections, old implementation commented out
    @staticmethod
    def create_section(request, section_name, course, user, day, time, location):
        # if not isinstance(ta, User) or not isinstance(lab_name, str) or not isinstance(course, Course):
        #     return None
        #
        # # if any of the inputs are none then return None
        # if lab_name == None or lab_name == "" or ta == None or course == None or course.instructors.first() == None:
        #     return None
        #
        # # if the role isn't TA then we can't assign to a lab so we return None
        # if ta.role != "TA":
        #     return None
        #
        # # if a lab of the same name already exists then return None
        # if Lab.objects.filter(name=lab_name).exists():
        #     return None
        #
        # # if everything is fine then we can create the lab no problem
        # lab = Lab(name=lab_name, course=course, ta=ta)
        # lab.save()
        #
        # return lab
        return None


class EditUser(EditUserInterface, ABC):
    @staticmethod
    def edit_user(request, username, newFirstname, newLastname, newPhone, newEmail, newRole):
        user = User.objects.get(username=username)

        # check for first name
        if (not isinstance(user, User) or not isinstance(newFirstname, str) or
                not newFirstname.strip() or newFirstname == "" or not newFirstname.isalpha()):
            return None

        # check for last name
        if (not isinstance(user, User) or not isinstance(newLastname, str)
                or not newLastname.strip() or newLastname == "" or not newLastname.isalpha()):
            return None

        # check for email
        if (not isinstance(user, User) or not isinstance(newEmail, str) or not len(newEmail) > 0
                or newEmail.find('@') == -1 or newEmail.find('.') == -1):
            return None

        # check for phone number
        if not isinstance(user, User) or not isinstance(newPhone, str) or not newPhone.isdigit() or len(newPhone) != 10:
            return None

        valid_roles = {"TA", "Instructor", "Admin"}  # Add other valid roles as needed
        if not isinstance(user, User) or not isinstance(newRole, str) or newRole not in valid_roles:
            return None

        # if the user is an admin then they shouldn't have any courses or labs
        if newRole == "Admin":
            removeInstructor = Course.objects.filter(instructors=user)
            removeTa = Lab.objects.filter(ta=user)
            for course in removeInstructor:
                course.instructors.remove(user)

            for lab in removeTa:
                lab.ta = None
                lab.save()

        # if the user is an Instructor then they shouldnt have any labs
        if newRole == "Instructor":
            removeTa = Lab.objects.filter(ta=user)
            for lab in removeTa:
                lab.ta = None
                lab.save()

        # if the user is an Instructor then they shouldnt have any courses
        if newRole == "TA":
            removeInstructor = Course.objects.filter(instructors=user)
            for course in removeInstructor:
                course.instructors.remove(user)

        # changes all of the necessary values to their new ones
        user.first_name = request.POST.get('first_name', user.first_name)
        user.last_name = request.POST.get("last_name", user.last_name)
        user.role = request.POST.get("role", user.role)
        user.email = request.POST.get("email", user.email)
        user.phone_number = request.POST.get("phone_number", user.phone_number)

        # Saves user
        user.save()
        user.refresh_from_db()
        return user


class EditCourse(EditCourseInterface):
    @staticmethod
    def edit_course(course_id, request):
        course = Course.objects.get(id=course_id)
        if course_id == None or course_id == "":
            return None

        new_course = request.POST.get("name", course.name)
        if new_course:
            course.name = new_course

        selected_instructors = request.POST.getlist("instructor[]")
        instructors = User.objects.filter(id__in=selected_instructors)
        course.instructors.set(instructors)

        course.save()
        return course


class EditLab(EditLabInterface):
    @staticmethod
    def edit_lab(lab_id, request):
        lab = Lab.objects.get(id=lab_id)
        if lab_id == None or lab_id == "":
            return None

        # Update Lab name
        lab.name = request.POST.get("lab", lab.name)
        if lab.name == None or lab.name == "":
            return None
        lab.save()

        # Update TAs
        selected_ta = request.POST.get("ta")
        if selected_ta:
            ta = User.objects.filter(id=selected_ta, role="TA").first()
            lab.ta = ta
        else:
            lab.ta = None

        # Update Courses, (be able to change  what course that lab is assigned
        selected_course_id = request.POST.get("course")
        if selected_course_id:
            course = Course.objects.filter(id=selected_course_id).first()
            lab.course = course
        else:
            lab.course = None

        lab.save()
        return lab

class RemoveUser(RemoveUserInterface):
    @staticmethod
    def remove_user(user_id, request):
        pass