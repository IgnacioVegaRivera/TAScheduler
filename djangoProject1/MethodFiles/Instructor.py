from djangoProject1.MethodFiles.Interfaces import AssignUserInterface
from djangoProject1.models import User, Course, Section

class AssignUser(AssignUserInterface):
    @staticmethod
    def assign_user(section, user, course):
        #check if user exists
        if user is not None:
            user_courses = Course.objects.filter(users=user)
            if course not in user_courses:
                return "Failed to update the section assignment"
            if "Lecture" not in section.name:
                if user.role == "Instructor":
                    return "Failed to update the section assignment"
            else:
                if user.role == "TA":
                    return "Failed to update the section assignment"

        section.user = user
        section.save()
        return "Section assignment was successfully updated"