from django.shortcuts import render

# Create your views here.
def schedule_list(request):
    return render(request, "schedule/schedule_list.html")