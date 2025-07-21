"""
URL configuration for business_manager project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views
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
    path('login/',  auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'),   name='logout'),

    # Core pages
    path('',           employee_list, name='employee-list'),
    path('profile/',   my_profile,    name='my-profile'),
    path('assign/',    assign_task,   name='assign-task'),
    path('profile/<int:user_id>/', edit_profile, name='edit-profile'),
    path('task/<int:task_id>/report/', report_task, name='report-task'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
