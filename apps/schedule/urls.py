from django.urls import path 
from . import views 

app_name = 'schedule'

urlpatterns = [
    path('', views.schedule_list, name='schedule_list'),
    path('create/', views.schedule_create, name='schedule_create'),
    path('<int:pk>/show/', views.schedule_show, name='schedule_show'),
    path('<int:pk>/edit/', views.schedule_update, name='schedule_update'),
    path('<int:pk>/toggle/', views.schedule_task_toggle, name='schedule_task_toggle')
]