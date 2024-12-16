# file for Admin methods
from abc import ABC
from datetime import time

# import re is used for checking the length of the phone number field
import re

# from django.template.context_processors import static

from djangoProject1.MethodFiles.Interfaces import CreateCourseInterface, CreateSectionInterface, EditUserInterface, \
    CreateUserInterface, EditCourseInterface, EditSectionInterface, RemoveUserInterface

from djangoProject1.models import Course, User, Section, DAYS_OF_WEEK


class CreateUser(CreateUserInterface):
    @staticmethod
    def create_user(user_name, user_email, user_password, user_first_name, user_last_name, user_phone_number,
                    user_address, user_role, user_skills):
        # Check if the username already exists and if it is valid
        if User.objects.filter(username=user_name).exists() or user_name == '' or not isinstance(user_name, str):
            return None

        # check for valid role
        valid_role = False
        for role in User.ROLE_CHOICES:
            if role[0] == user_role or role[1] == user_role:
                valid_role = True

        if not valid_role:
            return None

        # First name should only have alphabetical characters
        if not isinstance(user_first_name, str):
            return None

        if not user_first_name.isalpha() or user_first_name == '':
            return None

        # Last name should only have alphabetical characters
        if not isinstance(user_last_name, str):
            return None

        if not user_last_name.isalpha() or user_last_name == '':
            return None

        # Phone can only have digits and must be 10 digits
        if not isinstance(user_phone_number, str):
            return None

        if len(user_phone_number) != 10 and user_phone_number != "":
            return None

        # Address must have a street and house number if it is filled out
        if not isinstance(user_address, str):
            return None

        if user_address != "":
            digit = character = False
            for char in user_address:
                if char.isdigit():
                    digit = True
                if char.isalpha():
                    character = True
                if digit and character:
                    break
            if not digit or not character:
                return None


        # email cannot be empty
        if user_email == '' or not isinstance(user_email, str):
            return None

        # password should not be empty
        if user_password == '' or not isinstance(user_password, str):
            return None

        #skills is an optional field, all we need to check is if it is a string
        if not isinstance(user_skills, str):
            return None

        #if everything is all good we can then we can create the user and save it
        user = User(username=user_name, email=user_email, password=user_password,
                    first_name=user_first_name, last_name=user_last_name, phone_number=user_phone_number,
                    address=user_address, role=user_role, skills=user_skills)
        user.save()
        return user


class CreateCourse(CreateCourseInterface):
    @staticmethod
    def create_course(name, instructors, tas):
        if not isinstance(name, str) or not name.strip():
            return None

        # if any of the inputs are none then return None
        if name == None or name == "":
            return None

        # checks whether the instructors input is a list type, and also checks whether all the elements in the
        # instructors list are User objects
        if not isinstance(instructors, list) or not all(isinstance(instructor, User) for instructor in instructors):
            return None

        # checks whether the tas input is a list type, and also checks whether all the elements in the
        # tas list are User objects
        if not isinstance(tas, list) or not all(isinstance(ta, User) for ta in tas):
            return None

        # if the course already exists then return None
        if Course.objects.filter(name=name).exists():
            return None

        # if everything is fine then we can create the course no problem
        course = Course(name=name)
        course.save()

        course.users.add(*instructors)
        course.users.add(*tas)

        return course

class CreateSection(CreateSectionInterface):

    # this is a helper for creating sections, it's to clean up the create_section code
    @staticmethod
    def verify_fields(section_name, course, user, days, scheduled_time, location):
        # check each parameter is the correct type
        if not isinstance(user, User) and user is not None:
            return False

        # check if the user exists they are of the right role
        if user is not None:
            user_courses = Course.objects.filter(users=user)
            if course not in user_courses:
                return False
            if "Lecture" not in section_name:
                if user.role == "Instructor":
                    return False
            else:
                if user.role == "TA":
                    return False

        # check that the days are formatted properly
        if not isinstance(days, list):
            return False

        for day in days:
            found = False
            for i in range(7):
                if day == DAYS_OF_WEEK[i][0]:
                    found = True
                    break

            if not found:
                return False

        # check that the time is formatted properly
        if not isinstance(scheduled_time, time) and scheduled_time is not None:
            return False

        if not isinstance(location, str):
            return False

        # requires a building and a room number if a location is provided
        if location != "":
            digit = character = False
            for char in location:
                if char.isdigit():
                    digit = True
                if char.isalpha():
                    character = True
                if digit and character:
                    break

            if not digit or not character:
                return False

        # create the object
        return True

    # need to update this eventually to reflect the changes from labs to sections, old implementation commented out
    @staticmethod
    def create_section(section_name, course, user, days, scheduled_time, location):
        # every section needs a course
        if course == None or not isinstance(course, Course):
            return None

        # determine the kind of section that is being created, also checks that only 1 of the 3 keywords is in the name
        if not isinstance(section_name, str):
            return None

        if "Lab" not in section_name and "Discussion" not in section_name and "Lecture" not in section_name:
            return None

        if "Lab" in section_name:
            # if either of the other 2 identifiers is in the name then invalid name
            if "Discussion" in section_name or "Lecture" in section_name:
                return None

        elif "Discussion" in section_name:
            # if lecture is in the name then invalid name
            if "Lecture" in section_name:
                return None

        valid = CreateSection.verify_fields(section_name, course, user, days, scheduled_time, location)
        if valid and not Section.objects.filter(name=section_name, course=course).exists():
            section = Section(name=section_name, course=course, user=user, days=days, time=scheduled_time,
                              location=location)
            section.save()
            return section
        else:
            return None


class EditUser(EditUserInterface, ABC):
    @staticmethod
    def edit_user(request, username, newFirstname, newLastname, newPhone, newEmail, newRole, newAddress, newSkills):
        #get the user that we want to change
        user = User.objects.get(username=username)

        if user is None or not isinstance(user, User):
            return None

        # check for first name
        if not isinstance(newFirstname, str) or not newFirstname.strip() or newFirstname == "" or not newFirstname.isalpha():
            return None

        # check for last name
        if not isinstance(newLastname, str) or not newLastname.strip() or newLastname == "" or not newLastname.isalpha():
            return None

        # check for email
        if not isinstance(newEmail, str) or not len(newEmail) > 0:
            return None

        if newEmail.find('@') == -1 or newEmail.find('.') == -1:
            return None

        # check for phone number
        if not isinstance(newPhone, str):
            return None

        if len(newPhone) != 10 and newPhone != "":
            return None

        if len(newPhone) == 10:
            for char in newPhone:
                if not char.isdigit():
                    return None

        valid_roles = {"TA", "Instructor", "Admin"}  # Add other valid roles as needed
        if not isinstance(user, User) or not isinstance(newRole, str) or newRole not in valid_roles:
            return None


        #checks for address
        if not isinstance(newAddress, str):
            return None

        #address must have a street number and street name
        if newAddress != "":
            digit = character = False
            for char in newAddress:
                if char.isdigit():
                    digit = True
                if char.isalpha():
                    character = True
                if digit and character:
                    break
            if not digit or not character:
                return None

        #check for skills
        if not isinstance(newSkills, str):
            return None

        # make sure to check last in case any other field messes up, then we don't want to make changes to
        # the courses and sections because they shouldn't change if we don't update the user

        # if the user is an admin then they shouldn't have any courses or sections,
        if newRole == "Admin" and user.role != "Admin":
            removeCourses = Course.objects.filter(users=user)
            removeSections = Section.objects.filter(user=user)
            for course in removeCourses:
                course.users.remove(user)

            for lab in removeSections:
                lab.user = None
                lab.save()

        # if the user becomes an Instructor then they shouldnt have any labs or discussions
        if newRole == "Instructor" and user.role != "Instructor":
            removeLabAndDiscussion = Section.objects.filter(user=user)
            for lab in removeLabAndDiscussion:
                lab.user = None
                lab.save()

        # if the user becomes a TA then they shouldnt have any lectures
        if newRole == "TA" and user.role != "TA":
            removeLectures = Section.objects.filter(user=user)
            for lecture in removeLectures:
                lecture.user = None

        # changes all of the necessary values to their new ones
        user.first_name = request.POST.get('first_name', user.first_name)
        user.last_name = request.POST.get("last_name", user.last_name)
        user.role = request.POST.get("role", user.role)
        user.email = request.POST.get("email", user.email)
        user.phone_number = request.POST.get("phone_number", user.phone_number)
        user.address = request.POST.get("address", user.address)
        user.skills = request.POST.get("skills", user.skills)

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
        course.users.set(instructors)

        course.save()
        return course


class EditSection(EditSectionInterface):
    @staticmethod
    def edit_section(request, section_id, name, course, user, days, the_time, location):
        section = Section.objects.get(id=section_id)
        # every section needs a course
        if course == None or not isinstance(course, Course):
            return None

        # determine the kind of section that is being created, also checks that only 1 of the 3 keywords is in the name
        if not isinstance(name, str):
            return None

        if "Lab" not in name and "Discussion" not in name and "Lecture" not in name:
            return None

        if "Lab" in name:
            # if either of the other 2 identifiers is in the name then invalid name
            if "Discussion" in name or "Lecture" in name:
                return None

        elif "Discussion" in name:
            # if lecture is in the name then invalid name
            if "Lecture" in name:
                return None

        valid = CreateSection.verify_fields(name, course, user, days, the_time, location)

        # check if there already exists a section in the database with the same name and course, then check if it's
        # a different course than the one we are currently editing
        different = False
        if Section.objects.filter(name=name, course=course).exists():
            if Section.objects.get(name=name, course=course).id != section.id:
                different = True

        if valid and not different:
            section.name = name
            section.course = course
            section.user = user
            section.days = days
            section.time = the_time
            section.location = location
            section.save()
            return section
        else:
            return None


class RemoveUser(RemoveUserInterface):
    @staticmethod
    def remove_user(user_id):
        user = User.objects.filter(id=user_id).first()

        if user:
            user.delete()
            return "The user has been successfully removed"
        elif not user:
            return "User does not exist"
