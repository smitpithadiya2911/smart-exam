import random
from django.utils import timezone
from .models import Exam, ExamAttempt, AttemptViolation
from questions.models import Question

class ExamService:
    @staticmethod
    def start_exam_attempt(user, exam):
        """Initializes or retrieves an ongoing exam attempt for a student."""
        ongoing = ExamAttempt.objects.filter(
            exam=exam,
            student=user,
            status=ExamAttempt.Status.IN_PROGRESS
        ).first()

        if ongoing:
            # If the ongoing attempt has an empty question list (e.g. from an earlier empty config)
            # but the subject has questions, populate them dynamically
            if not ongoing.question_order:
                q_ids = list(exam.questions.values_list('id', flat=True))
                if not q_ids:
                    from questions.services import QuestionService
                    sampled = QuestionService.generate_random_questions(exam.subject.id, 10)
                    exam.questions.set(sampled)
                    q_ids = list(exam.questions.values_list('id', flat=True))
                if exam.shuffle_questions:
                    random.shuffle(q_ids)
                ongoing.question_order = q_ids
                ongoing.save(update_fields=['question_order'])
            return ongoing

        # Fetch exam questions
        q_ids = list(exam.questions.values_list('id', flat=True))
        if not q_ids:
            # Fallback: if exam has no questions, sample 10 questions from the subject question bank
            from questions.services import QuestionService
            sampled = QuestionService.generate_random_questions(exam.subject.id, 10)
            exam.questions.set(sampled)
            q_ids = list(exam.questions.values_list('id', flat=True))

        if exam.shuffle_questions:
            random.shuffle(q_ids)

        attempt = ExamAttempt.objects.create(
            exam=exam,
            student=user,
            question_order=q_ids,
            status=ExamAttempt.Status.IN_PROGRESS
        )
        return attempt

    @staticmethod
    def get_remaining_seconds(attempt):
        """Calculates server-verified remaining time in seconds."""
        exam = attempt.exam
        elapsed = (timezone.now() - attempt.start_time).total_seconds()
        total_allowed = exam.duration_minutes * 60
        remaining = total_allowed - elapsed
        return max(0, int(remaining))

    @staticmethod
    def log_violation(attempt, violation_type, details=""):
        """Logs anti-cheating violation and auto-submits if threshold breached."""
        AttemptViolation.objects.create(
            attempt=attempt,
            violation_type=violation_type,
            details=details
        )
        attempt.violations_count += 1
        attempt.save(update_fields=['violations_count'])

        if attempt.violations_count >= attempt.exam.max_violations:
            attempt.status = ExamAttempt.Status.DISQUALIFIED
            attempt.end_time = timezone.now()
            attempt.save(update_fields=['status', 'end_time'])
            
            # Auto-evaluate saved answers
            from results.services import GradingService
            GradingService.evaluate_attempt(attempt)
            return True # Disqualified & auto-submitted
        return False
