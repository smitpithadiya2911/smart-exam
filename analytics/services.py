from django.db.models import Avg, Count, Q
from exams.models import ExamAttempt, Exam
from results.models import AnswerAttempt
from questions.models import Question
from .models import AIStudyRecommendation

class AIRecommendationService:
    @staticmethod
    def generate_recommendations_for_student(student_user):
        """
        Rule-based AI Learning Recommendation Engine:
        1. Analyzes student's past AnswerAttempts grouped by topic.
        2. Identifies weak topics (< 50% accuracy).
        3. Maps weak areas to suggested review chapters and recommended practice questions.
        4. Predicts future score improvement trend based on historical trajectory.
        """
        # Fetch all answers by this student
        user_answers = AnswerAttempt.objects.filter(attempt__student=student_user).select_related('question', 'question__subject')
        
        topic_stats = {}
        for ans in user_answers:
            topic = ans.question.topic or "General Fundamentals"
            subj_name = ans.question.subject.name
            key = (subj_name, topic)
            if key not in topic_stats:
                topic_stats[key] = {'total': 0, 'correct': 0, 'chapter': ans.question.chapter or ''}
            topic_stats[key]['total'] += 1
            if ans.is_correct:
                topic_stats[key]['correct'] += 1

        recommendations = []
        for (subj_name, topic), data in topic_stats.items():
            if data['total'] > 0:
                acc = (data['correct'] / data['total']) * 100.0
                if acc < 50.0:
                    rec_msg = f"Your accuracy in '{topic}' under {subj_name} is currently {acc:.1f}%. We recommend re-reading {data['chapter'] or 'the core notes'} and attempting 10 practice questions."
                    
                    obj, created = AIStudyRecommendation.objects.get_or_create(
                        student=student_user,
                        subject_name=subj_name,
                        weak_topic=topic,
                        defaults={
                            'accuracy_percentage': round(acc, 2),
                            'recommendation_text': rec_msg,
                            'suggested_chapter': data['chapter']
                        }
                    )
                    if not created:
                        obj.accuracy_percentage = round(acc, 2)
                        obj.recommendation_text = rec_msg
                        obj.save()
                    recommendations.append(obj)

        # Performance trend prediction
        recent_attempts = ExamAttempt.objects.filter(student=student_user, status=ExamAttempt.Status.COMPLETED).order_by('start_time')
        scores = [float(a.percentage) for a in recent_attempts]
        trend_label = "Stable"
        predicted_next = 75.0
        if len(scores) >= 2:
            diff = scores[-1] - scores[0]
            if diff > 5:
                trend_label = "Upward Trajectory (+{:.1f}%)".format(diff)
                predicted_next = min(100.0, scores[-1] + 4.0)
            elif diff < -5:
                trend_label = "Declining Trend ({:.1f}%)".format(diff)
                predicted_next = max(0.0, scores[-1] - 3.0)
            else:
                predicted_next = scores[-1]
        elif len(scores) == 1:
            predicted_next = scores[0]

        return {
            'weak_topic_recs': recommendations,
            'historical_scores': scores,
            'trend_label': trend_label,
            'predicted_next_score': round(predicted_next, 1)
        }


import hashlib
from io import BytesIO
from django.http import HttpResponse
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from subjects.models import Subject

class AIStudyPlannerService:
    @staticmethod
    def get_planner_data(student_user):
        # Fetch completed exam attempts for this student
        completed_attempts = ExamAttempt.objects.filter(
            student=student_user,
            status=ExamAttempt.Status.COMPLETED
        ).select_related('exam', 'exam__subject')

        has_attempts = completed_attempts.exists()
        
        # Extract unique subjects from completed attempts
        subjects = list(set(att.exam.subject for att in completed_attempts))
        try:
            profile = student_user.student_profile
        except Exception:
            profile = None

        subject_progress = []
        subject_weights = {}

        for subject in subjects:
            attempts = completed_attempts.filter(exam__subject=subject)
            
            avg_score = attempts.aggregate(Avg('percentage'))['percentage__avg']
            avg_score = float(avg_score) if avg_score is not None else 0.0
                
            from results.models import AnswerAttempt
            ans_attempts = AnswerAttempt.objects.filter(
                attempt__student=student_user,
                question__subject=subject
            )
            total_ans = ans_attempts.count()
            correct_ans = ans_attempts.filter(is_correct=True).count()
            accuracy = (correct_ans / total_ans * 100.0) if total_ans > 0 else None
            
            progress_val = avg_score
            
            if progress_val < 50.0:
                priority = "Critical Focus (High Effort)"
                weight = 3.0
                suggestion = "Focus heavily on weak topics, re-read textbook chapters, and do daily practice questions."
            elif progress_val < 75.0:
                priority = "Moderate Focus (Medium Effort)"
                weight = 2.0
                suggestion = "Practice intermediate problems and focus on reducing small errors."
            else:
                priority = "Steady Progress (Low Effort)"
                weight = 1.0
                suggestion = "Maintain standard practice, do mock tests, and keep formulas/syntax fresh."
                
            subject_progress.append({
                'subject': subject,
                'avg_score': avg_score,
                'accuracy': accuracy,
                'progress_val': round(progress_val, 1),
                'priority': priority,
                'suggestion': suggestion
            })
            subject_weights[subject.id] = weight

        days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        slots = [
            'Morning (09:00 AM - 11:00 AM)',
            'Afternoon (02:00 PM - 04:00 PM)',
            'Evening (07:00 PM - 09:00 PM)'
        ]
        
        weighted_pool = []
        for s_prog in subject_progress:
            w = int(subject_weights[s_prog['subject'].id])
            weighted_pool.extend([s_prog['subject']] * w)
            
        if not weighted_pool:
            weighted_pool = subjects
            
        timetable = {}
        
        if has_attempts:
            weights_str = "".join([f"{sid}:{w}" for sid, w in sorted(subject_weights.items())])
            seed_str = f"{student_user.id}:{weights_str}"
            seed_int = int(hashlib.md5(seed_str.encode('utf-8')).hexdigest(), 16) % 100000
            idx = seed_int
        else:
            idx = 0
            
        for day in days:
            timetable[day] = {}
            for slot in slots:
                if day == 'Sunday':
                    if slot == 'Morning (09:00 AM - 11:00 AM)':
                        timetable[day][slot] = "Weekly Revision of All Subjects"
                    elif slot == 'Afternoon (02:00 PM - 04:00 PM)':
                        timetable[day][slot] = "Full Syllabus Mock Test / MCQ Practice"
                    else:
                        timetable[day][slot] = "Weekly Study Plan Review & Rest"
                else:
                    if weighted_pool:
                        selected_subj = weighted_pool[idx % len(weighted_pool)]
                        timetable[day][slot] = f"{selected_subj.name} ({selected_subj.code})"
                        idx += 1
                    else:
                        timetable[day][slot] = "Self Study / Academic Reading"
                        
        timetable_rows = []
        for slot in slots:
            slot_days = []
            for day in days:
                activity = timetable[day][slot]
                slot_days.append({
                    'day': day,
                    'activity': activity
                })
            timetable_rows.append({
                'slot_name': slot,
                'days': slot_days
            })

        return {
            'has_attempts': has_attempts,
            'subject_progress': subject_progress,
            'timetable': timetable,
            'timetable_rows': timetable_rows,
            'days': days,
            'slots': slots,
            'profile': profile
        }

    @staticmethod
    def generate_timetable_pdf(student_user):
        data = AIStudyPlannerService.get_planner_data(student_user)
        timetable = data['timetable']
        days = data['days']
        slots = data['slots']
        
        buffer = BytesIO()
        doc = SimpleDocTemplate(
            buffer,
            pagesize=letter,
            rightMargin=36, leftMargin=36, topMargin=36, bottomMargin=36
        )
        story = []
        styles = getSampleStyleSheet()
        
        title_style = ParagraphStyle(
            'PlannerTitle',
            parent=styles['Heading1'],
            fontName='Helvetica-Bold',
            fontSize=20,
            textColor=colors.HexColor('#002b49'),
            alignment=1,
            spaceAfter=12
        )
        
        section_style = ParagraphStyle(
            'PlannerSection',
            parent=styles['Heading2'],
            fontName='Helvetica-Bold',
            fontSize=14,
            textColor=colors.HexColor('#002b49'),
            spaceBefore=12,
            spaceAfter=6
        )
        
        text_style = ParagraphStyle(
            'PlannerText',
            parent=styles['Normal'],
            fontName='Helvetica',
            fontSize=10,
            textColor=colors.HexColor('#333333'),
            spaceAfter=4
        )
        
        header_text = f"<b>Student:</b> {student_user.get_full_name()} ({student_user.email})<br/>"
        if data['profile']:
            header_text += f"<b>Roll Number:</b> {data['profile'].roll_number} | <b>Course:</b> {data['profile'].course.name if data['profile'].course else 'N/A'} | <b>Semester:</b> {data['profile'].semester.number if data['profile'].semester else 'N/A'}"
        
        story.append(Paragraph("AI PERSONALIZED STUDY PLANNER", title_style))
        story.append(Paragraph(header_text, text_style))
        story.append(Spacer(1, 15))
        
        # 1. Subject Progress & Suggestions
        story.append(Paragraph("Subject Progress & AI Recommendations", section_style))
        table_data = [["Subject Code & Name", "Average Score", "AI Study Priority & Suggestion"]]
        for item in data['subject_progress']:
            sub = item['subject']
            avg = f"{item['progress_val']}%" if item['avg_score'] is not None or item['accuracy'] is not None else "No Attempts"
            suggestion_p = f"<b>{item['priority']}</b><br/>{item['suggestion']}"
            table_data.append([
                Paragraph(f"<b>{sub.code}</b><br/>{sub.name}", text_style),
                Paragraph(avg, text_style),
                Paragraph(suggestion_p, text_style)
            ])
            
        progress_table = Table(table_data, colWidths=[150, 80, 310])
        progress_table.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#002b49')),
            ('TEXTCOLOR', (0,0), (-1,0), colors.white),
            ('ALIGN', (0,0), (-1,-1), 'LEFT'),
            ('VALIGN', (0,0), (-1,-1), 'TOP'),
            ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#dddddd')),
            ('PADDING', (0,0), (-1,-1), 6),
        ]))
        
        # Fix table header text color
        for i in range(3):
            table_data[0][i] = Paragraph(f"<font color='white'><b>{table_data[0][i]}</b></font>", text_style)
            
        story.append(progress_table)
        story.append(Spacer(1, 15))
        
        # 2. Study Timetable Grid
        story.append(Paragraph("Weekly Routine Study Timetable", section_style))
        
        # Grid format: Row for each day, cols: Day, Morning, Afternoon, Evening
        grid_data = [["Day", "Morning\n(09:00 - 11:00 AM)", "Afternoon\n(02:00 - 04:00 PM)", "Evening\n(07:00 - 09:00 PM)"]]
        for day in days:
            row = [day]
            for slot in slots:
                row.append(timetable[day][slot])
            grid_data.append(row)
            
        # Convert all to Paragraphs for text wrapping
        formatted_grid = []
        for r_idx, row in enumerate(grid_data):
            formatted_row = []
            for c_idx, cell in enumerate(row):
                if r_idx == 0:
                    formatted_row.append(Paragraph(f"<font color='white'><b>{cell}</b></font>", text_style))
                else:
                    if c_idx == 0:
                        formatted_row.append(Paragraph(f"<b>{cell}</b>", text_style))
                    else:
                        formatted_row.append(Paragraph(cell, text_style))
            formatted_grid.append(formatted_row)
            
        timetable_table = Table(formatted_grid, colWidths=[80, 153, 153, 154])
        timetable_table.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#002b49')),
            ('TEXTCOLOR', (0,0), (-1,0), colors.white),
            ('ALIGN', (0,0), (-1,-1), 'LEFT'),
            ('VALIGN', (0,0), (-1,-1), 'TOP'),
            ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#dddddd')),
            ('PADDING', (0,0), (-1,-1), 6),
        ]))
        story.append(timetable_table)
        
        doc.build(story)
        buffer.seek(0)
        
        response = HttpResponse(buffer.read(), content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="AI_Study_Planner_{student_user.id}.pdf"'
        return response
