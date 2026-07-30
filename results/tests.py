from django.test import TestCase
from django.utils import timezone
from datetime import timedelta
from accounts.models import User
from departments.models import Department
from courses.models import Course
from semesters.models import Semester
from subjects.models import Subject
from questions.models import Question
from exams.models import Exam, ExamAttempt
from .models import AnswerAttempt
from .services import GradingService

class GradingServiceTest(TestCase):
    def test_auto_grading(self):
        user = User.objects.create_user(email='prof@exam.com', password='pass', role=User.Role.TEACHER)
        student = User.objects.create_user(email='student@exam.com', password='pass', role=User.Role.STUDENT)
        dept = Department.objects.create(name='CS', code='CS')
        course = Course.objects.create(name='BCA', code='BCA', department=dept)
        sem = Semester.objects.create(course=course, number=1, name='Sem 1', start_date=timezone.now().date(), end_date=timezone.now().date() + timedelta(days=180))
        subject = Subject.objects.create(semester=sem, name='C Prog', code='BCA101')
        q1 = Question.objects.create(subject=subject, question_type=Question.Type.MCQ, prompt_text='Q1', correct_answer='A', marks=5)

        exam = Exam.objects.create(
            title='Midterm', subject=subject, created_by=user,
            start_time=timezone.now(), end_time=timezone.now()+timedelta(hours=1),
            duration_minutes=60, total_marks=5, passing_marks=2
        )
        exam.questions.add(q1)

        attempt = ExamAttempt.objects.create(exam=exam, student=student, status=ExamAttempt.Status.COMPLETED)
        AnswerAttempt.objects.create(attempt=attempt, question=q1, selected_option='A')

        GradingService.evaluate_attempt(attempt)
        self.assertEqual(float(attempt.total_score), 5.0)
        self.assertTrue(attempt.is_passed)
