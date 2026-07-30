from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
from accounts.models import User
from departments.models import Department
from courses.models import Course
from semesters.models import Semester
from subjects.models import Subject
from students.models import StudentProfile
from teachers.models import TeacherProfile
from questions.models import Question
from exams.models import Exam, ExamAttempt
from results.models import AnswerAttempt
from results.services import GradingService
from notifications.models import Notification
from leaderboard.models import AchievementBadge, UserBadge

class Command(BaseCommand):
    help = 'Seeds realistic sample data for BCA Final Year Project'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS("Starting database seeding..."))

        # 1. SuperAdmin
        admin_user, _ = User.objects.get_or_create(
            email='smitpithadiya@gmail.com',
            defaults={
                'first_name': 'System',
                'last_name': 'Administrator',
                'role': User.Role.SUPER_ADMIN,
                'is_staff': True,
                'is_superuser': True
            }
        )
        admin_user.set_password('Smit#2911')
        admin_user.save()

        # 2. Departments
        dept_cs, _ = Department.objects.get_or_create(name='Computer Science & Applications', code='BCA-DEPT', description='School of Computer Science & Applications')
        dept_it, _ = Department.objects.get_or_create(name='Information Technology', code='IT-DEPT', description='School of IT')

        # 3. Courses
        course_bca, _ = Course.objects.get_or_create(name='Bachelor of Computer Applications', code='BCA', department=dept_cs, duration_years=3)
        course_bsc, _ = Course.objects.get_or_create(name='B.Sc Information Technology', code='BSCIT', department=dept_it, duration_years=3)

        # 4. Semesters
        start = timezone.now().date() - timedelta(days=90)
        end = start + timedelta(days=180)
        sem1, _ = Semester.objects.get_or_create(course=course_bca, number=1, defaults={'name': 'Semester I', 'start_date': start, 'end_date': end})
        sem6, _ = Semester.objects.get_or_create(course=course_bca, number=6, defaults={'name': 'Final Semester VI', 'start_date': start, 'end_date': end})

        # 5. Teachers
        teacher1_user, _ = User.objects.get_or_create(
            email='prof.sharma@exam.com',
            defaults={'first_name': 'Rajesh', 'last_name': 'Sharma', 'role': User.Role.TEACHER}
        )
        teacher1_user.set_password('Password123')
        teacher1_user.save()
        TeacherProfile.objects.get_or_create(user=teacher1_user, defaults={'employee_id': 'EMP001', 'department': dept_cs, 'designation': 'Senior Professor'})

        teacher2_user, _ = User.objects.get_or_create(
            email='prof.verma@exam.com',
            defaults={'first_name': 'Anita', 'last_name': 'Verma', 'role': User.Role.TEACHER}
        )
        teacher2_user.set_password('Password123')
        teacher2_user.save()
        TeacherProfile.objects.get_or_create(user=teacher2_user, defaults={'employee_id': 'EMP002', 'department': dept_cs, 'designation': 'Associate Professor'})

        # 6. Subjects
        subj_c, _ = Subject.objects.get_or_create(code='BCA101', defaults={'semester': sem1, 'name': 'C Programming & Logic', 'assigned_teacher': teacher1_user, 'credits': 4})
        subj_db, _ = Subject.objects.get_or_create(code='BCA601', defaults={'semester': sem6, 'name': 'Database Systems & MySQL', 'assigned_teacher': teacher2_user, 'credits': 4})
        subj_python, _ = Subject.objects.get_or_create(code='BCA602', defaults={'semester': sem6, 'name': 'Python & Web Frameworks', 'assigned_teacher': teacher1_user, 'credits': 4})

        # 7. Students
        s1, _ = User.objects.get_or_create(email='student.rahul@exam.com', defaults={'first_name': 'Rahul', 'last_name': 'Kumar', 'role': User.Role.STUDENT})
        s1.set_password('Password123')
        s1.save()
        StudentProfile.objects.get_or_create(user=s1, defaults={'roll_number': 'BCA2026-001', 'department': dept_cs, 'course': course_bca, 'semester': sem6})

        s2, _ = User.objects.get_or_create(email='student.priya@exam.com', defaults={'first_name': 'Priya', 'last_name': 'Singh', 'role': User.Role.STUDENT})
        s2.set_password('Password123')
        s2.save()
        StudentProfile.objects.get_or_create(user=s2, defaults={'roll_number': 'BCA2026-002', 'department': dept_cs, 'course': course_bca, 'semester': sem6})

        # 8. Question Bank
        sample_questions = [
            (subj_c, Question.Type.MCQ, "What is the size of int data type in 64-bit C compiler?", "2 Bytes", "4 Bytes", "8 Bytes", "1 Byte", "B", "In standard 64-bit C compilers, int is 4 bytes."),
            (subj_c, Question.Type.MCQ, "Which keyword is used to prevent variable modification in C?", "static", "const", "volatile", "extern", "B", "The const keyword defines constant read-only variables."),
            (subj_db, Question.Type.MCQ, "Which SQL command is used to retrieve data from a database?", "FETCH", "SELECT", "GET", "EXTRACT", "B", "SELECT statement queries database tables."),
            (subj_db, Question.Type.MCQ, "What does ACID stand for in Database Systems?", "Atomicity, Consistency, Isolation, Durability", "Access, Control, Index, Data", "Auto, Command, Input, Delete", "None of these", "A", "ACID guarantees transactional validity."),
            (subj_python, Question.Type.MCQ, "Which Django MVT component handles database queries?", "View", "Template", "Model", "Controller", "C", "Models encapsulate Django ORM database tables.")
        ]

        created_qs = []
        for subj, qtype, prompt, oa, ob, oc, od, ans, exp in sample_questions:
            q, _ = Question.objects.get_or_create(
                subject=subj, prompt_text=prompt,
                defaults={
                    'question_type': qtype, 'option_a': oa, 'option_b': ob, 'option_c': oc, 'option_d': od,
                    'correct_answer': ans, 'explanation': exp, 'marks': 20.0, 'difficulty': Question.Difficulty.MEDIUM
                }
            )
            created_qs.append(q)

        # 9. Exams
        now = timezone.now()
        exam_db, _ = Exam.objects.get_or_create(
            title='BCA Final Year MySQL & Database Exam',
            subject=subj_db,
            defaults={
                'created_by': teacher2_user,
                'start_time': now - timedelta(days=1),
                'end_time': now + timedelta(days=7),
                'duration_minutes': 30,
                'total_marks': 100.0,
                'passing_marks': 40.0,
                'negative_marking': 2.0,
                'is_published': True
            }
        )
        exam_db.questions.set(created_qs)

        # 10. Exam Attempt & Grading
        attempt1 = ExamAttempt.objects.create(exam=exam_db, student=s1, status=ExamAttempt.Status.COMPLETED)
        for q in created_qs:
            AnswerAttempt.objects.create(attempt=attempt1, question=q, selected_option=q.correct_answer)
        GradingService.evaluate_attempt(attempt1)

        # 11. Notifications
        Notification.objects.get_or_create(recipient=s1, title="Welcome to Smart Exam System", message="Your BCA Final Semester dashboard is ready.", notification_type=Notification.Type.ANNOUNCEMENT)

        self.stdout.write(self.style.SUCCESS("Database seeding completed successfully!"))
        self.stdout.write(self.style.SUCCESS("Credentials created:"))
        self.stdout.write(" - SuperAdmin: smitpithadiya@gmail.com / Smit#2911")
        self.stdout.write(" - Teacher: prof.sharma@exam.com / Password123")
        self.stdout.write(" - Student: student.rahul@exam.com / Password123")
