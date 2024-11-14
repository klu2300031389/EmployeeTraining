from django.contrib.auth.decorators import login_required
from django.shortcuts import render

def UserHomePage(request):
    return render(request,  'userapp/UserHomePage.html')
def module_details(request, module_id):
    return render(request, 'userapp/module_details.html', {'module_id': module_id})
def start_training(request, module_id):
    return render(request, 'userapp/start_training.html', {'module_id': module_id})
from django.shortcuts import render, redirect, get_object_or_404
from .models import UserProfile
from .forms import UserProfileForm
@login_required
def user_profile(request):
    try:
        employee_profile = UserProfile.objects.get(user=request.user)
    except UserProfile.DoesNotExist:
        employee_profile = None
        if request.method == 'POST':
            form = UserProfileForm(request.POST, request.FILES, instance=employee_profile)
        else:
            form = UserProfileForm(request.POST, request.FILES)

        if form.is_valid():
            profile = form.save(commit=False)
            profile.user = request.user
            profile.save()
            return redirect('userapp:employee_dashboard')
    else:
        form = UserProfileForm(instance=employee_profile)

    return render(request, 'userapp/profile.html', {'form': form})

def user_dashboard(request):
    if not request.user.is_authenticated:
        return redirect('login')

    try:
        employee_profile = UserProfile.objects.get(user=request.user)
    except UserProfile.DoesNotExist:
        return redirect('userapp:employee_profile')  # Redirect to profile creation if not found

    context = {
        'employee_profile': employee_profile,
    }
    return render(request, 'userapp/dashboard.html', context)

# In your view function to display marks
from adminapp.models import Marks

def view_mark(request):
    user = request.user
    marks = Marks.objects.filter(student=user).select_related('course')
    return render(request, 'userapp/view_marks.html', {'marks': marks})


from django.shortcuts import render
from adminapp.models import Progress, Certificate


def my_progress_and_certificates(request):
    # Get the logged-in user
    user = request.user

    # Retrieve the progress records for this user
    progress_records = Progress.objects.filter(user=user)

    # Retrieve the certificates for this user
    certificates = Certificate.objects.filter(user=user)

    context = {
        'progress_records': progress_records,
        'certificates': certificates,
    }
    return render(request, 'userapp/my_progress_and_certificates.html', context)
from django.shortcuts import render
from adminapp.models import Assessment

def assessment_descriptions(request):
    # Retrieve all assessments along with the course title and description
    assessments = Assessment.objects.select_related('cou'
                                                    'rse').values('description', 'course__title')
    return render(request, 'userapp/assessment_descriptions.html', {'assessments': assessments})