from django import forms
from django.contrib.auth.models import User
from .models import Course, Module, Category
class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'is_staff']
    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)
        self.fields['is_staff'].label = 'Is Admin (Staff)'
class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['title', 'category', 'description', 'start_date', 'end_date']
    def __init__(self, *args, **kwargs):
        super(CourseForm, self).__init__(*args, **kwargs)
        self.fields['category'].queryset = Category.objects.all()
class ModuleForm(forms.ModelForm):
    class Meta:
        model = Module
        fields = ['course', 'title', 'content', 'duration']
from django import forms
from .models import Progress
class ProgressForm(forms.ModelForm):
    class Meta:
        model = Progress
        fields = ['user', 'course', 'progress_percentage', 'completion_date']
        widgets = {
            'completion_date': forms.DateInput(attrs={'type': 'date'}),
        }
from django import forms
from .models import Certificate, Progress
class CertificateForm(forms.ModelForm):
    class Meta:
        model = Certificate
        fields = ['user', 'course', 'progress']
        widgets = {
            'user': forms.Select(attrs={'class': 'form-control'}),
            'course': forms.Select(attrs={'class': 'form-control'}),
            'progress': forms.Select(attrs={'class': 'form-control'}),
        }

from django import forms
from .models import Assessment, Question
class AssessmentForm(forms.ModelForm):
    class Meta:
        model = Assessment
        fields = ['title', 'description', 'course']
class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['text', 'assessment']
from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
class PasswordResetForm(forms.Form):
    user = forms.ModelChoiceField(queryset=User.objects.all(), label="User")
    new_password = forms.CharField(widget=forms.PasswordInput, label="New Password")
    confirm_password = forms.CharField(widget=forms.PasswordInput, label="Confirm Password")
    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("new_password")
        confirm_password = cleaned_data.get("confirm_password")
        if password != confirm_password:
            raise ValidationError("Passwords do not match")
        return cleaned_data
    def save(self):
        user = self.cleaned_data["user"]
        new_password = self.cleaned_data["new_password"]
        user.set_password(new_password)
        user.save()
class CourseSearchForm(forms.Form):
    query = forms.CharField(label='Search Courses', max_length=100)
from adminapp.models import Marks
class MarksForm(forms.ModelForm):
    class Meta:
        model = Marks
        fields = ['student', 'course', 'marks']