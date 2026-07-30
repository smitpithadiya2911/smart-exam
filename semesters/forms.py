from django import forms
from .models import Semester

class SemesterForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if 'course' in self.fields:
            self.fields['course'].empty_label = "-- Select Course --"

    class Meta:
        model = Semester
        fields = ['course', 'number', 'name', 'start_date', 'end_date', 'is_active']
        widgets = {
            'course': forms.Select(attrs={'class': 'form-select glass-input'}),
            'number': forms.NumberInput(attrs={'class': 'form-control glass-input', 'placeholder': '1'}),
            'name': forms.TextInput(attrs={'class': 'form-control glass-input', 'placeholder': 'e.g. Fall 2026'}),
            'start_date': forms.DateInput(attrs={'class': 'form-control glass-input', 'type': 'date'}),
            'end_date': forms.DateInput(attrs={'class': 'form-control glass-input', 'type': 'date'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

