import abc

class CreateCourseInterface(abc.ABC):
    @abc.abstractmethod
    def create_course(self, name, instructors, tas):
        pass

class CreateSectionInterface(abc.ABC):
    @abc.abstractmethod

    def create_section(self, section_name, course, user, days, time, location):
        pass

class CheckPermissionInterface(abc.ABC):
    @abc.abstractmethod
    def check_admin(self, user):
        pass

    @abc.abstractmethod
    def check_instructor(self, user):
        pass


class EditUserInterface(abc.ABC):
    @abc.abstractmethod
    def edit_user(self, username, newFirstname, newLastname, newPhone, newEmail, newRole, newAddress, newSkills):
        pass

class EditCourseInterface(abc.ABC):
    @abc.abstractmethod
    def edit_course(self, course, newCourseName, users):
        pass

class EditSectionInterface(abc.ABC):
    @abc.abstractmethod
    def edit_section(self, request, section_id, name, course, user, days, the_time, location):
        pass

class CreateUserInterface(abc.ABC):
    @abc.abstractmethod
    def create_user(self, user_name, user_email, user_password, user_first_name, user_last_name, user_phone_number, user_address, user_role, user_skills):
      pass

class GetUserInterface(abc.ABC):
    @abc.abstractmethod
    def get_user(self, request):
        pass

class RemoveUserInterface(abc.ABC):
    @abc.abstractmethod
    def remove_user(self,user_id):
        pass

class EditPersonalUserInterface(abc.ABC):
    @abc.abstractmethod
    def edit_personal_user(self, request, newUsername, newPassword, newFirstname, newLastname,
                           newPhone, newEmail, newAddress, newSkills):
        pass

class AssignUserInterface(abc.ABC):
    @abc.abstractmethod
    def assign_user(self, section_id, user, request):
        pass