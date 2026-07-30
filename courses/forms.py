from django import forms
from .models import Course

class CourseForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if 'department' in self.fields:
            self.fields['department'].empty_label = "-- Select Department --"

    class Meta:
        model = Course
        fields = ['name', 'code', 'department', 'duration_years', 'description']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control glass-input', 'placeholder': 'e.g. BCA General'}),
            'code': forms.TextInput(attrs={'class': 'form-control glass-input', 'placeholder': 'e.g. BCA101'}),
            'department': forms.Select(attrs={'class': 'form-select glass-input'}),
            'duration_years': forms.NumberInput(attrs={'class': 'form-control glass-input', 'placeholder': '3'}),
            'description': forms.Textarea(attrs={'class': 'form-control glass-input', 'rows': 3, 'placeholder': 'Course details...'}),
        }

