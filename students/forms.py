from django import forms
from .models import StudentProfile
from accounts.models import User

class StudentProfileForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if 'department' in self.fields:
            self.fields['department'].empty_label = "-- Select Department --"
        if 'course' in self.fields:
            self.fields['course'].empty_label = "-- Select Course --"
        if 'semester' in self.fields:
            self.fields['semester'].empty_label = "-- Select Semester --"

    class Meta:
        model = StudentProfile
        fields = ['roll_number', 'department', 'course', 'semester', 'address']
        widgets = {
            'roll_number': forms.TextInput(attrs={'class': 'form-control glass-input'}),
            'department': forms.Select(attrs={'class': 'form-select glass-input'}),
            'course': forms.Select(attrs={'class': 'form-select glass-input'}),
            'semester': forms.Select(attrs={'class': 'form-select glass-input'}),
            'address': forms.Textarea(attrs={'class': 'form-control glass-input', 'rows': 3}),
        }

class StudentEditForm(forms.ModelForm):
    first_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control glass-input'}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control glass-input'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control glass-input'}))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if 'department' in self.fields:
            self.fields['department'].empty_label = "-- Select Department --"
        if 'course' in self.fields:
            self.fields['course'].empty_label = "-- Select Course --"
        if 'semester' in self.fields:
            self.fields['semester'].empty_label = "-- Select Semester --"

    class Meta:
        model = StudentProfile
        fields = ['roll_number', 'department', 'course', 'semester', 'address']
        widgets = {
            'roll_number': forms.TextInput(attrs={'class': 'form-control glass-input'}),
            'department': forms.Select(attrs={'class': 'form-select glass-input'}),
            'course': forms.Select(attrs={'class': 'form-select glass-input'}),
            'semester': forms.Select(attrs={'class': 'form-select glass-input'}),
            'address': forms.Textarea(attrs={'class': 'form-control glass-input', 'rows': 3}),
        }

