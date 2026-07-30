from django.db import models
from django.conf import settings
import uuid
from exams.models import ExamAttempt, Exam

class Certificate(models.Model):
    certificate_uuid = models.UUIDField(default=uuid.uuid4, unique=True, editable=False, db_index=True)
    attempt = models.OneToOneField(ExamAttempt, on_delete=models.CASCADE, related_name='certificate')
    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='certificates')
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE, related_name='certificates')
    issue_date = models.DateField(auto_now_add=True)
    
    qr_code_image = models.ImageField(upload_to='certificates/qr_codes/', blank=True, null=True)
    pdf_file = models.FileField(upload_to='certificates/pdfs/', blank=True, null=True)

    class Meta:
        ordering = ['-issue_date']
        verbose_name = 'Certificate'
        verbose_name_plural = 'Certificates'

    def __str__(self):
        return f"Certificate {self.certificate_uuid} - {self.student.get_full_name()} ({self.exam.subject.code})"
