from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages

from .models import EmployeeProfile, Task

# Create your views here.
@login_required
def employee_list(request):
    """
    Show all non-admin employees, ordered: Head → Manager → Employee
    """
    priority = {'head': 1, 'manager': 2, 'employee': 3}
    profiles = (
        EmployeeProfile.objects
        .exclude(role='admin')
        .select_related('user')
    )
    sorted_profiles = sorted(
        profiles,
        key=lambda p: priority.get(p.role, 99)
    )
    for p in sorted_profiles:
        p.progress_offset = 100 - (p.progress or 0)
    return render(request, 'employee_list.html', {'profiles': sorted_profiles})


@login_required
def my_profile(request):
    """
    Show & edit the logged-in user's own profile.
    Enforce progress <= 100 via min().
    """
    profile, _ = EmployeeProfile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        # Only progress is editable (others managed by Head/Manager)
        try:
            new_prog = int(request.POST.get('progress', profile.progress))
        except ValueError:
            new_prog = profile.progress

        profile.progress = min(new_prog, 100)
        profile.save()
        messages.success(request, "Your progress has been updated.")
        return redirect('my-profile')

    return render(request, 'profile.html', {'profile': profile})


@login_required
def assign_task(request):
    """
    Allow Heads & Managers to assign tasks.
    Managers cannot assign to Heads.
    """
    assigner = EmployeeProfile.objects.get(user=request.user)
    if assigner.role not in ('head', 'manager'):
        messages.error(request, "Permission denied.")
        return redirect('employee-list')

    # Build the assignee list
    if assigner.role == 'head':
        assignees = EmployeeProfile.objects.exclude(role='admin')
    else:  # manager
        assignees = EmployeeProfile.objects.exclude(role__in=('admin', 'head'))

    if request.method == 'POST':
        title       = request.POST.get('title', '').strip()
        description = request.POST.get('description', '').strip()
        to_id       = request.POST.get('assigned_to')

        if title and to_id:
            try:
                assignee = EmployeeProfile.objects.get(id=to_id)
                Task.objects.create(
                    title=title,
                    description=description,
                    assigned_to=assignee,
                    assigned_by=assigner
                )
                messages.success(request, "Task assigned successfully.")
            except EmployeeProfile.DoesNotExist:
                messages.error(request, "Selected employee does not exist.")
        else:
            messages.error(request, "Title and assignee are required.")

        return redirect('assign-task')

    return render(request, 'assign_task.html', {
        'employees': assignees,
    })

@login_required
def edit_profile(request, user_id):
    """
    Allow Head, Manager, Admin to edit other users' profiles. Employees can only edit their own.
    """
    target_profile = get_object_or_404(EmployeeProfile, user__id=user_id)
    current_profile = EmployeeProfile.objects.get(user=request.user)
    can_edit = False
    if current_profile.role in ('head', 'admin'):
        can_edit = True
    elif current_profile.role == 'manager' and target_profile.role == 'employee':
        can_edit = True
    elif current_profile.user == target_profile.user:
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
    return render(request, 'profile.html', {'profile': target_profile, 'editing_other': current_profile != target_profile})

@login_required
def report_task(request, task_id):
    """
    Allow employees to mark/report their own tasks as done or add a report.
    """
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