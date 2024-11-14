
from . import views
from django.conf.urls.static import static  # Make sure this is correct
from django.conf import settings
from django.urls import path, include
app_name = 'userapp'

urlpatterns = [
    path('UserHomePage/', views.UserHomePage, name='UserHomePage'),
    path('module/<int:module_id>/', views.module_details, name='module_details'),
    path('start_training/<int:module_id>/', views.start_training, name='start_training'),
    path('dashboard/', views.user_dashboard, name='employee_dashboard'),
    path('profile/', views.user_profile, name='employee_profile'),
    path('viewmarks/',views.view_mark,name='view_marks'),
    path('my-progress-certificates/', views.my_progress_and_certificates, name='my_progress_and_certificates'),
    path('assessment_descriptions/',views.assessment_descriptions,name='assessment_descriptions')
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)