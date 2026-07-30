from django.test import TestCase
from .models import SystemReportLog

class ReportLogTest(TestCase):
    def test_log_creation(self):
        log = SystemReportLog.objects.create(report_name='Test Report', generated_by='smitpithadiya@gmail.com', format='PDF')
        self.assertEqual(log.format, 'PDF')
