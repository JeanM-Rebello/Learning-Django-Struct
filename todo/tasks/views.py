from django.shortcuts import render,get_object_or_404,redirect
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.http import HttpResponse
from django.contrib import messages
from .models import Task
from .forms import TaskForm
import datetime

@login_required
def task_list(request):
    search=request.GET.get('search')
    filter=request.GET.get('filter')
    task_done_recently = Task.objects.filter(done = "feito", updated_at=datetime.datetime.now()-datetime.timedelta(days=30),user=request.user).count()
    task_done = Task.objects.filter(done = "feito",user=request.user).count()
    task_doing = Task.objects.filter(done = "fazendo",user=request.user).count()
    if search:
        tasks = Task.objects.filter(title__icontains=search, user=request.user)
    elif filter:
        tasks = Task.objects.filter(done=filter, user=request.user)
    else:
        tasks_list_var = Task.objects.all().order_by('-created_at').filter(user=request.user)
        paginator = Paginator(tasks_list_var, 5)
        page = request.GET.get('page')
        tasks = paginator.get_page(page)
    return render(request,'tasks/list.html',{'tasks': tasks,'tasksrecently':task_done_recently,'tasksdone':task_done,'tasksdoing':task_doing})

@login_required
def task_view(request,id):
    task = get_object_or_404(Task,pk=id)
    return render(request, 'tasks/task.html',{'task':task})

@login_required
def new_task(request):
    if request.method == "POST":
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.done = 'fazendo'
            task.user =  request.user
            task.save()
            return redirect('/')
    else:    
        form = TaskForm()
        return render(request, 'tasks/addtask.html',{'form':form})

@login_required
def edit_task(request,id):
    task = get_object_or_404(Task,pk=id)
    form = TaskForm(instance=task)
    
    if request.method == "POST":
        form = TaskForm(request.POST,instance=task)
        if(form.is_valid()):
            task.save()
            return redirect('/')
        else:
            return render(request,'tasks/editTask.html', {'form':form,'task':task})
    else:
        return render(request,'tasks/editTask.html', {'form':form,'task':task})

@login_required
def delete_task(request,id):
    task = get_object_or_404(Task,pk=id)
    task.delete()
    messages.success(request,"Tarefa deletada com sucesso!!!")
    return redirect('/')

@login_required
def change_status(request,id):
    task = get_object_or_404(Task,pk=id)
    if(task.done == 'fazendo'):
        task.done = 'feito'
    else:
        task.done = 'fazendo'
    task.save()
    return redirect('/')

@login_required
def hello_world(request):
    return HttpResponse('Hello World!')

@login_required
def your_name(resquest, name):
    return render(resquest,'tasks/yourname.html',{'name': name})