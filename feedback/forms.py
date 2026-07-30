from django import forms
from .models import Feedback

class FeedbackForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if 'exam' in self.fields:
            self.fields['exam'].empty_label = "-- Select Exam (Optional) --"
        if 'feedback_type' in self.fields:
            self.fields['feedback_type'].choices = [('', '-- Select Feedback Type --')] + list(self.fields['feedback_type'].choices)[1:]

    class Meta:
        model = Feedback
        fields = ['feedback_type', 'exam', 'rating', 'comments']
        widgets = {
            'feedback_type': forms.Select(attrs={'class': 'form-select glass-input'}),
            'exam': forms.Select(attrs={'class': 'form-select glass-input'}),
            'rating': forms.NumberInput(attrs={'class': 'form-control glass-input', 'min': 1, 'max': 5, 'placeholder': 'Rate 1 to 5 stars'}),
            'comments': forms.Textarea(attrs={'class': 'form-control glass-input', 'rows': 4, 'placeholder': 'Share your experience or suggestions...'}),
        }

