from django import forms
from .models import Department

class DepartmentForm(forms.ModelForm):
    class Meta:
        model = Department
        fields = ['name', 'code', 'description']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control glass-input', 'placeholder': 'e.g. Computer Applications'}),
            'code': forms.TextInput(attrs={'class': 'form-control glass-input', 'placeholder': 'e.g. BCA'}),
            'description': forms.Textarea(attrs={'class': 'form-control glass-input', 'rows': 3, 'placeholder': 'Department details...'}),
        }
