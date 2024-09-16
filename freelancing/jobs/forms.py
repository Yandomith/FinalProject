from django import forms
from .models import Job,Message

class JobForm(forms.ModelForm):
    class Meta:
        model = Job
        fields = ['title', 'budget', 'description', 'requirement','expertise_required']
        labels = {
            'title': 'Give your project brief a title',
            'budget':"I'm looking to spend Rs.......",
            'description':"What are you looking to get done?"
        }

class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['body']
        widgets = {
            'body': forms.Textarea(attrs={'placeholder': 'Enter your message...'}),
        }