from djangoProject1.MethodFiles.Interfaces import CheckPermissionInterface, GetUserInterface
from djangoProject1.models import User


class CheckPermission(CheckPermissionInterface):
    @staticmethod
    def check_admin(user):
        if isinstance(user, User):
            if user.role == 'Admin':
                return True
            else:
                return False
        else:
            return False

    @staticmethod
    def check_instructor(user):
        pass

class GetUser(GetUserInterface):
    @staticmethod
    def get_user(request):
        name = request.session.get('cur_user_name')
        if not name:
            return None
        else:
            return User.objects.filter(username=name).first()