from django.db import models
from django.contrib.auth.models import User 

# Create your models here.
class Schedule(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='schedules')
    title = models.CharField(max_length=156)
    description = models.TextField()
    available = models.BooleanField(default=False)
    total_minutes = models.PositiveIntegerField(default=0) # um time_box deve ser declarado em minutos inteiros
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title} {self.user.username}"

    @property
    def allocated_minutes(self):
        return sum(task.duration_minutes for task in self.tasks.all())

    @property 
    def remaining_minutes(self):
        return self.total_minutes - self.allocated_minutes
    
    @property 
    def utilization_percentage(self):
        if self.total_minutes == 0:
            return 0
        return min(100, int((self.allocated_minutes / self.total_minutes) * 100))

 