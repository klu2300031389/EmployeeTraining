from django.db import models
from django.contrib.auth.models import User
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=20)
    def __str__(self):
        return self.user.username
class Task(models.Model):
    title = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.title
class StudentList(models.Model):
    register_number = models.CharField(max_length=20, unique=True)
    name = models.CharField(max_length=100)
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    def __str__(self):
        return self.register_number
class Category(models.Model):
    name = models.CharField(max_length=100)
    def __str__(self):
        return self.name
class Course(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    prerequisites = models.TextField(null=True, blank=True)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    def __str__(self):
        return self.title
class Module(models.Model):
    course = models.ForeignKey(Course, related_name='modules', on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    content = models.TextField()
    duration = models.IntegerField(help_text="Duration in minutes")
    def __str__(self):
        return self.title
class Employee(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    def __str__(self):
        return self.user.username
class Progress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    progress_percentage = models.FloatField(default=0.0)
    completion_date = models.DateField(null=True, blank=True)
    def __str__(self):
        return f"{self.user.username} - {self.course.title} ({self.progress_percentage}%)"
from django.db import models
class Certificate(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    progress = models.ForeignKey(Progress, on_delete=models.CASCADE)
    issued_date = models.DateField(auto_now_add=True)
    def __str__(self):
        return f"Certificate for {self.user.username} - {self.course.title}"
from django.db import models
from django.contrib.auth.models import User
class Assessment(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    def __str__(self):
        return self.title
class Question(models.Model):
    text = models.CharField(max_length=500)
    assessment = models.ForeignKey(Assessment, related_name='questions', on_delete=models.CASCADE)
    def __str__(self):
        return self.text
from django.contrib.auth.models import User
from django.db import models
from .models import Assessment
class EmployeeResult(models.Model):
    employee = models.ForeignKey(User, on_delete=models.CASCADE)  # Link to User model
    assessment = models.ForeignKey(Assessment, on_delete=models.CASCADE)
    score = models.DecimalField(max_digits=5, decimal_places=2
    def __str__(self):
        return f'{self.employee.username} - {self.assessment.title} - {self.score}'
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
class UserActivity(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    activity_type = models.CharField(max_length=255)
    timestamp = models.DateTimeField(default=timezone.now)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.CharField(max_length=255, null=True, blank=True)
    path = models.CharField(max_length=255)
    extra_data = models.TextField(null=True, blank=True)  # Optional metadata
    def __str__(self):
        return f"{self.user.username} - {self.activity_type} at {self.timestamp}"
from django.db import models
from django.contrib.auth.models import User
class Subscription(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    date_subscribed = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"{self.user.username} subscribed to {self.course.title}"
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models
class CustomUser(AbstractUser):
    is_active = models.BooleanField(default=True)
    groups = models.ManyToManyField(
        Group,
        related_name='customuser_set',
        blank=True,
        help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.'
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name='customuser_set',
        blank=True,
        help_text='Specific permissions for this user.'
    )
class UserCourse(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    enrollment_date = models.DateTimeField(auto_now_add=True)
    completed = models.BooleanField(default=False)
    def __str__(self):
        return f"{self.user.username} - {self.course.title}"
class Marks(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    marks = models.IntegerField()
    def __str__(self):
        return f"{self.student.username} - {self.course.title} - Marks: {self.marks}"