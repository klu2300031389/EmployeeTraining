from django.contrib.auth import authenticate, login, logout as auth_logout
def ensure_groups_exist():
    Group.objects.get_or_create(name='Admin')
    Group.objects.get_or_create(name='Employee')
    Group.objects.get_or_create(name='User')
from adminapp.models import Course, Subscription
def homepage(request):
    return render(request, 'adminapp/homepage.html')
def projecthomepage(request):
    courses = Course.objects.all()
    if request.user.is_authenticated:
        user_subscriptions = Subscription.objects.filter(user=request.user)
    else:
        user_subscriptions = []
    users = User.objects.all()
    return render(request, 'adminapp/ProjectHomePage.html', {
        'courses': courses,
        'user_subscriptions': user_subscriptions,
        'users': users
    })
def add_user(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = User.objects.create_user(username=username, email=email, password=password)
        roles = request.POST.getlist('roles')
        for role in roles:
            group, created = Group.objects.get_or_create(name=role)
            user.groups.add(group)
        messages.success(request, "User added successfully!")
        return redirect('adminapp:user_list')
    return render(request, 'adminapp/add_user.html')
def user_list(request):
    users = User.objects.all()
    user_data = []
    for user in users:
        roles = ', '.join([group.name for group in user.groups.all()])
        user_data.append({
            'user': user,
            'is_admin': user.is_staff,
            'roles': roles
        })
    return render(request, 'adminapp/user_list.html', {'user_data': user_data})
from django.contrib.auth.models import User, Group
from .forms import UserForm, ModuleForm, QuestionForm, CertificateForm
def edit_user(request, user_id):
    user = get_object_or_404(User, id=user_id)
    if request.method == 'POST':
        form = UserForm(request.POST, instance=user)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_staff = 'is_staff' in request.POST
            user.save()
            user.groups.clear()
            roles = request.POST.getlist('role')
            for role in roles:
                try:
                    group = Group.objects.get(name=role)
                    group.user_set.add(user)
                except Group.DoesNotExist:
                    messages.error(request, f"Group '{role}' does not exist. Please check the role name.")
            messages.success(request, "User updated successfully.")
            return redirect('adminapp:user_list')
    else:
        form = UserForm(instance=user)
    user_roles = user.groups.values_list('name', flat=True)
    return render(request, 'adminapp/edit_user.html', {
        'form': form,
        'user': user,
        'user_roles': user_roles
    })
def delete_user(request, user_id):
    user = get_object_or_404(User, id=user_id)
    if request.method == 'POST':
        try:
            with transaction.atomic():
                user.delete()
            messages.success(request, "User deleted successfully.")
            return redirect('adminapp:user_list')
        except OperationalError:
            messages.error(request, "Error deleting user. Please try again later.")
    return render(request, 'adminapp/delete_user.html', {'user': user})
def UserRegisterPageCall(request):
    return render(request, 'adminapp/UserRegisterPage.html')
def UserRegisterLogic(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        pass1 = request.POST.get('password')
        pass2 = request.POST.get('password1')
        print(f"Username: {username}, Email: {email}")
        if pass1 == pass2:
            if User.objects.filter(username=username).exists():
                messages.info(request, 'OOPS! Username already taken.')
                return render(request, 'adminapp/UserRegisterPage.html')
            elif User.objects.filter(email=email).exists():
                messages.info(request, 'OOPS! Email already registered.')
                return render(request, 'adminapp/UserRegisterPage.html')
            else:
                try:
                    user = User.objects.create_user(
                        username=username,
                        password=pass1,
                        first_name=first_name,
                        last_name=last_name,
                        email=email
                    )
                    user.save()
                    messages.info(request, 'Account created Successfully!')
                    return render(request, 'adminapp/homepage.html')
                except Exception as e:
                    print(f"Error saving user: {e}")  # Debugging error output
                    messages.info(request, 'Error creating account.')
                    return render(request, 'adminapp/UserRegisterPage.html')
        else:
            messages.info(request, 'Passwords do not match.')
            return render(request, 'adminapp/UserRegisterPage.html')
    else:
        return render(request, 'adminapp/UserRegister.html')
def UserLoginPageCall(request):
    return render(request, 'adminapp/UserLoginPage.html')
def UserLoginLogic(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            if len(username) == 10:
                messages.success(request, 'Login successful as student!')
                return redirect('userapp:UserHomePage')
            elif len(username) == 4:
                return redirect('trainerapp:TrainerHomePage')
            elif len(username) == 3:
                return redirect('adminapp:projecthomepage')
            else:
                messages.error(request, 'Username does not match any role criteria.')
        else:
            messages.error(request, 'Invalid username or password.')
    return render(request, 'adminapp/UserLoginPage.html')
def logout(request):
    auth_logout(request)
    return redirect('adminapp:homepage')
from .models import  EmployeeResult
from django.contrib.auth.decorators import login_required
from .forms import CourseForm
@login_required
def add_course(request):
    if request.method == 'POST':
        form = CourseForm(request.POST)
        if form.is_valid():
            course = form.save(commit=False)
            course.created_by = request.user
            course.save()
            messages.success(request, "Course added successfully!")
            return redirect('adminapp:course_list')
        else:
            messages.error(request, "There was an error with your submission.")
    else:
        form = CourseForm()
    return render(request, 'adminapp/course_form.html', {'form': form})
def course_list(request):
    courses = Course.objects.all()
    return render(request, 'adminapp/course_list.html', {'courses': courses})
def edit_course(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    if request.method == 'POST':
        form = CourseForm(request.POST, instance=course)
        if form.is_valid():
            form.save()
            messages.success(request, "Course updated successfully.")
            return redirect('adminapp:course_list')
        else:
            messages.error(request, "There was an error updating the course.")
            print(form.errors)
    else:
        form = CourseForm(instance=course)
    return render(request, 'adminapp/course_form.html', {
        'form': form,
        'course': course
    })
from django.db import transaction, OperationalError
def delete_course(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    if request.method == 'POST':
        try:
            with transaction.atomic():
                course.delete()
            messages.success(request, "Course deleted successfully.")
            return redirect('adminapp:course_list')
        except OperationalError:
            messages.error(request, "Error deleting course. Please try again later.")
    return render(request, 'adminapp/delete_course.html', {'course': course})
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
class CustomLoginView(LoginView):
    template_name = 'custom_login_template.html'
    success_url = reverse_lazy('some_success_url')
def track_progress(request):
    users = User.objects.all()
    courses = Course.objects.all()
    if request.method == 'POST':
        user_id = request.POST.get('user')
        course_id = request.POST.get('course')
        progress_percentage = request.POST.get('progress_percentage')
        completion_date = request.POST.get('completion_date')
        progress = Progress(
            user_id=user_id,
            course_id=course_id,
            progress_percentage=progress_percentage,
            completion_date=completion_date
        )
        progress.save()
        return redirect('adminapp:track_progress')
    progress_reports = Progress.objects.all()
    context = {
        'users': users,
        'courses': courses,
        'progress_reports': progress_reports,
    }
    return render(request, 'adminapp/track_progress.html', context)
def edit_progress(request, progress_id):
    progress = get_object_or_404(Progress, id=progress_id)
    users = User.objects.all()
    courses = Course.objects.all()
    if request.method == 'POST':
        progress.user_id = request.POST.get('user')
        progress.course_id = request.POST.get('course')
        progress.progress_percentage = request.POST.get('progress_percentage')
        progress.completion_date = request.POST.get('completion_date')
        progress.save()
        return redirect('adminapp:track_progress')
    context = {
        'progress': progress,
        'users': users,
        'courses': courses,
    }
    return render(request, 'adminapp/edit_progress.html', context)
def delete_progress(request, progress_id):
    progress = get_object_or_404(Progress, id=progress_id)
    if request.method == 'POST':
        progress.delete()
        return redirect('adminapp:track_progress')
    context = {
        'progress': progress,
    }
    return render(request, 'adminapp/delete_progress.html', context)
def issue_certificate(request):
    if request.method == "POST":
        form = CertificateForm(request.POST)
        if form.is_valid():
            certificate = form.save()
            return redirect('adminapp:generate_certificate', progress_id=certificate.progress.id)
    else:
        form = CertificateForm()
    return render(request, 'adminapp/issue_certificate.html', {'form': form})
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet
from .models import Progress
def generate_certificate(request, progress_id):
    progress = get_object_or_404(Progress, id=progress_id)
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="certificate_{progress.user.username}_{progress.course.title}.pdf"'
    doc = SimpleDocTemplate(response, pagesize=letter)
    content = []
    logo = Image('media/logo/img.png', width=2 * inch, height=1 * inch)
    logo.hAlign = 'CENTER'
    content.append(logo)
    content.append(Spacer(1, 0.5 * inch))
    styles = getSampleStyleSheet()
    title = Paragraph("Certificate of Completion", styles['Title'])
    content.append(title)
    content.append(Spacer(1, 0.5 * inch))
    certifying_statement = Paragraph("This certifies that", styles['Normal'])
    content.append(certifying_statement)
    content.append(Spacer(1, 0.2 * inch))
    user_name = Paragraph(f"<b>{progress.user.username}</b>", styles['Heading1'])
    content.append(user_name)
    content.append(Spacer(1, 0.5 * inch))
    course_completion = Paragraph("has completed the course", styles['Normal'])
    content.append(course_completion)
    content.append(Spacer(1, 0.2 * inch))
    course_title = Paragraph(f"<b>{progress.course.title}</b>", styles['Heading1'])
    content.append(course_title)
    content.append(Spacer(1, 0.5 * inch))
    progress_statement = Paragraph(f"with a progress of <b>{progress.progress_percentage} %</b>.", styles['Normal'])
    content.append(progress_statement)
    content.append(Spacer(1, 0.5 * inch))
    issued_date = Paragraph(f"Issued on: {progress.completion_date.strftime('%B %d, %Y')}", styles['Normal'])
    content.append(issued_date)
    p = canvas.Canvas(response, pagesize=letter)
    p.setStrokeColor(colors.black)
    p.setLineWidth(5)
    p.rect(30, 30, 550, 730, fill=0)
    p.save()
    doc.build(content)
    return response
from django.contrib.auth.decorators import login_required
@login_required
def add_assessment(request):
    if request.method == 'POST':
        form = AssessmentForm(request.POST)
        if form.is_valid():
            assessment = form.save(commit=False)
            assessment.created_by = request.user
            assessment.save()
            messages.success(request, "Assessment added successfully!")
            return redirect('adminapp:assessment_list')
        else:
            messages.error(request, "There was an error with your submission.")
    else:
        form = AssessmentForm()
    return render(request, 'adminapp/assessment_form.html', {'form': form})
from .forms import AssessmentForm
from .models import Assessment
def edit_assessment(request, assessment_id):
    assessment = get_object_or_404(Assessment, id=assessment_id)
    if request.method == 'POST':
        form = AssessmentForm(request.POST, instance=assessment)
        if form.is_valid():
            updated_assessment = form.save(commit=False)
            updated_assessment.created_by = request.user
            updated_assessment.save()
            messages.success(request, "Assessment updated successfully.")
            return redirect('adminapp:dashboard')
        else:
            messages.error(request, "There was an error updating the assessment.")
            print(form.errors)
    else:
        form = AssessmentForm(instance=assessment)
    return render(request, 'adminapp/assessment_form.html', {
        'form': form,
        'assessment': assessment
    })
def assessment_list(request):
    assessments = Assessment.objects.all()
    return render(request, 'adminapp/assessment_list.html', {'assessments': assessments})
def delete_assessment(request, assessment_id):
    assessment = get_object_or_404(Assessment, id=assessment_id)
    if request.method == 'POST':
        try:
            assessment.delete()
            messages.success(request, "Assessment deleted successfully.")
            return redirect('adminapp:dashboard')
        except OperationalError:
            messages.error(request, "Error deleting assessment. Please try again later.")
    return render(request, 'adminapp/delete_assessment.html', {'assessment': assessment})
@login_required
def create_question(request):
    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('adminapp:dashboard')
    else:
        form = QuestionForm()
    return render(request, 'adminapp/create_question.html', {'form': form})
@login_required
def view_results(request):
    results = EmployeeResult.objects.all()
    return render(request, 'adminapp/view_results.html', {'results': results})
@login_required
def dashboard(request):
    assessments = Assessment.objects.all()
    return render(request, 'adminapp/dashboard.html', {'assessments': assessments})
from .forms import PasswordResetForm
def reset_password(request):
    if request.method == 'POST':
        form = PasswordResetForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Password has been reset successfully!')
            return redirect('adminapp:login')
    else:
        form = PasswordResetForm()
    return render(request, 'adminapp/reset_password.html', {'form': form})
from django.views.generic import TemplateView
class CustomLoginView(TemplateView):
    template_name = 'adminapp/custom_login_template.html'
def search_users(request):
    query = request.GET.get('q')
    results = []
    if query:
        results = User.objects.filter(username__icontains=query) | User.objects.filter(
            email__icontains=query) | User.objects.filter(first_name__icontains=query)
    context = {'results': results, 'query': query}
    return render(request, 'adminapp/search_users.html', context)
def search_course(request):
    query = request.GET.get('query', '')
    courses = Course.objects.filter(title__icontains=query)
    context = {
        'courses': courses,
        'query': query,
    }
    return render(request, 'adminapp/search_courses.html', context)
def export_users_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="users.csv"'
    writer = csv.writer(response)
    writer.writerow(['Username', 'Email', 'First Name', 'Last Name'])
    for user in User.objects.all():
        writer.writerow([user.username, user.email, user.first_name, user.last_name])
    return response
def export_users_excel(request):
    workbook = Workbook()
    worksheet = workbook.active
    worksheet.title = 'Users'
    worksheet.append(['Username', 'Email', 'First Name', 'Last Name'])
    for user in User.objects.all():
        worksheet.append([user.username, user.email, user.first_name, user.last_name])
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename="users.xlsx"'
    workbook.save(response)
    return response
from openpyxl import Workbook
import csv
import pandas as pd
from django.http import HttpResponse
def export_courses_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="courses.csv"'
    writer = csv.writer(response)
    writer.writerow(['Title', 'Description', 'Category', 'Prerequisites', 'Start Date', 'End Date', 'Is Active', 'Created By'])
    for course in Course.objects.all():
        writer.writerow([
            course.title,
            course.description,
            course.category.name,
            course.prerequisites,
            course.start_date,
            course.end_date,
            course.is_active,
            course.created_by.username,
        ])
    return response
def export_courses_excel(request):
    courses = Course.objects.all().values(
        'title',
        'description',
        'category__name',
        'prerequisites',
        'start_date',
        'end_date',
        'is_active',
        'created_by__username'
    )
    df = pd.DataFrame(list(courses))
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename="courses.xlsx"'
    with pd.ExcelWriter(response, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='Courses')
    return response
from django.contrib.auth.decorators import login_required
from .models import UserActivity
@login_required
def user_activity_list(request):
    activities = UserActivity.objects.all().order_by('-timestamp')
    return render(request, 'adminapp/user_activity_list.html', {'activities': activities})
from django.contrib.auth import get_user_model
User = get_user_model()
from django.shortcuts import get_object_or_404, redirect
def toggle_user_status(request, user_id):
    user = get_object_or_404(User, id=user_id)
    user.is_active = not user.is_active
    user.save()
    if user.is_active:
        messages.success(request, f'{user.username} has been reactivated.')
    else:
        messages.success(request, f'{user.username} has been suspended.')
    return redirect('adminapp:projecthomepage')
def users_list(request):
    users = User.objects.all()
    return render(request, 'adminapp/users_list.html', {'users': users})
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from .models import Course, UserCourse
def assign_course(request):
    if request.method == 'POST':
        user_id = request.POST.get('user')
        course_id = request.POST.get('course')
        user = User.objects.get(id=user_id)
        course = Course.objects.get(id=course_id)
        UserCourse.objects.get_or_create(user=user, course=course)
        messages.success(request, f'Successfully assigned {course.title} to {user.username}.')
        return redirect('adminapp:assign_course')
    users = User.objects.all()
    courses = Course.objects.filter(is_active=True)
    users_with_courses = User.objects.prefetch_related('usercourse_set').all()
    return render(request, 'adminapp/assign_courses.html', {
        'users': users,
        'courses': courses,
        'users_with_courses': users_with_courses,
    })
def assigned_courses(request):
    users_with_courses = User.objects.prefetch_related('usercourse_set').all()
    return render(request, 'adminapp/assigned_courses.html', {'users_with_courses': users_with_courses})