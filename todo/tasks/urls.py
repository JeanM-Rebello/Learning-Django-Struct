from django.urls import path
from . import views

urlpatterns = [
    path('helloworld/', views.hello_world),
    path('',views.task_list, name = 'task-list'),
    path('task/<int:id>', views.task_view, name="taks-view"),
    path('newtask/',views.new_task, name = "new-task"),
    path('edit/<int:id>', views.edit_task, name = 'edit-task'),
    path('changestatus/<int:id>', views.change_status, name = 'chnage-status'),
    path('delete/<int:id>', views.delete_task, name = 'delete-task'),
    path('yourname/<str:name>', views.your_name, name = 'your-name')
]