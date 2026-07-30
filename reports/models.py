from django.db import models

class SystemReportLog(models.Model):
    report_name = models.CharField(max_length=150)
    generated_by = models.CharField(max_length=150)
    format = models.CharField(max_length=20, default='PDF')
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.report_name} ({self.format}) at {self.timestamp.strftime('%Y-%m-%d %H:%M')}"
