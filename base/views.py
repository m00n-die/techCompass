from django.shortcuts import render, redirect
from django.db.models import Q
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponse
from .models import Job, Category, Comment
from .forms import JobForm


def loginPage(request):
    page = 'login'
    if request.user.is_authenticated:
        return redirect('HomePage')
    
    if request.method == "POST":
        username = request.POST.get('username').lower()
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
    context = {'page': page}
    return render(request, 'base/login_register.html', context)

def logoutUser(request):
    logout(request)
    return redirect('HomePage')

def registerUser(request):
    form = UserCreationForm()

    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid:
            user = form.save(commit=False)

            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect('HomePage')
        else:
            messages.error(request, "An unknown error occured. Please try again")

    context = {"form": form}
    return render(request, 'base/login_register.html', context)

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

    all_jobs = Job.objects.all()
    context = {"jobs": jobs, "category": category, 'job_count': job_count, "all_jobs": all_jobs}
    return render(request, 'base/home.html', context)


def job(request, pk):
    job = Job.objects.get(id=pk)
    comments = job.comment_set.all().order_by('-created')

    if request.method == 'POST':
        comment = Comment.objects.create(
            user = request.user,
            job = job,
            comment = request.POST.get('comment'),
        )
        return redirect('Job', pk=job.id)
    
    context = {'job': job, "comments": comments}
    return render(request, 'base/job.html', context)

def userProfile(request, pk):
    user = User.objects.get(id=pk)
    jobs = user.job_set.all()
    context = {'user': user, 'jobs': jobs}
    return render(request, 'base/profile.html', context)

@login_required(login_url='login')
def addJob(request):
    form = JobForm
    
    if request.method == 'POST':
        form = JobForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('HomePage')

    context = {"form": form}
    return render(request, 'base/job_form.html', context)

@login_required(login_url='login')
def updateJob(request, pk):
    """Updates info on a Job Listing"""
    job = Job.objects.get(id=pk)
    form = JobForm(instance=job)

    # TODO: Make a custom template for this and remove the HttpResponse
    if request.user != job.posted_by:
        return HttpResponse('You are not allowed!')
    
    if request.method == "POST":
        form = JobForm(request.POST, instance=job)
        if form.is_valid():
            form.save()
            return redirect('HomePage')
        
    context = {'form': form}
    return render(request, 'base/job_form.html', context)

@login_required(login_url='login')
def deleteJob(request, pk):
    """Deletes a Job Listing"""
    job = Job.objects.get(id=pk)

    # TODO: Make a custom template for this and remove the HttpResponse
    if request.user != job.posted_by:
        return HttpResponse('You are not allowed!')
    
    if request.method == "POST":
        job.delete()
        return redirect('HomePage')
    
    context = {'obj': job}
    return render(request, 'base/delete.html', context)

@login_required(login_url='login')
def deleteComment(request, pk):
    """Deletes a Job Listing"""
    comment = Comment.objects.get(id=pk)

    # TODO: Make a custom template for this and remove the HttpResponse
    if request.user != comment.user:
        return HttpResponse('You are not allowed!')
    
    if request.method == "POST":
        comment.delete()
        return redirect('HomePage')
    
    context = {'obj': comment}
    return render(request, 'base/delete.html', context)
