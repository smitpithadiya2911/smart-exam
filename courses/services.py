class CourseService:
    @staticmethod
    def get_courses_by_department(dept_id):
        from .models import Course
        return Course.objects.filter(department_id=dept_id)
