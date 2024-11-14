from django import forms

class ChatbotForm(forms.Form):
    query = forms.CharField(label='Ask the chatbot', max_length=255)
# trainerapp/forms.py

from django import forms
from .models import TrainerProfile

class TrainerProfileForm(forms.ModelForm):
    class Meta:
        model = TrainerProfile
        fields = ['trainer_name', 'department', 'salary', 'contact_number', 'email', 'biography', 'photo']
