class SubjectService:
    @staticmethod
    def get_teacher_subjects(teacher_user):
        from .models import Subject
        return Subject.objects.filter(assigned_teacher=teacher_user)
