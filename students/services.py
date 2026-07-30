class StudentService:
    @staticmethod
    def get_student_count():
        from .models import StudentProfile
        return StudentProfile.objects.count()
