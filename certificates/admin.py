from django.contrib import admin
from .models import Certificate

@admin.register(Certificate)
class CertificateAdmin(admin.ModelAdmin):
    list_display = ('certificate_uuid', 'student', 'exam', 'issue_date')
    search_fields = ('certificate_uuid', 'student__email', 'exam__title')
