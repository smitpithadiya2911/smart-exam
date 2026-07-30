from django import forms
from .models import Question

class QuestionForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if 'subject' in self.fields:
            self.fields['subject'].empty_label = "-- Select Subject --"

    class Meta:
        model = Question
        fields = [
            'subject', 'question_type', 'chapter', 'topic', 'marks', 'difficulty',
            'prompt_text', 'option_a', 'option_b', 'option_c', 'option_d',
            'correct_answer', 'explanation', 'image', 'tags'
        ]
        widgets = {
            'subject': forms.Select(attrs={'class': 'form-select glass-input'}),
            'question_type': forms.Select(attrs={'class': 'form-select glass-input'}),
            'chapter': forms.TextInput(attrs={'class': 'form-control glass-input', 'placeholder': 'e.g. Chapter 2 - Pointers'}),
            'topic': forms.TextInput(attrs={'class': 'form-control glass-input', 'placeholder': 'e.g. Dynamic Memory'}),
            'marks': forms.NumberInput(attrs={'class': 'form-control glass-input', 'step': '0.5', 'placeholder': '1'}),
            'difficulty': forms.Select(attrs={'class': 'form-select glass-input'}),
            'prompt_text': forms.Textarea(attrs={'class': 'form-control glass-input', 'rows': 4, 'placeholder': 'Type your question here...'}),
            'option_a': forms.TextInput(attrs={'class': 'form-control glass-input', 'placeholder': 'Option A'}),
            'option_b': forms.TextInput(attrs={'class': 'form-control glass-input', 'placeholder': 'Option B'}),
            'option_c': forms.TextInput(attrs={'class': 'form-control glass-input', 'placeholder': 'Option C'}),
            'option_d': forms.TextInput(attrs={'class': 'form-control glass-input', 'placeholder': 'Option D'}),
            'correct_answer': forms.TextInput(attrs={'class': 'form-control glass-input', 'placeholder': 'A / True / Exact answer'}),
            'explanation': forms.Textarea(attrs={'class': 'form-control glass-input', 'rows': 3, 'placeholder': 'Solution explanation...'}),
            'image': forms.FileInput(attrs={'class': 'form-control glass-input'}),
            'tags': forms.TextInput(attrs={'class': 'form-control glass-input', 'placeholder': 'arrays, pointers, easy'}),
        }

class QuestionExcelImportForm(forms.Form):
    excel_file = forms.FileField(widget=forms.FileInput(attrs={'class': 'form-control glass-input'}))
    subject = forms.ModelChoiceField(queryset=None, empty_label="-- Select Subject --", widget=forms.Select(attrs={'class': 'form-select glass-input'}))

    def __init__(self, *args, **kwargs):
        subjects = kwargs.pop('subjects', None)
        super().__init__(*args, **kwargs)
        if subjects is not None:
            self.fields['subject'].queryset = subjects
            self.fields['subject'].empty_label = "-- Select Subject --"

