from django.db import models
from django.core.exceptions import ValidationError
from courses.models import Course

class Semester(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='semesters')
    number = models.PositiveIntegerField()
    name = models.CharField(max_length=100, help_text="e.g. Semester 1 / Final Semester")
    start_date = models.DateField()
    end_date = models.DateField()
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['course', 'number']
        unique_together = ('course', 'number')
        constraints = [
            models.CheckConstraint(
                check=models.Q(end_date__gt=models.F('start_date')),
                name='semester_end_date_after_start_date'
            )
        ]
        verbose_name = 'Semester'
        verbose_name_plural = 'Semesters'

    def clean(self):
        if self.start_date and self.end_date and self.end_date <= self.start_date:
            raise ValidationError({'end_date': 'End date must be strictly after start date.'})

    def __str__(self):
        return f"{self.course.code} - Sem {self.number} ({self.name})"
