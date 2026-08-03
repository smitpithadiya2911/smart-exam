from django import forms
from .models import StudyMaterial

class StudyMaterialForm(forms.ModelForm):
    class Meta:
        model = StudyMaterial
        fields = [
            'title', 'description', 'subject', 'course', 'semester', 'department',
            'file', 'thumbnail', 'material_type', 'visibility'
        ]
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control glass-input', 'placeholder': 'Enter material title'}),
            'description': forms.Textarea(attrs={'class': 'form-control glass-input', 'rows': 4, 'placeholder': 'Describe the material...'}),
            'subject': forms.Select(attrs={'class': 'form-select glass-input'}),
            'course': forms.Select(attrs={'class': 'form-select glass-input'}),
            'semester': forms.Select(attrs={'class': 'form-select glass-input'}),
            'department': forms.Select(attrs={'class': 'form-select glass-input'}),
            'material_type': forms.Select(attrs={'class': 'form-select glass-input'}),
            'visibility': forms.Select(attrs={'class': 'form-select glass-input'}),
            'file': forms.ClearableFileInput(attrs={'class': 'form-control glass-input'}),
            'thumbnail': forms.ClearableFileInput(attrs={'class': 'form-control glass-input'}),
        }

    def clean_file(self):
        file = self.cleaned_data.get('file', False)
        if file:
            if file.size > 50 * 1024 * 1024: # 50MB limit
                raise forms.ValidationError("File size must be under 50MB.")
        return file
