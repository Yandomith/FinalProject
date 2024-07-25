from django import forms
from .models import Job

class JobForm(forms.ModelForm):
    class Meta:
        model = Job
        fields = ['title', 'budget', 'description', 'requirement','expertise_required']
        labels = {
            'title': 'Give your project brief a title',
            'budget':"I'm looking to spend...",
            'description':"What are you looking to get done?"


        }
