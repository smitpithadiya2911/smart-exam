from django.db.models import Avg, Count, Q
from exams.models import ExamAttempt, Exam
from results.models import AnswerAttempt
from questions.models import Question
from .models import AIStudyRecommendation
import hashlib
from io import BytesIO
from django.http import HttpResponse
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from subjects.models import Subject
from django.utils import timezone
import statistics

class AIRecommendationService:
    @staticmethod
    def generate_recommendations_for_student(student_user):
        user_answers = AnswerAttempt.objects.filter(attempt__student=student_user).select_related('question', 'question__subject')
        recent_attempts = ExamAttempt.objects.filter(student=student_user, status=ExamAttempt.Status.COMPLETED).order_by('start_time')
        
        has_data = recent_attempts.exists()
        
        # 1. Dashboard Stats
        total_exams = recent_attempts.count()
        scores = [float(a.percentage) for a in recent_attempts]
        avg_score = round(sum(scores)/len(scores), 1) if scores else 0.0
        highest_score = round(max(scores), 1) if scores else 0.0
        lowest_score = round(min(scores), 1) if scores else 0.0
        
        # Calculate prep percent
        preparation_percent = avg_score
        
        # Consistency & Improvement
        improvement_percent = 0.0
        if len(scores) >= 3:
            first_three = sum(scores[:3])/3
            last_three = sum(scores[-3:])/3
            improvement_percent = round(last_three - first_three, 1)
        
        consistency_percent = 100.0
        if len(scores) >= 2:
            try:
                variance = statistics.variance(scores)
                consistency_percent = max(0.0, min(100.0, 100 - (variance / 10)))
            except Exception:
                pass
        
        # 2. Predicted Score & Probability
        trend_label = "Stable"
        predicted_next = 75.0
        if len(scores) >= 2:
            diff = scores[-1] - scores[0]
            if diff > 5:
                trend_label = "Upward Trajectory"
                predicted_next = min(100.0, scores[-1] + 4.0)
            elif diff < -5:
                trend_label = "Declining Trend"
                predicted_next = max(0.0, scores[-1] - 3.0)
            else:
                predicted_next = scores[-1]
        elif len(scores) == 1:
            predicted_next = scores[0]
            
        passing_probability = min(99.0, (predicted_next / 50.0) * 100.0) if predicted_next else 0.0
        risk_level = "High" if passing_probability < 50 else "Medium" if passing_probability < 75 else "Low"
        
        # 3. Confidence & Readiness
        total_ans = user_answers.count()
        skipped = user_answers.filter(selected_option__isnull=True, text_response__isnull=True).count()
        skip_ratio = (skipped / total_ans) if total_ans > 0 else 0
        confidence_score = max(0.0, 100.0 - (skip_ratio * 100 * 2))  # Penalty for skipping
        
        exam_readiness_percent = min(100.0, (preparation_percent * 0.7) + (confidence_score * 0.3))
        
        # 4. Topic-wise Analysis & AI Recommendations
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
        smart_suggestions = []
        
        best_topic = None
        best_acc = -1
        worst_topic = None
        worst_acc = 101
        
        for (subj_name, topic), data in topic_stats.items():
            if data['total'] > 0:
                acc = (data['correct'] / data['total']) * 100.0
                
                if acc > best_acc:
                    best_acc = acc
                    best_topic = topic
                if acc < worst_acc:
                    worst_acc = acc
                    worst_topic = topic
                
                difficulty = "Hard" if acc < 40 else "Medium" if acc < 70 else "Easy"
                priority = "High" if acc < 50 else "Medium" if acc < 75 else "Low"
                hours = 3 if priority == "High" else 2 if priority == "Medium" else 1
                rec_text = f"Revise {data['chapter'] or 'Core Notes'}"
                
                recommendations.append({
                    'subject_name': subj_name,
                    'weak_topic': topic,
                    'accuracy_percentage': round(acc, 1),
                    'difficulty_level': difficulty,
                    'confidence_score': round(acc * 0.9, 1),
                    'improvement_required': f"+{round(100-acc, 1)}%",
                    'estimated_study_hours': f"{hours} Hrs",
                    'expected_score_after': f"{round(min(100, acc + 15), 1)}%",
                    'priority_level': priority,
                    'ai_recommendation': rec_text
                })
        
        # Generate Smart Suggestions
        if has_data:
            if best_topic:
                smart_suggestions.append(f"You are strong in {best_topic}.")
            if worst_topic:
                smart_suggestions.append(f"Your weakest area is {worst_topic}. Spend more time here.")
            if skip_ratio > 0.2:
                smart_suggestions.append(f"You skip too many questions. Try attempting easier ones first.")
            smart_suggestions.append(f"Complete one Mock Test on Saturday.")
            smart_suggestions.append(f"Estimated improvement after following this plan: +{round(100-predicted_next, 1)*0.2:.1f}%")
            
        # Study Ratio
        remaining = max(0, 100 - preparation_percent)
        ratio_theory = int(remaining * 0.8)
        ratio_mcq = int(preparation_percent * 0.5)
        ratio_rev = int(preparation_percent * 0.2)
        ratio_mock = int(preparation_percent * 0.3)
        total_ratio = ratio_theory + ratio_mcq + ratio_rev + ratio_mock
        if total_ratio == 0: total_ratio = 1
        
        study_ratio = {
            'theory': round(ratio_theory/total_ratio*100),
            'mcq': round(ratio_mcq/total_ratio*100),
            'revision': round(ratio_rev/total_ratio*100),
            'mock': round(ratio_mock/total_ratio*100),
        }

        # Study hours
        today_hours = 3 if exam_readiness_percent < 50 else 2
        tomorrow_hours = 2
        mcq_count = int(120 * (study_ratio['mcq']/100))

        return {
            'has_data': has_data,
            'dashboard_stats': {
                'total_exams': total_exams,
                'avg_score': avg_score,
                'highest_score': highest_score,
                'lowest_score': lowest_score,
                'study_hours_total': total_exams * 2 + 10,
                'study_streak': 5
            },
            'preparation_percent': round(preparation_percent, 1),
            'exam_readiness_percent': round(exam_readiness_percent, 1),
            'confidence_score': round(confidence_score, 1),
            'passing_probability': round(passing_probability, 1),
            'risk_level': risk_level,
            'improvement_percent': improvement_percent,
            'consistency_percent': round(consistency_percent, 1),
            'predicted_next_score': round(predicted_next, 1),
            'trend_label': trend_label,
            'smart_suggestions': smart_suggestions,
            'topic_recommendations': sorted(recommendations, key=lambda x: x['accuracy_percentage']),
            'study_ratio': study_ratio,
            'study_hours': {
                'today': today_hours,
                'tomorrow': tomorrow_hours,
                'mcq_count': mcq_count
            }
        }


class AIStudyPlannerService:
    @staticmethod
    def get_planner_data(student_user):
        completed_attempts = ExamAttempt.objects.filter(
            student=student_user,
            status=ExamAttempt.Status.COMPLETED
        ).select_related('exam', 'exam__subject').order_by('-end_time')

        has_attempts = completed_attempts.exists()
        
        try:
            profile = student_user.student_profile
            if profile.course:
                subjects = list(Subject.objects.filter(course=profile.course))
            else:
                subjects = list(set(att.exam.subject for att in completed_attempts))
        except Exception:
            subjects = list(set(att.exam.subject for att in completed_attempts))
            
        if not subjects:
            subjects = list(Subject.objects.all())
            
        subjects.sort(key=lambda s: s.name)  # Sort for consistent order
        
        days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        slots = [
            'Morning (09:00 AM - 11:00 AM)',
            'Afternoon (02:00 PM - 04:00 PM)',
            'Evening (07:00 PM - 09:00 PM)'
        ]
        
        timetable = {}
        subject_idx = 0
        
        # Build dynamic all-exams timetable
        for day in days:
            timetable[day] = {}
            for slot in slots:
                if not subjects:
                    timetable[day][slot] = "Self Study / Academic Reading"
                    continue
                
                current_subj = subjects[subject_idx % len(subjects)]
                
                # Intelligent dynamic routing
                if day == 'Sunday':
                    if 'Morning' in slot:
                        timetable[day][slot] = "Weekly Revision of All Subjects"
                    elif 'Afternoon' in slot:
                        timetable[day][slot] = "Full Syllabus Mock Test / MCQ Practice"
                    else:
                        timetable[day][slot] = "Weekly Study Plan Review & Rest"
                elif day == 'Saturday':
                    timetable[day][slot] = f"Mock Test for {current_subj.name}"
                    subject_idx += 1
                else:
                    if 'Morning' in slot:
                        timetable[day][slot] = f"Theory: {current_subj.name}"
                    elif 'Afternoon' in slot:
                        timetable[day][slot] = f"MCQ Practice: {current_subj.name}"
                        subject_idx += 1
                    else:
                        timetable[day][slot] = "Revision & Note Making"
                        
        timetable_rows = []
        for slot in slots:
            slot_days = []
            for day in days:
                slot_days.append({
                    'day': day,
                    'activity': timetable[day][slot]
                })
            timetable_rows.append({
                'slot_name': slot,
                'days': slot_days
            })

        return {
            'has_attempts': has_attempts,
            'timetable': timetable,
            'timetable_rows': timetable_rows,
            'days': days,
            'slots': slots,
            'latest_exam_name': "All Evaluated Subjects" if has_attempts else "None"
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
            textColor=colors.HexColor('#00E5FF'),
            alignment=1,
            spaceAfter=12
        )
        
        section_style = ParagraphStyle(
            'PlannerSection',
            parent=styles['Heading2'],
            fontName='Helvetica-Bold',
            fontSize=14,
            textColor=colors.HexColor('#7B61FF'),
            spaceBefore=12,
            spaceAfter=6
        )
        
        story.append(Paragraph("AI PERSONALIZED STUDY PLANNER", title_style))
        story.append(Spacer(1, 10))
        
        table_data = [["Time Slot"] + days]
        
        for slot in slots:
            row = [slot]
            for day in days:
                row.append(timetable[day][slot])
            table_data.append(row)
            
        t = Table(table_data, colWidths=[100] + [75]*7)
        t.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#0B1120')),
            ('TEXTCOLOR', (0,0), (-1,0), colors.HexColor('#00E5FF')),
            ('ALIGN', (0,0), (-1,-1), 'CENTER'),
            ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
            ('GRID', (0,0), (-1,-1), 1, colors.HexColor('#1A2238')),
            ('BACKGROUND', (0,1), (0,-1), colors.HexColor('#121826')),
            ('TEXTCOLOR', (0,1), (-1,-1), colors.HexColor('#ffffff')),
            ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
            ('FONTSIZE', (0,0), (-1,-1), 8),
            ('WORDWRAP', (0,0), (-1,-1), True),
        ]))
        
        story.append(t)
        doc.build(story)
        
        pdf_value = buffer.getvalue()
        buffer.close()
        
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="AI_Study_Planner.pdf"'
        response.write(pdf_value)
        return response
