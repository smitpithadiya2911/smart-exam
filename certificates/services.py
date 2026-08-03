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
    @staticmethod
    def generate_certificate(attempt, request=None):
        """Generates QR Code and PDF Certificate for a passed ExamAttempt."""
        cert, created = Certificate.objects.get_or_create(
            attempt=attempt,
            student=attempt.student,
            exam=attempt.exam
        )

        # Generate QR Code image linking to public verification page
        if request:
            verification_url = request.build_absolute_uri(f"/certificates/verify/{cert.certificate_uuid}/")
        else:
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
            rightMargin=50, leftMargin=50, topMargin=50, bottomMargin=50
        )
        story = []
        styles = getSampleStyleSheet()

        cert_title_style = ParagraphStyle(
            'CertTitle',
            fontName='Times-BoldItalic',
            fontSize=36,
            textColor=colors.HexColor('#1e3a8a'),
            alignment=1,
            spaceAfter=20
        )

        cert_sub_style = ParagraphStyle(
            'CertSub',
            fontName='Helvetica',
            fontSize=16,
            textColor=colors.HexColor('#475569'),
            alignment=1,
            spaceAfter=30
        )

        name_style = ParagraphStyle(
            'CertName',
            fontName='Times-BoldItalic',
            fontSize=32,
            textColor=colors.HexColor('#0284c7'),
            alignment=1,
            spaceAfter=20
        )

        body_style = ParagraphStyle(
            'CertBody',
            fontName='Times-Roman',
            fontSize=16,
            textColor=colors.HexColor('#1e293b'),
            alignment=1,
            spaceAfter=40
        )

        story.append(Spacer(1, 100)) # Space for the seal/logo at the top
        story.append(Paragraph("Certificate of Achievement", cert_title_style))
        story.append(Paragraph("SMART ONLINE EXAMINATION SYSTEM", cert_sub_style))
        story.append(Paragraph("This is proudly presented to", ParagraphStyle('PresentTo', parent=cert_sub_style, fontSize=14)))
        story.append(Spacer(1, 10))
        story.append(Paragraph(attempt.student.get_full_name().title(), name_style))
        story.append(Spacer(1, 10))
        story.append(Paragraph(
            f"For successfully qualifying the examination <b>{attempt.exam.title}</b> in <br/>"
            f"<b>{attempt.exam.subject.name} ({attempt.exam.subject.code})</b> with a passing score.",
            body_style
        ))
        story.append(Spacer(1, 20))

        # Bottom section: Signature & QR Code
        qr_img_path = cert.qr_code_image.path if cert.qr_code_image else None
        
        sig_text = Paragraph("<b>_________________________</b><br/><br/><b>Authorized Signatory</b><br/>Director of Examinations", ParagraphStyle('Sig', fontName='Helvetica', fontSize=12, alignment=1))
        verify_text = Paragraph(f"<b>Scan to Verify</b><br/>ID: {str(cert.certificate_uuid)[:13]}...", ParagraphStyle('Ver', fontName='Helvetica', fontSize=10, alignment=1))

        if os.path.exists(qr_img_path):
            qr_rl_img = RLImage(qr_img_path, width=70, height=70)
            footer_table = Table([[sig_text, qr_rl_img, verify_text]], colWidths=[250, 100, 250])
        else:
            footer_table = Table([[sig_text, verify_text]], colWidths=[300, 300])

        footer_table.setStyle(TableStyle([
            ('ALIGN', (0,0), (-1,-1), 'CENTER'),
            ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ]))
        story.append(footer_table)

        def add_background_and_border(canvas, doc):
            canvas.saveState()
            # Draw double border
            canvas.setStrokeColor(colors.HexColor('#1e3a8a'))
            canvas.setLineWidth(4)
            canvas.rect(20, 20, doc.width + 100 - 40, doc.height + 100 - 40)
            canvas.setStrokeColor(colors.HexColor('#0284c7'))
            canvas.setLineWidth(1)
            canvas.rect(26, 26, doc.width + 100 - 52, doc.height + 100 - 52)
            
            # Corner accents
            canvas.setLineWidth(2)
            canvas.setStrokeColor(colors.HexColor('#f59e0b')) # Gold
            for x, y in [(20, 20), (doc.width+60, 20), (20, doc.height+60), (doc.width+60, doc.height+60)]:
                canvas.circle(x, y, 6, fill=1)

            # Draw text logo (EdTech Core)
            logo_y = doc.height + 100 - 90
            canvas.setStrokeColor(colors.HexColor('#1e3a8a'))
            canvas.setFillColor(colors.white)
            canvas.setLineWidth(2)
            canvas.circle(80, logo_y, 40, stroke=1, fill=1)
            
            # Inner circle
            canvas.setStrokeColor(colors.HexColor('#f59e0b'))
            canvas.circle(80, logo_y, 35, stroke=1, fill=0)

            # Text inside logo
            canvas.setFillColor(colors.HexColor('#1e3a8a'))
            canvas.setFont("Helvetica-Bold", 10)
            canvas.drawCentredString(80, logo_y + 5, "EDTECH")
            canvas.drawCentredString(80, logo_y - 10, "CORE")
            canvas.restoreState()

        doc.build(story, onFirstPage=add_background_and_border)
        pdf_file_name = f"cert_{cert.certificate_uuid}.pdf"
        cert.pdf_file.save(pdf_file_name, ContentFile(pdf_io.getvalue()), save=False)
        pdf_io.close()

        cert.save()
        return cert
