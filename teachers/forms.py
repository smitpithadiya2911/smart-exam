from django import forms
from .models import TeacherProfile
from accounts.models import User

class TeacherRegistrationForm(forms.ModelForm):
    first_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control glass-input', 'placeholder': 'First Name', 'autocomplete': 'off'}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control glass-input', 'placeholder': 'Last Name', 'autocomplete': 'off'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={
        'class': 'form-control glass-input',
        'placeholder': 'Enter your email',
        'autocomplete': 'new-password'
    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control glass-input pe-5',
        'placeholder': 'Enter your password',
        'autocomplete': 'new-password'
    }))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if 'department' in self.fields:
            self.fields['department'].empty_label = "-- Select Department --"

    class Meta:
        model = TeacherProfile
        fields = ['employee_id', 'department', 'designation', 'qualification']
        widgets = {
            'employee_id': forms.TextInput(attrs={'class': 'form-control glass-input'}),
            'department': forms.Select(attrs={'class': 'form-select glass-input'}),
            'designation': forms.TextInput(attrs={'class': 'form-control glass-input'}),
            'qualification': forms.TextInput(attrs={'class': 'form-control glass-input'}),
        }

class TeacherEditForm(forms.ModelForm):
    first_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control glass-input'}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control glass-input'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control glass-input'}))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if 'department' in self.fields:
            self.fields['department'].empty_label = "-- Select Department --"

    class Meta:
        model = TeacherProfile
        fields = ['employee_id', 'department', 'designation', 'qualification']
        widgets = {
            'employee_id': forms.TextInput(attrs={'class': 'form-control glass-input'}),
            'department': forms.Select(attrs={'class': 'form-select glass-input'}),
            'designation': forms.TextInput(attrs={'class': 'form-control glass-input'}),
            'qualification': forms.TextInput(attrs={'class': 'form-control glass-input'}),
        }

