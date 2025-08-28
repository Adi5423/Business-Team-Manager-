from django.contrib import admin
from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from django.conf import settings
from django.conf.urls.static import static

from department.views import (
    employee_list,
    my_profile,
    assign_task,
    edit_profile,
    report_task,
)

urlpatterns = [
    path('admin/', admin.site.urls),

    # Auth
    path('login/', LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),

    # App routes
    path('', employee_list, name='employee-list'),
    path('profile/', my_profile, name='my-profile'),
    path('assign/', assign_task, name='assign-task'),
    path('profile/<int:user_id>/edit/', edit_profile, name='edit-profile'),
    path('task/<int:task_id>/report/', report_task, name='report-task'),
]

# Serve media in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
