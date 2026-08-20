from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods

from apps.schedule.forms import ScheduleForm
from apps.todo.forms import TaskForm
from .models import Schedule
from apps.todo.models import Task

def schedule_list(request):
    schedules = Schedule.objects.filter(user=request.user).order_by('-created_at')
    context = {
        'schedules': schedules
    }
    return render(request, "schedule/schedule_list.html", context)

def schedule_show(request, pk):
    schedule = get_object_or_404(Schedule, pk=pk, user=request.user)

    if request.method == 'POST':
        form = TaskForm(request.POST)
        
        if form.is_valid():
            task = form.save(commit=False)
            task.user = request.user
            task.schedule = schedule
            task.save()
            
            if request.headers.get('HX-Request'):
                # 💡 RE-FETCH THE SCHEDULE FRESH FROM DB
                # This clears the ORM cache and forces recalculation of remaining_minutes
                fresh_schedule = Schedule.objects.get(pk=pk, user=request.user)
                
                response = render(
                    request, 
                    'schedule/partials/schedule_task_created_partial.html', 
                    {'schedule': fresh_schedule}
                )
                response['HX-Trigger'] = 'close-task-modal'
                return response 
            
            return redirect('schedule:schedule_show', pk=schedule.pk)
        
        if request.headers.get('HX-Request'):
            return render(request, 'schedule/partials/schedule_task_form.html', {
                'schedule': schedule,
                'form': form,
                'title': schedule.title
            })
    else:
        form = TaskForm()

    context = { 'schedule': schedule, 'title': schedule.title, 'form': form }
    return render(request, "schedule/schedule_show.html", context)

@login_required 
def schedule_update(request, pk):
    schedule = get_object_or_404(Schedule, pk=pk)
    is_modal = bool(request.headers.get('HX-Request'))
    if request.method == 'POST':
        form = ScheduleForm(request.POST, instance=schedule)
        if form.is_valid():
            form.save()

            if is_modal:
                response = render(request, 'schedule/partials/schedule_task_created_partial.html', {'schedule': schedule})
                response['HX-Trigger'] = 'close-schedule-modal'
                return response
            
            return redirect('schedule:schedule_list')
        if is_modal:
            return render(request, 'schedule/partials/schedule_form_partial.html', {
                'schedule': schedule, 'form': form, 'is_modal': True
            })
        return render(request, 'schedule/schedule_form.html', {
            'form': form, 'title': 'Edit Schedule', 'schedule': schedule, 'is_modal': False
        })
    else:
        form = ScheduleForm(instance=schedule)

    if is_modal:
        return render(request, 'schedule/partials/schedule_form_partial.html', {
            'schedule': schedule, 'form': form, 'is_modal': True
        })
    return render(request, 'schedule/schedule_form.html', {'form': form, 'title': 'Edit Schedule', 'is_modal': False})

@login_required
def schedule_create(request):
    if request.method == 'POST':
        form = ScheduleForm(request.POST)
        if form.is_valid():
            schedule = form.save(commit=False)
            schedule.user = request.user 
            schedule.save()
            return redirect('schedule:schedule_list')
    else:
        form = ScheduleForm()
    return render(request, 'schedule/schedule_form.html', {'form': form, 'title': 'Create Schedule'})

@login_required
@require_http_methods(["PATCH"])
def schedule_task_toggle(request, pk):
    task = get_object_or_404(Task, pk=pk)
    task.completed = not task.completed
    task.save()
    
    context = {
        'task': task,
    }
    
    return render(request, 'schedule/partials/schedule_task_item.html', context)