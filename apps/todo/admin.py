from django.contrib import admin
from .models import Task, TaskNote
# Register your models here.
admin.site.register(Task)

class TaskNoteAdmin(admin.ModelAdmin):
    list_display = ('note', 'task_id', 'created_at', 'updated_at')
    class Meta:
        model = Task

admin.site.register(TaskNote, TaskNoteAdmin)