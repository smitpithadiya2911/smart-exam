class TeacherService:
    @staticmethod
    def get_teacher_count():
        from .models import TeacherProfile
        return TeacherProfile.objects.count()
