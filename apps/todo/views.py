from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_http_methods
from .models import Task
from .forms import TaskForm
from django.contrib.auth.decorators import login_required

# READ (List)
@login_required
def task_list(request):
    tasks = Task.objects.filter(user=request.user).order_by('-created_at')
    total_count = tasks.count()
    pending_count = tasks.filter(completed=False).count()
    completed_count = tasks.filter(completed=True).count()
    return render(request, 'todo/task_list.html', {
        'tasks': tasks,
        'total_count': total_count,
        'pending_count': pending_count,
        'completed_count': completed_count,
    })

# CREATE
@login_required
def task_create(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.user = request.user  # Assign the logged-in user to the task
            task.save()
            return redirect('todo:task_list')
    else:
        form = TaskForm()
    return render(request, 'todo/task_form.html', {'form': form, 'title': 'Create Task'})

# UPDATE
@login_required
def task_update(request, pk):
    task = get_object_or_404(Task, pk=pk)
    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect('todo:task_list')
    else:
        form = TaskForm(instance=task)
    return render(request, 'todo/task_form.html', {'form': form, 'title': 'Edit Task'})

# DELETE
@login_required
def task_delete(request, pk):
    task = get_object_or_404(Task, pk=pk)
    if request.method == 'POST':
        task.delete()
        return redirect('todo:task_list')
    return render(request, 'todo/task_confirm_delete.html', {'task': task})

@login_required
@require_http_methods(["PATCH"])
def task_toggle(request, pk):
    task = get_object_or_404(Task, pk=pk, user=request.user)
    task.completed = not task.completed
    task.save()

    # Recalculate stats for the user
    user_tasks = request.user.tasks.all()
    completed_count = user_tasks.filter(completed=True).count()
    pending_count = user_tasks.filter(completed=False).count()

    context = {
        'task': task,
        'completed_count': completed_count,
        'pending_count': pending_count,
    }
    return render(request, 'todo/partials/task_toggle_response.html', context)

@login_required
@require_http_methods(["DELETE"])
def task_delete(request, pk):
    task = get_object_or_404(Task, pk=pk)
    task.delete()
    return HttpResponse("")