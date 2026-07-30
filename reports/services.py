import openpyxl
from io import BytesIO
from django.http import HttpResponse
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from exams.models import ExamAttempt, Exam
from accounts.models import User, LoginHistory

class ReportGeneratorService:
    @staticmethod
    def export_students_excel():
        wb = openpyxl.Workbook()
        ws = wb.active
        ws.title = "Students Performance"

        ws.append(['Email', 'Name', 'Role', 'Date Joined', 'Exams Appeared', 'Avg Score (%)'])
        students = User.objects.filter(role=User.Role.STUDENT)

        for s in students:
            attempts = ExamAttempt.objects.filter(student=s, status=ExamAttempt.Status.COMPLETED)
            cnt = attempts.count()
            avg_s = sum([float(a.percentage) for a in attempts]) / cnt if cnt > 0 else 0.0
            ws.append([s.email, s.get_full_name(), s.get_role_display(), s.date_joined.strftime('%Y-%m-%d'), cnt, round(avg_s, 2)])

        response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = 'attachment; filename=students_performance_report.xlsx'
        wb.save(response)
        return response

    @staticmethod
    def export_exams_summary_pdf():
        buffer = BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=letter, rightMargin=36, leftMargin=36, topMargin=36, bottomMargin=36)
        story = []
        styles = getSampleStyleSheet()

        title_style = ParagraphStyle('RepTitle', fontName='Helvetica-Bold', fontSize=18, textColor=colors.HexColor('#1e3a8a'), alignment=1, spaceAfter=15)
        story.append(Paragraph("SMART ONLINE EXAMINATION SYSTEM", title_style))
        story.append(Paragraph("SYSTEM EXAMS & RESULTS ANALYTICAL REPORT", ParagraphStyle('Sub', fontName='Helvetica', fontSize=11, alignment=1, spaceAfter=15)))
        story.append(Spacer(1, 10))

        rows = [["Exam Title", "Subject Code", "Total Marks", "Attempts", "Pass Rate (%)"]]
        exams = Exam.objects.select_related('subject').all()
        for e in exams:
            attempts = ExamAttempt.objects.filter(exam=e, status=ExamAttempt.Status.COMPLETED)
            cnt = attempts.count()
            passed = attempts.filter(is_passed=True).count()
            pass_rate = round((passed / cnt * 100.0), 1) if cnt > 0 else 0.0
            rows.append([e.title[:30], e.subject.code, str(e.total_marks), str(cnt), f"{pass_rate}%"])

        t = Table(rows, colWidths=[160, 90, 80, 80, 90])
        t.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#1e3a8a')),
            ('TEXTCOLOR', (0,0), (-1,0), colors.white),
            ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#cbd5e1')),
            ('PADDING', (0,0), (-1,-1), 6),
            ('ALIGN', (2,0), (-1,-1), 'CENTER'),
        ]))
        story.append(t)

        doc.build(story)
        pdf_val = buffer.getvalue()
        buffer.close()

        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="system_exams_summary_report.pdf"'
        response.write(pdf_val)
        return response
