from django import forms
from .models import Subject
from accounts.models import User

class SubjectForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if 'semester' in self.fields:
            self.fields['semester'].empty_label = "-- Select Semester --"
        if 'assigned_teacher' in self.fields:
            self.fields['assigned_teacher'].queryset = User.objects.filter(role=User.Role.TEACHER)
            self.fields['assigned_teacher'].empty_label = "-- Select Teacher (Optional) --"

    class Meta:
        model = Subject
        fields = ['semester', 'name', 'code', 'assigned_teacher', 'credits', 'description']
        widgets = {
            'semester': forms.Select(attrs={'class': 'form-select glass-input'}),
            'name': forms.TextInput(attrs={'class': 'form-control glass-input', 'placeholder': 'e.g. Data Structures & Algorithms'}),
            'code': forms.TextInput(attrs={'class': 'form-control glass-input', 'placeholder': 'e.g. BCA301'}),
            'assigned_teacher': forms.Select(attrs={'class': 'form-select glass-input'}),
            'credits': forms.NumberInput(attrs={'class': 'form-control glass-input', 'placeholder': '4'}),
            'description': forms.Textarea(attrs={'class': 'form-control glass-input', 'rows': 3, 'placeholder': 'Subject details...'}),
        }

