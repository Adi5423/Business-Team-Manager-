from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import logout
from django.http import JsonResponse

from .models import EmployeeProfile, Task


@login_required
def employee_list(request):
    priority = {'head': 1, 'manager': 2, 'employee': 3}
    profiles = EmployeeProfile.objects.exclude(role='admin').select_related('user')
    sorted_profiles = sorted(profiles, key=lambda p: priority.get(p.role, 99))
    for p in sorted_profiles:
        p.progress_offset = 100 - (p.progress or 0)
    return render(request, 'employee_list.html', {'profiles': sorted_profiles})


@login_required
def my_profile(request):
    profile, _ = EmployeeProfile.objects.get_or_create(user=request.user)
    return render(request, 'profile.html', {'profile': profile})


@login_required
def custom_logout(request):
    logout(request)
    return redirect('/login/')


@login_required
def assign_task(request):
    assigner = EmployeeProfile.objects.get(user=request.user)
    if assigner.role not in ('head', 'manager'):
        messages.error(request, "Permission denied.")
        return redirect('employee-list')

    if assigner.role == 'head':
        assignees = EmployeeProfile.objects.exclude(role='admin')
    else:
        assignees = EmployeeProfile.objects.exclude(role__in=('admin', 'head'))

    if request.method == 'POST':
        title = request.POST.get('title', '').strip()
        description = request.POST.get('description', '').strip()
        to_ids_str = request.POST.get('assigned_to', '')
        to_ids = [i for i in to_ids_str.split(',') if i.strip().isdigit()]

        if title and to_ids:
            employees = EmployeeProfile.objects.filter(id__in=to_ids)
            for emp in employees:
                Task.objects.create(
                    title=title,
                    description=description,
                    assigned_to=emp,
                    assigned_by=assigner
                )
            messages.success(request, f"Task assigned to {employees.count()} employee(s).")
        else:
            messages.error(request, "Title and at least one assignee are required.")

        return redirect('assign-task')

    return render(request, 'assign_task.html', {'employees': assignees})


@login_required
def edit_profile(request, user_id):
    target_profile = get_object_or_404(EmployeeProfile, user__id=user_id)
    current_profile = EmployeeProfile.objects.get(user=request.user)
    can_edit = False

    if current_profile.role in ('head', 'admin'):
        can_edit = True
    elif current_profile.role == 'manager' and target_profile.role == 'employee':
        can_edit = True

    if not can_edit:
        messages.error(request, "Permission denied.")
        return redirect('employee-list')

    if request.method == 'POST':
        try:
            new_prog = int(request.POST.get('progress', target_profile.progress))
        except ValueError:
            new_prog = target_profile.progress
        target_profile.progress = min(new_prog, 100)
        target_profile.save()
        messages.success(request, "Profile updated.")
        return redirect('employee-list')

    return render(request, 'profile.html', {'profile': target_profile, 'editing_other': True})


@login_required
def report_task(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    profile = EmployeeProfile.objects.get(user=request.user)
    if task.assigned_to != profile:
        messages.error(request, "You can only report your own tasks.")
        return redirect('employee-list')

    if request.method == 'POST':
        status = request.POST.get('status', task.status)
        progress = min(int(request.POST.get('progress', task.progress)), 100)
        report = request.POST.get('report', task.review)
        task.status = status
        task.progress = progress
        task.review = report
        task.save()
        messages.success(request, "Task updated.")
        return redirect('my-profile')

    return render(request, 'report_task.html', {'task': task})


@login_required
def get_user_tasks(request, user_id):
    profile = get_object_or_404(EmployeeProfile, id=user_id)
    if request.user != profile.user and request.user.employeeprofile.role not in ("head", "manager", "admin"):
        return JsonResponse({"error": "Permission denied"}, status=403)

    tasks = Task.objects.filter(assigned_to=profile).select_related("assigned_by")
    task_list = [
        {
            "title": task.title,
            "status": task.status,
            "progress": task.progress,
            "assigned_by": task.assigned_by.user.username if task.assigned_by else "N/A",
            "created_at": task.created_at.strftime("%Y-%m-%d %H:%M")
        }
        for task in tasks
    ]
    return JsonResponse({"tasks": task_list})
