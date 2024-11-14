# signals.py

from django.contrib.auth.signals import user_logged_in, user_logged_out
from django.dispatch import receiver
from .models import UserActivity

@receiver(user_logged_in)
def log_user_login(sender, request, user, **kwargs):
    UserActivity.objects.create(
        user=user,
        activity_type='Login',
        ip_address=get_client_ip(request),
        user_agent=request.META.get('HTTP_USER_AGENT', ''),
        path=request.path,
    )

@receiver(user_logged_out)
def log_user_logout(sender, request, user, **kwargs):
    UserActivity.objects.create(
        user=user,
        activity_type='Logout',
        ip_address=get_client_ip(request),
        user_agent=request.META.get('HTTP_USER_AGENT', ''),
        path=request.path,
    )

def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


# signals.py (continued)

from django.db.models.signals import post_save, post_delete
from .models import Course  # Assuming you have a Course model
from .models import UserActivity


@receiver(post_save, sender=Course)
def log_course_change(sender, instance, created, **kwargs):
    activity_type = 'Course Created' if created else 'Course Updated'

    UserActivity.objects.create(
        user=instance.created_by,
        activity_type=activity_type,
        path=f'/course/{instance.id}/',
        extra_data=f'Course title: {instance.title}'
    )


@receiver(post_delete, sender=Course)
def log_course_deletion(sender, instance, **kwargs):
    UserActivity.objects.create(
        user=instance.created_by,
        activity_type='Course Deleted',
        path=f'/course/{instance.id}/',
        extra_data=f'Course title: {instance.title}'
    )
