from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from apps.schedule.models import Schedule

# Create your models here.
class Task(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tasks')
    schedule = models.ForeignKey(Schedule, on_delete=models.CASCADE, related_name='tasks', null=True, blank=True)
    title = models.CharField(max_length=100)
    description = models.TextField()
    completed = models.BooleanField(default=False)
    duration_minutes = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title} ({self.duration_minutes}m)"

    def clean(self):
        super().clean()
        if not self.schedule_id:
            return

        existing_allocations = sum(
            t.duration_minutes for t in self.schedule.tasks.exclude(pk=self.pk)
        )

        if existing_allocations + self.duration_minutes > self.schedule.total_minutes:
            remaining = self.schedule.total_minutes - existing_allocations
            raise ValidationError(
                f"Cannot add task ({self.duration_minutes}m)"
                f"Only {max(0, remaining)}m remaining time in schedule"
            )