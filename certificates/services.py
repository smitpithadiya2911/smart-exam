import os
import qrcode
from io import BytesIO
from django.core.files.base import ContentFile
from django.conf import settings
from reportlab.lib.pagesizes import letter, landscape
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image as RLImage, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from .models import Certificate

class CertificateService:
    @staticmethod
    def generate_certificate(attempt):
        """Generates QR Code and PDF Certificate for a passed ExamAttempt."""
        cert, created = Certificate.objects.get_or_create(
            attempt=attempt,
            student=attempt.student,
            exam=attempt.exam
        )

        # Generate QR Code image linking to public verification page
        verification_url = f"http://127.0.0.1:8000/certificates/verify/{cert.certificate_uuid}/"
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_M,
            box_size=6,
            border=2,
        )
        qr.add_data(verification_url)
        qr.make(fit=True)
        img = qr.make_image(fill_color="#1e3a8a", back_color="white")

        qr_io = BytesIO()
        img.save(qr_io, format='PNG')
        qr_file_name = f"qr_{cert.certificate_uuid}.png"
        cert.qr_code_image.save(qr_file_name, ContentFile(qr_io.getvalue()), save=False)
        qr_io.close()

        # Build Landscape PDF Certificate
        pdf_io = BytesIO()
        doc = SimpleDocTemplate(
            pdf_io,
            pagesize=landscape(letter),
            rightMargin=36, leftMargin=36, topMargin=36, bottomMargin=36
        )
        story = []
        styles = getSampleStyleSheet()

        cert_title_style = ParagraphStyle(
            'CertTitle',
            fontName='Helvetica-Bold',
            fontSize=28,
            textColor=colors.HexColor('#1e3a8a'),
            alignment=1,
            spaceAfter=15
        )

        cert_sub_style = ParagraphStyle(
            'CertSub',
            fontName='Helvetica',
            fontSize=14,
            textColor=colors.HexColor('#475569'),
            alignment=1,
            spaceAfter=25
        )

        name_style = ParagraphStyle(
            'CertName',
            fontName='Helvetica-Bold',
            fontSize=24,
            textColor=colors.HexColor('#0284c7'),
            alignment=1,
            spaceAfter=15
        )

        body_style = ParagraphStyle(
            'CertBody',
            fontName='Helvetica',
            fontSize=12,
            textColor=colors.HexColor('#1e293b'),
            alignment=1,
            spaceAfter=30
        )

        story.append(Spacer(1, 20))
        story.append(Paragraph("CERTIFICATE OF ACHIEVEMENT", cert_title_style))
        story.append(Paragraph("SMART ONLINE EXAMINATION & LEARNING ANALYTICS SYSTEM", cert_sub_style))
        story.append(Paragraph("This is proudly presented to", ParagraphStyle('PresentTo', parent=cert_sub_style, fontSize=12)))
        story.append(Spacer(1, 10))
        story.append(Paragraph(attempt.student.get_full_name().upper(), name_style))
        story.append(Paragraph(
            f"for successfully qualifying the examination <b>{attempt.exam.title}</b> in "
            f"<b>{attempt.exam.subject.name} ({attempt.exam.subject.code})</b> with a score of <b>{attempt.percentage}%</b>.",
            body_style
        ))
        story.append(Spacer(1, 20))

        # Bottom section: Signature & QR Code
        qr_img_path = cert.qr_code_image.path if cert.qr_code_image else None
        
        sig_text = Paragraph("<b>Authorized Signatory</b><br/>Director of Examinations", ParagraphStyle('Sig', fontName='Helvetica', fontSize=10, alignment=1))
        verify_text = Paragraph(f"<b>Scan to Verify:</b><br/>ID: {str(cert.certificate_uuid)[:13]}...", ParagraphStyle('Ver', fontName='Helvetica', fontSize=8, alignment=1))

        if os.path.exists(qr_img_path):
            qr_rl_img = RLImage(qr_img_path, width=80, height=80)
            footer_table = Table([[sig_text, qr_rl_img, verify_text]], colWidths=[250, 100, 250])
        else:
            footer_table = Table([[sig_text, verify_text]], colWidths=[300, 300])

        footer_table.setStyle(TableStyle([
            ('ALIGN', (0,0), (-1,-1), 'CENTER'),
            ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ]))
        story.append(footer_table)

        doc.build(story)
        pdf_file_name = f"cert_{cert.certificate_uuid}.pdf"
        cert.pdf_file.save(pdf_file_name, ContentFile(pdf_io.getvalue()), save=False)
        pdf_io.close()

        cert.save()
        return cert
