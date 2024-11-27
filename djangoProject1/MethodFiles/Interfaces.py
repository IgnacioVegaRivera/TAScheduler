import abc

class CreateCourseInterface(abc.ABC):
    @abc.abstractmethod
    def create_course(self, name, instructor):
        pass

class CreateLabInterface(abc.ABC):
    @abc.abstractmethod
    def create_lab(self, lab_name, course_name, ta):
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
    def edit_user(self, user):
        pass

class CreateUserInterface(abc.ABC):
    @abc.abstractmethod
    def create_user(self, user_name, user_email, user_password, user_first_name, user_last_name, user_phone_number, user_address, user_role):
      pass