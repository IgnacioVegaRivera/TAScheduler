import abc

class CreateCourseInterface(abc.ABC):
    @abc.abstractmethod
    def create_course(self, name, instructor):
        pass

class CreateLabInterface(abc.ABC):
    @abc.abstractmethod
    def create_lab(self, lab_name, course, ta):
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
    def edit_first_name(self, user, firstname):
        pass

    @abc.abstractmethod
    def edit_last_name(self, user, lastname):
        pass

    @abc.abstractmethod
    def edit_username(self, user, username):
        pass

    @abc.abstractmethod
    def edit_password(self, user, password):
        pass

    @abc.abstractmethod
    def edit_email(self, user, email):
        pass

    @abc.abstractmethod
    def edit_phone(self, user, phone):
        pass

    @abc.abstractmethod
    def edit_address(self, user, address):
        pass

    @abc.abstractmethod
    def edit_role(self, user, role):
        pass

class EditCourseInterface(abc.ABC):
    @abc.abstractmethod
    def edit_course(self, course):
        pass

class CreateUserInterface(abc.ABC):
    @abc.abstractmethod
    def create_user(self, user_name, user_email, user_password, user_first_name, user_last_name, user_phone_number, user_address, user_role):
      pass

class GetUserInterface(abc.ABC):
    @abc.abstractmethod
    def get_user(self, request):
        pass