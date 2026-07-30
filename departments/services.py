class DepartmentService:
    @staticmethod
    def get_all_departments():
        from .models import Department
        return Department.objects.all()
