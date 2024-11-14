# employeeapp/forms.py
from django import forms
from .models import UserProfile

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['employee_name', 'department', 'position', 'contact_number', 'email', 'biography', 'photo']
