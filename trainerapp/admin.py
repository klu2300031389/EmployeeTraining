from django.contrib import admin

# Register your models here.
from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import FAQ, Module, TrainingSchedule

admin.site.register(FAQ)
admin.site.register(Module)
admin.site.register(TrainingSchedule)
