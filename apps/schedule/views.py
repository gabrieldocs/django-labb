from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required

from apps.schedule.forms import ScheduleForm
from .models import Schedule


def schedule_list(request):
    schedules = Schedule.objects.filter(user=request.user).order_by('-created_at')
    context = {
        'schedules': schedules
    }
    return render(request, "schedule/schedule_list.html", context)

def schedule_show(request, pk):
    schedule = get_object_or_404(Schedule, pk=pk, user=request.user)
    context = { 'schedule': schedule, 'title': schedule.title}
    return render(request, "schedule/schedule_show.html", context)

@login_required 
def schedule_update(request, pk):
    schedule = get_object_or_404(Schedule, pk=pk)
    if request.method == 'POST':
        form = ScheduleForm(request.POST, instance=schedule)
        if form.is_valid():
            form.save()
            return redirect('schedule:schedule_list')
    else:
        form = ScheduleForm(instance=schedule)
    return render(request, 'schedule/schedule_form.html', {'form': form, 'title': 'Edit Schedule'})

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