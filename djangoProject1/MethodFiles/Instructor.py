from djangoProject1.MethodFiles.Interfaces import AssignUserInterface
from djangoProject1.models import User, Course, Section

class AssignUser(AssignUserInterface):
    @staticmethod
    def assign_user(section_id, user, request):
        pass