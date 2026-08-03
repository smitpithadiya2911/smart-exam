import os
from io import BytesIO
from django.http import HttpResponse
from django.conf import settings
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from exams.models import ExamAttempt
from questions.models import Question
from certificates.services import CertificateService
from .models import AnswerAttempt

class GradingService:
    @staticmethod
    def evaluate_attempt(attempt, request=None):
        """
        Auto-evaluates objective questions (MCQ, True/False, Fill in Blank)
        with negative marking applied correctly, and scales question marks
        proportionally so they sum exactly to the exam's configured total_marks.
        """
        from decimal import Decimal
        from exams.models import ExamAttempt
        exam = attempt.exam
        
        # Zero Tolerance: If cheating detected, invalidate all answers and force score to 0
        if attempt.status == ExamAttempt.Status.DISQUALIFIED:
            for q in exam.questions.all():
                ans, created = AnswerAttempt.objects.get_or_create(
                    attempt=attempt,
                    question=q,
                    defaults={'selected_option': '', 'text_response': '', 'marks_obtained': Decimal('0.00'), 'is_correct': False}
                )
                ans.is_correct = False
                ans.marks_obtained = Decimal('0.00')
                ans.save(update_fields=['is_correct', 'marks_obtained'])

            attempt.total_score = Decimal('0.00')
            attempt.percentage = Decimal('0.00')
            attempt.is_passed = False
            attempt.is_evaluated = True
            attempt.save(update_fields=['total_score', 'percentage', 'is_passed', 'is_evaluated'])
            return attempt

        answers = AnswerAttempt.objects.filter(attempt=attempt).select_related('question')
        
        # Calculate sum of all base question marks in the exam
        base_marks_sum = sum(float(q.marks) for q in exam.questions.all())
        exam_total = float(exam.total_marks) if float(exam.total_marks) > 0.0 else 100.0
        
        # Proportional scale factor
        scale_factor = exam_total / base_marks_sum if base_marks_sum > 0.0 else 1.0
        
        for ans in answers:
            q = ans.question
            # Objective question auto-evaluation
            if q.question_type in [Question.Type.MCQ, Question.Type.TRUE_FALSE, Question.Type.FILL_BLANK]:
                user_choice = (ans.selected_option or ans.text_response or "").strip().lower()
                correct_choice = (q.correct_answer or "").strip().lower()

                # Scale question marks proportionally to fit exam total_marks
                q_scaled_marks = float(q.marks) * scale_factor

                if user_choice and user_choice == correct_choice:
                    ans.is_correct = True
                    ans.marks_obtained = round(q_scaled_marks, 2)
                elif user_choice: # Wrong answer -> negative marking
                    ans.is_correct = False
                    ans.marks_obtained = -abs(float(exam.negative_marking))
                else: # Unanswered / skipped
                    ans.is_correct = False
                    ans.marks_obtained = 0.0

                ans.save(update_fields=['is_correct', 'marks_obtained'])

        # Recalculate total_score directly from DB to prevent any floating point accumulation issues or mismatch
        db_answers = AnswerAttempt.objects.filter(attempt=attempt)
        total_score_decimal = sum((Decimal(str(a.marks_obtained)) for a in db_answers), Decimal('0.00'))
        total_score = float(total_score_decimal)

        # Cap score at 0 minimum, and max at exam_total
        final_score = min(exam_total, max(0.0, total_score))
        attempt.total_score = final_score
        
        # Calculate percentage & pass status
        pct = (final_score / exam_total) * 100.0
        attempt.percentage = round(pct, 2)
        attempt.is_passed = final_score >= float(exam.passing_marks)
        attempt.is_evaluated = True
        attempt.save(update_fields=['total_score', 'percentage', 'is_passed', 'is_evaluated'])

        # Auto-generate QR Certificate if passed!
        if attempt.is_passed:
            CertificateService.generate_certificate(attempt, request=request)

        return attempt

class ResultPDFService:
    @staticmethod
    def generate_result_pdf(attempt):
        """Generates an official downloadable PDF Scorecard using ReportLab."""
        buffer = BytesIO()
        doc = SimpleDocTemplate(
            buffer,
            pagesize=letter,
            rightMargin=36, leftMargin=36, topMargin=36, bottomMargin=36
        )
        story = []
        styles = getSampleStyleSheet()

        title_style = ParagraphStyle(
            'TitleStyle',
            parent=styles['Heading1'],
            fontName='Helvetica-Bold',
            fontSize=20,
            textColor=colors.HexColor('#1e3a8a'),
            alignment=1, # Center
            spaceAfter=12
        )

        subtitle_style = ParagraphStyle(
            'SubTitleStyle',
            parent=styles['Normal'],
            fontName='Helvetica',
            fontSize=11,
            textColor=colors.HexColor('#475569'),
            alignment=1,
            spaceAfter=20
        )

        story.append(Paragraph("SMART ONLINE EXAMINATION SYSTEM", title_style))
        story.append(Paragraph("OFFICIAL EXAM PERFORMANCE SCORECARD", subtitle_style))
        story.append(Spacer(1, 10))

        # Candidate Details Table
        student = attempt.student
        exam = attempt.exam
        
        meta_data = [
            [Paragraph("<b>Student Name:</b>", styles['Normal']), Paragraph(student.get_full_name(), styles['Normal']),
             Paragraph("<b>Roll Number:</b>", styles['Normal']), Paragraph(getattr(getattr(student, 'student_profile', None), 'roll_number', 'N/A'), styles['Normal'])],
            [Paragraph("<b>Exam Title:</b>", styles['Normal']), Paragraph(exam.title, styles['Normal']),
             Paragraph("<b>Subject Code:</b>", styles['Normal']), Paragraph(exam.subject.code, styles['Normal'])],
            [Paragraph("<b>Date Taken:</b>", styles['Normal']), Paragraph(attempt.start_time.strftime("%d %b %Y, %H:%M"), styles['Normal']),
             Paragraph("<b>Status:</b>", styles['Normal']), Paragraph("PASSED" if attempt.is_passed else "FAILED", styles['Normal'])],
        ]

        meta_table = Table(meta_data, colWidths=[100, 170, 100, 170])
        meta_table.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#f8fafc')),
            ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#cbd5e1')),
            ('PADDING', (0,0), (-1,-1), 6),
        ]))
        story.append(meta_table)
        story.append(Spacer(1, 15))

        # Score Summary Box
        score_data = [
            ["Total Marks", "Passing Marks", "Marks Obtained", "Percentage", "Final Result"],
            [f"{exam.total_marks}", f"{exam.passing_marks}", f"{attempt.total_score}", f"{attempt.percentage}%", "PASS" if attempt.is_passed else "FAIL"]
        ]
        score_table = Table(score_data, colWidths=[108, 108, 108, 108, 108])
        score_table.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#1e3a8a')),
            ('TEXTCOLOR', (0,0), (-1,0), colors.white),
            ('ALIGN', (0,0), (-1,-1), 'CENTER'),
            ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#cbd5e1')),
            ('PADDING', (0,0), (-1,-1), 8),
            ('TEXTCOLOR', (4,1), (4,1), colors.HexColor('#16a34a') if attempt.is_passed else colors.HexColor('#dc2626')),
            ('FONTNAME', (0,0), (-1,-1), 'Helvetica-Bold'),
        ]))
        story.append(score_table)
        story.append(Spacer(1, 20))

        # Question Analysis Section
        story.append(Paragraph("<b>Question-wise Performance Breakdown:</b>", styles['Heading3']))
        story.append(Spacer(1, 5))

        q_rows = [["#", "Question Prompt", "Selected Option", "Status", "Score"]]
        answers = AnswerAttempt.objects.filter(attempt=attempt).select_related('question')
        
        # Calculate scale factor
        base_marks_sum = sum(float(ans.question.marks) for ans in answers)
        exam_total = float(attempt.exam.total_marks) if float(attempt.exam.total_marks) > 0.0 else 100.0
        scale_factor = exam_total / base_marks_sum if base_marks_sum > 0.0 else 1.0

        from django.utils.html import escape
        
        for i, ans in enumerate(answers, 1):
            scaled_max = round(float(ans.question.marks) * scale_factor, 2)
            safe_prompt = escape(ans.question.prompt_text[:60]) + "..."
            q_rows.append([
                str(i),
                Paragraph(safe_prompt, styles['Normal']),
                ans.selected_option or ans.text_response or "Skipped",
                "Correct" if ans.is_correct else ("Wrong" if ans.selected_option else "Skipped"),
                f"{ans.marks_obtained} / {scaled_max}"
            ])

        q_table = Table(q_rows, colWidths=[25, 255, 120, 70, 70])
        q_table.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#e2e8f0')),
            ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#cbd5e1')),
            ('PADDING', (0,0), (-1,-1), 5),
            ('FONTSIZE', (0,0), (-1,-1), 9),
        ]))
        story.append(q_table)

        doc.build(story)
        pdf_value = buffer.getvalue()
        buffer.close()

        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="Scorecard_{student.first_name}_{exam.subject.code}.pdf"'
        response.write(pdf_value)
        return response
