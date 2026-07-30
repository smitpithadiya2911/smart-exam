from django import forms

class AnnouncementForm(forms.Form):
    title = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control glass-input', 'placeholder': 'Announcement Title'}))
    message = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control glass-input', 'rows': 4, 'placeholder': 'Broadcast message to all users...'}))
