from django.test import TestCase
from django.utils import timezone
from datetime import timedelta
from departments.models import Department
from courses.models import Course
from semesters.models import Semester
from subjects.models import Subject
from questions.models import Question
from questions.services import QuestionService

class QuestionBankTest(TestCase):
    def setUp(self):
        dept = Department.objects.create(name='CS', code='CS')
        course = Course.objects.create(name='BCA', code='BCA', department=dept)
        sem = Semester.objects.create(course=course, number=1, name='Sem 1', start_date=timezone.now().date(), end_date=timezone.now().date() + timedelta(days=180))
        self.subject = Subject.objects.create(semester=sem, name='C Prog', code='BCA101')
        for i in range(5):
            Question.objects.create(
                subject=self.subject,
                question_type=Question.Type.MCQ,
                prompt_text=f"Question {i}",
                option_a="Opt A", option_b="Opt B", option_c="Opt C", option_d="Opt D",
                correct_answer="A"
            )

    def test_random_question_generator(self):
        sample = QuestionService.generate_random_questions(self.subject.id, 3)
        self.assertEqual(sample.count(), 3)

    def test_import_questions_from_pdf_with_answer_key_at_end(self):
        from unittest.mock import MagicMock, patch
        from questions.services import QuestionService

        mock_page1 = MagicMock()
        mock_page1.extract_text.return_value = (
            "1. What is Python?\n"
            "(A) Snake (B) Language\n"
            "(C) Food (D) None\n\n"
            "2. What is Django?\n"
            "A) Web Framework B) Movie\n"
            "C) Music D) Car\n\n"
            "Answer Key\n"
            "1. B\n"
            "2. A\n"
        )

        mock_reader = MagicMock()
        mock_reader.pages = [mock_page1]

        with patch('pypdf.PdfReader', return_value=mock_reader):
            from io import BytesIO
            file_obj = BytesIO(b"dummy pdf data")
            created_qs = QuestionService.import_questions_from_pdf(file_obj, self.subject)
            
            self.assertEqual(created_qs.count(), 2)
            q1 = created_qs.get(prompt_text="What is Python?")
            q2 = created_qs.get(prompt_text="What is Django?")
            
            self.assertEqual(q1.correct_answer, "B")
            self.assertEqual(q2.correct_answer, "A")
