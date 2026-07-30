from django import forms
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError

User = get_user_model()

class LoginForm(forms.Form):
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'class': 'form-control glass-input', 'placeholder': 'Enter your email', 'autocomplete': 'off'})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control glass-input pe-5', 'placeholder': 'Enter your password', 'autocomplete': 'new-password'})
    )
    captcha_answer = forms.IntegerField(
        required=True,
        widget=forms.NumberInput(attrs={'class': 'form-control glass-input', 'placeholder': 'Answer', 'autocomplete': 'off'})
    )
    remember_me = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}))

class StudentRegistrationForm(forms.ModelForm):
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control glass-input pe-5', 'placeholder': 'Enter your password', 'autocomplete': 'new-password'})
    )
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control glass-input pe-5', 'placeholder': 'Enter your password', 'autocomplete': 'new-password'})
    )
    department_id = forms.CharField(required=False, widget=forms.HiddenInput())
    course_id = forms.CharField(required=False, widget=forms.HiddenInput())
    semester_id = forms.CharField(required=False, widget=forms.HiddenInput())

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'phone_number']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control glass-input', 'placeholder': 'First Name', 'autocomplete': 'off'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control glass-input', 'placeholder': 'Last Name', 'autocomplete': 'off'}),
            'email': forms.EmailInput(attrs={'class': 'form-control glass-input', 'placeholder': 'Enter your email', 'autocomplete': 'off'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control glass-input', 'placeholder': '+91', 'autocomplete': 'off'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')
        if password and confirm_password and password != confirm_password:
            raise ValidationError("Passwords do not match.")
        return cleaned_data

class ForgotPasswordForm(forms.Form):
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'class': 'form-control glass-input', 'placeholder': 'Enter your email', 'autocomplete': 'off'})
    )

class VerifyOTPForm(forms.Form):
    otp = forms.CharField(
        max_length=6,
        widget=forms.TextInput(attrs={'class': 'form-control glass-input text-center tracking-widest', 'placeholder': '123456'})
    )
    new_password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control glass-input pe-5', 'placeholder': 'Enter your password'})
    )


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'phone_number', 'avatar', 'dark_mode']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control glass-input'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control glass-input'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control glass-input'}),
            'avatar': forms.FileInput(attrs={'class': 'form-control glass-input'}),
            'dark_mode': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
