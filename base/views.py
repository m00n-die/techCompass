from django.shortcuts import render, redirect
from django.db.models import Q
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from .models import Job, Category
from .forms import JobForm
# Create your views here.


def loginPage(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, 'User does not exist')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('HomePage')
        else:
            messages.error(request, 'Invalid username or Password')
    context = {}
    return render(request, 'base/login_register.html', context)

def logoutUser(request):
    logout(request)
    return redirect('HomePage')

def home(request):
    """View for the home page"""
    # q gets the query params in the GET url
    q = request.GET.get('q') if request.GET.get('q') != None else ""

    jobs = Job.objects.filter(
        Q(category__category__icontains=q) |
        Q(title__icontains=q) |
        Q(description__icontains=q)
        )
    
    category = Category.objects.all()

    job_count = jobs.count()
    context = {"jobs": jobs, "category": category, 'job_count': job_count}
    return render(request, 'base/home.html', context)


def job(request, pk):
    job = Job.objects.get(id=pk)
    context = {'job': job}
    return render(request, 'base/job.html', context)

def addJob(request):
    form = JobForm
    
    if request.method == 'POST':
        form = JobForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('HomePage')

    context = {"form": form}
    return render(request, 'base/job_form.html', context)

def updateJob(request, pk):
    """Updates info on a Job Listing"""
    job = Job.objects.get(id=pk)
    form = JobForm(instance=job)
    
    if request.method == "POST":
        form = JobForm(request.POST, instance=job)
        if form.is_valid():
            form.save()
            return redirect('HomePage')
        
    context = {'form': form}
    return render(request, 'base/job_form.html', context)

def deleteJob(request, pk):
    """Deletes a Job Listing"""
    job = Job.objects.get(id=pk)
    if request.method == "POST":
        job.delete()
        return redirect('HomePage')
    
    context = {'obj': job}
    return render(request, 'base/delete.html', context)
