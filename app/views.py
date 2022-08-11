from django.shortcuts import render, redirect, get_object_or_404
from .models import Task
from datetime import date
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect
from django.urls import reverse

def Index(request):
    if request.method == 'GET':
        tasks = Task.objects.all()
        return render(request, 'app/index.html', {'tasks': tasks, 'direction': 'asce'})
    if request.method == 'POST':
        task_id = list(request.POST)[1]
        current_task = Task.objects.get(id=task_id)
        print("Printing Current Task")
        print(current_task)
        print("PRINTING USER:")
        print(request.user)
        current_task.last_cleaned_date = date.today()
        current_task.completed_by = request.user
        current_task.save()
        tasks = Task.objects.all()
        return render(request, 'app/index.html', {'tasks': tasks, 'direction': 'asce'})

def LoginView(request):
    if request.method == 'GET':
        return render(request, 'app/login.html', {})
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            print('SUCCESS!')
            return HttpResponseRedirect(reverse('index'))
        else:
            print('FAILURE')
            return render(request, 'app/login.html', {})


def LogoutView(request):
    logout(request)
    print('Running logout view')
    if request.user is not None:
        print("Something went wrong!")
    return redirect('index')

def CreateTaskView(request):
    if request.method == 'GET':
        if request.user.is_authenticated:
            return render(request, 'app/new-task.html', {})
        else:
            return HttpResponseRedirect(reverse('index'))
    if request.method == 'POST':
        activity = request.POST['activity']
        room = request.POST['room']
        last_cleaned_date = date.today()
        task = Task(activity=activity, room=room, last_cleaned_date=last_cleaned_date)
        task.save()
        return HttpResponseRedirect(reverse('index'))

def DeleteTaskView(request, uuid):
    task = get_object_or_404(Task, id=uuid)
    if task is not None:
        task.delete()
        return HttpResponseRedirect(reverse('index'))
    else:
        return HttpResponseRedirect(reverse('index'))

def SortTableView(request, orderby, direction):
    if request.method == 'GET':
        print("PRINTING DIRECTION AT TOP:")
        print(direction)
        try:
            if direction == 'asce':
                print("IN ASCE ORDER ALREADY, FLIPPING TO DESC")
                filtered_tasks = Task.objects.all().order_by(orderby)
                print("MADE IT PAST THE REVERSE ORDER BY")
                new_direction = 'desc'
            elif direction == 'desc':
                string_order = '-'+str(orderby)
                print("PRINTING STRING ORDER")
                print(string_order)
                filtered_tasks = Task.objects.all().order_by(string_order)
                new_direction = 'asce'
            else:
                print("SOMETHING FUCKED UP")
                new_direction = 'asce'
        except:
            print("WENT INTO EXCEPTION, ERROR")
            filtered_tasks = Task.objects.all()
            new_direction = 'asce'
        finally:
            print("PRINTING ORDER BY VALUE:")
            print(orderby)
            print("PRINTING DIRECTION AT END")
            print(new_direction)
            return render(request, 'app/index.html', {'tasks': filtered_tasks, 'direction': new_direction})

