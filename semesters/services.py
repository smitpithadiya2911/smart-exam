class SemesterService:
    @staticmethod
    def get_semesters_for_course(course_id):
        from .models import Semester
        return Semester.objects.filter(course_id=course_id, is_active=True)
