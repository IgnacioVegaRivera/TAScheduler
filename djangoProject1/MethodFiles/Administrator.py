# file for Admin methods
from djangoProject1.MethodFiles.Interfaces import CreateCourseInterface
from djangoProject1.models import Course, User

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

