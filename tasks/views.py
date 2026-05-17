from django.shortcuts import render, redirect, get_object_or_404
from .models import Task
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm # Import Django's built-in signup form
from django.contrib.auth import login # Allows us to automatically log the user in after signing up

@login_required(login_url='login')
def task_list(request):
    # Check if the user clicked the "Add" button
    if request.method == 'POST':
        task_title = request.POST.get('title') # Grab the text from the input box
        if task_title:
            Task.objects.create(user=request.user, title=task_title) # Create and save it to PostgreSQL!
            return redirect('task_list') # Reload the page to clear the form and show the new task
        
            
    # If it's a normal page visit (GET request), just fetch and show the tasks
    tasks = Task.objects.filter(user=request.user).order_by('-id') # ' -id' displays newest tasks at the top
    return render(request, 'tasks/list.html', {'tasks': tasks})

@login_required(login_url='login')
def toggle_task(request, task_id):
    if request.method == 'POST': # Add this safety check wrapper
        task = get_object_or_404(Task, id=task_id, user=request.user)
        task.complete = not task.complete
        task.save()
    return redirect('task_list')

@login_required(login_url='login')
def delete_task(request, task_id):
    if request.method == 'POST': # Add this safety check wrapper
        task = get_object_or_404(Task, id=task_id, user=request.user)
        task.delete()
    return redirect('task_list')

def register_user(request):
    # If the user is already logged in, they don't need to register; send them home
    if request.user.is_authenticated:
        return redirect('task_list')
        
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save() # Saves the new user to the PostgreSQL database!
            login(request, user) # Instantly logs them in
            return redirect('task_list')
    else:
        form = UserCreationForm()
        
    return render(request, 'tasks/register.html', {'form': form})