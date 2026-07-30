from django.test import TestCase
from .models import Department

class DepartmentModelTest(TestCase):
    def test_department_creation(self):
        dept = Department.objects.create(name='Bachelor of Computer Applications', code='BCA', description='BCA Department')
        self.assertEqual(dept.code, 'BCA')
        self.assertEqual(str(dept), 'Bachelor of Computer Applications (BCA)')
