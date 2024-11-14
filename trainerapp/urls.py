
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views

app_name='trainerapp'
urlpatterns = [
   path('TrainerHomePage/',views.TrainerHomePage,name="TrainerHomePage"),
   path('chatbot/', views.chatbot, name='chatbot'),
   path('login/', views.custom_login, name='custom_login'),
   path('profile/', views.trainer_profile, name='trainer_profile'),
   path('dashboard/', views.trainer_dashboard, name='trainer_dashboard'),
   path('trainerapp/trainer_profile/', views.trainer_profile, name='trainer_profile'),
   path('user_list/', views.user_list, name='user_list'),
   path('add_user/', views.add_user, name='add_user'),
   path('users/edit/<int:user_id>/', views.edit_user, name='edit_user'),
    path('users/delete/<int:user_id>/', views.delete_user, name='delete_user'),
    path('course_list/',views.course_list,name='course_list'),
    path('courses/add/', views.add_course, name='add_course'),
    path('courses/edit/<int:course_id>/', views.edit_course, name='edit_course'),
    path('courses/delete/<int:course_id>/', views.delete_course, name='delete_course'),
    path('assign_courses/', views.assign_course, name='assign_course'),
    path('assessments/', views.assessment_list, name='assessment_list'),
    path('assessments/add/', views.add_assessment, name='add_assessment'),
    path('assessments/edit/<int:assessment_id>/', views.edit_assessment, name='edit_assessment'),
    path('assessments/delete/<int:assessment_id>/', views.delete_assessment, name='delete_assessment'),
    path('results/', views.view_results, name='view_results'),
    path('assignment_dashboard/',views.assignment_dashboard,name='assignment_dashboard'),
    path('postmarks/',views.post_marks,name='post_marks'),
    path('edit_marks/<int:mark_id>/', views.edit_marks, name='edit_marks'),
    path('delete_marks/<int:mark_id>/', views.delete_marks, name='delete_marks'),
    path('track_progress/', views.track_progress, name='track_progress'),
    path('track_progress/edit/<int:progress_id>/', views.edit_progress, name='edit_progress'),
    path('track_progress/delete/<int:progress_id>/', views.delete_progress, name='delete_progress'),
    path('issue-certificate/', views.issue_certificate, name='issue_certificate'),
    path('generate-certificate/<int:progress_id>/', views.generate_certificate, name='generate_certificate'),

]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)