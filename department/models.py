from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator

# Create your models here.
class EmployeeProfile(models.Model):
    ROLE_CHOICES = [
        ('employee', 'Employee'),
        ('manager',  'Manager'),
        ('head',     'Head'),
        ('admin',    'Admin'),
    ]
    user     = models.OneToOneField(User, on_delete=models.CASCADE)
    role     = models.CharField(max_length=20, choices=ROLE_CHOICES, default='employee')
    progress = models.PositiveIntegerField(
        default=0,
        validators=[MaxValueValidator(100)]
    )
    # remove score/last_day_progress here; we’ll track per-task reviews instead

class Task(models.Model):
    title        = models.CharField(max_length=200)
    description  = models.TextField(blank=True)
    assigned_to  = models.ForeignKey(EmployeeProfile, related_name='tasks', on_delete=models.CASCADE)
    assigned_by  = models.ForeignKey(EmployeeProfile, related_name='assigned_tasks', on_delete=models.SET_NULL, null=True)
    status       = models.CharField(max_length=20, choices=[('pending','Pending'),('in_progress','In Progress'),('done','Done')], default='pending')
    progress     = models.PositiveIntegerField(default=0)
    review       = models.TextField(blank=True)
    attachment   = models.FileField(upload_to='task_uploads/', blank=True, null=True)
    created_at   = models.DateTimeField(auto_now_add=True)
    due_date     = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.title} → {self.assigned_to.user.username}"
