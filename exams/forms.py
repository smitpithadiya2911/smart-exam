from django import forms
from .models import Exam

class ExamConfigForm(forms.ModelForm):
    question_pdf = forms.FileField(
        required=False,
        label="Upload AI Questions PDF (Optional)",
        widget=forms.FileInput(attrs={'class': 'form-control glass-input', 'accept': '.pdf'}),
        help_text="Upload a PDF of MCQ questions from an AI platform to automatically import them."
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if 'subject' in self.fields:
            self.fields['subject'].empty_label = "-- Select Subject --"

    class Meta:
        model = Exam
        fields = [
            'title', 'subject', 'start_time', 'end_time', 'duration_minutes',
            'total_marks', 'passing_marks', 'negative_marking',
            'shuffle_questions', 'shuffle_options', 'attempt_limit',
            'password', 'instructions', 'is_published', 'max_violations'
        ]
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control glass-input', 'placeholder': 'e.g. Mid-Term C Programming Exam'}),
            'subject': forms.Select(attrs={'class': 'form-select glass-input'}),
            'start_time': forms.DateTimeInput(attrs={'class': 'form-control glass-input', 'type': 'datetime-local'}),
            'end_time': forms.DateTimeInput(attrs={'class': 'form-control glass-input', 'type': 'datetime-local'}),
            'duration_minutes': forms.NumberInput(attrs={'class': 'form-control glass-input', 'placeholder': '60'}),
            'total_marks': forms.NumberInput(attrs={'class': 'form-control glass-input', 'step': '1'}),
            'passing_marks': forms.NumberInput(attrs={'class': 'form-control glass-input', 'step': '1'}),
            'negative_marking': forms.NumberInput(attrs={'class': 'form-control glass-input', 'step': '0.25'}),
            'shuffle_questions': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'shuffle_options': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'attempt_limit': forms.NumberInput(attrs={'class': 'form-control glass-input'}),
            'password': forms.PasswordInput(attrs={'class': 'form-control glass-input', 'placeholder': 'Optional passcode'}),
            'instructions': forms.Textarea(attrs={'class': 'form-control glass-input', 'rows': 4}),
            'is_published': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'max_violations': forms.NumberInput(attrs={'class': 'form-control glass-input'}),
        }

class ExamEntryForm(forms.Form):
    password = forms.CharField(
        required=False,
        widget=forms.PasswordInput(attrs={'class': 'form-control glass-input', 'placeholder': 'Passcode (if protected)'})
    )

