from django.db import models
from adminapp.models import Employee  # Assuming Employee is in adminapp
from django.contrib.auth.models import Group  

class FAQ(models.Model):
    question = models.CharField(max_length=255)
    answer = models.TextField()
    role = models.ForeignKey(Group, on_delete=models.CASCADE, null=True, blank=True, help_text="The role for which this FAQ is relevant.")

    def __str__(self):
        return self.question


class Module(models.Model):
    """
    Model to represent training modules that employees will take.
    """
    name = models.CharField(max_length=255)
    description = models.TextField()

    def __str__(self):
        return self.name


class TrainingSchedule(models.Model):
    """
    Model to represent the training schedule of an employee.
    Links employees to the modules they are scheduled to take.
    """
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    module = models.ForeignKey(Module, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()

    def __str__(self):
        return f'{self.employee.name} - {self.module.name} ({self.start_date} to {self.end_date})'
# trainerapp/models.py

from django.db import models
from django.contrib.auth.models import User

class TrainerProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    trainer_name = models.CharField(max_length=100)
    department = models.CharField(max_length=100)
    salary = models.DecimalField(max_digits=10, decimal_places=2)
    contact_number = models.CharField(max_length=15, blank=True, null=True)
    email = models.EmailField()
    date_joined = models.DateField(auto_now_add=True)
    biography = models.TextField(blank=True, null=True)
    photo = models.ImageField(upload_to='trainer_photos/', blank=True, null=True)  # The photo field

    def __str__(self):
        return self.trainer_name
