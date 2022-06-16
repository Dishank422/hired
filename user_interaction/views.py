import os

from django.shortcuts import render, redirect
from .forms import CreateUserForm, CreateEmployerForm, GetUserProfile, GetJob, OTP
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from .models import student, employer, Job
import smtplib
import random

# Create your views here.


def index(request):
    return render(request, 'index.html')


def sloginPage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            if not student.objects.filter(username=user).exists():
                messages.info(request, 'Username or Password is incorrect')
                return render(request, 'slogin.html')
            login(request, user)
            return redirect('/studentProfile')
        else:
            messages.info(request, 'Username or Password is incorrect')
            return render(request, 'slogin.html')
    return render(request, 'slogin.html')


def sregister(request):
    form = CreateUserForm()
    context = {'form': form}
    if request.method == 'POST':
        username = request.POST.get('username')
        if len(username) < 11:
            messages.info(request, 'Only IITH students can register.')
            return render(request, 'sregister.html', context)
        elif username[-11:].lower() != "@iith.ac.in":
            messages.info(request, 'Only IITH students can register.')
            return render(request, 'sregister.html', context)
        form = CreateUserForm(request.POST)
        if form.is_valid():
            request.session['registrant'] = request.POST
            return HttpResponseRedirect('/sotp')
        else:
            messages.info(request, 'Error registering. Please ensure that you do not have another account with this email id. Password should be at least 8 characters and cannot be entirely numeric.')
            return render(request, 'sregister.html', context)
    return render(request, 'sregister.html', context)


def sotp(request):
    if 'otp' not in request.session or request.method == 'GET':
        otp = random.randrange(100000, 999999, 1)
        msg = "Your OTP to register for Hired is "+str(otp)+"."
        s = smtplib.SMTP('smtp.gmail.com', 587)
        s.starttls()
        password = os.getenv("EMAIL")
        s.login("hiredfromiith@gmail.com", password)
        s.sendmail('&&&&&&&&&&&', request.session['registrant']['username'], msg)
        request.session['otp'] = otp
        return render(request, 'sotp.html')
    if request.method == 'POST':
        form = OTP(request.POST)
        if form.is_valid():
            a = int(request.POST['otp'])
            if a == request.session['otp']:
                registrant = request.session['registrant']
                data = CreateUserForm(registrant)
                data.save()
                messages.success(request, 'Account created successfully. Please login.')
                return redirect('/slogin')
            else:
                messages.info(request, "Wrong OTP. Please enter correct OTP.")
                return render(request, 'sotp.html')


def rloginPage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            if not employer.objects.filter(username=user).exists():
                messages.info(request, 'Username or Password is incorrect')
                return render(request, 'rlogin.html')
            login(request, user)
            return redirect('/recruiterProfile')
        else:
            messages.info(request, 'Username or Password is incorrect')
            return render(request, 'rlogin.html')
    return render(request, 'rlogin.html')


def rregister(request):
    form = CreateUserForm()
    context = {'form': form}
    if request.method == 'POST':
        form = CreateEmployerForm(request.POST)
        if form.is_valid():
            request.session['registrant'] = request.POST
            return HttpResponseRedirect('/rotp')
        else:
            messages.info(request, 'Error registering. Please ensure that you do not have another account with this email id. Password should be at least 8 characters and cannot be entirely numeric.')
            return render(request, 'rregister.html', context)
    return render(request, 'rregister.html', context)


def rotp(request):
    if 'otp' not in request.session or request.method == 'GET':
        otp = random.randrange(100000, 999999, 1)
        msg = "Your OTP to register for Hired is "+str(otp)+"."
        s = smtplib.SMTP('smtp.gmail.com', 587)
        s.starttls()
        password = os.getenv("EMAIL")
        s.login("hiredfromiith@gmail.com", password)
        s.sendmail('&&&&&&&&&&&', request.session['registrant']['username'], msg)
        request.session['otp'] = otp
        return render(request, 'rotp.html')
    if request.method == 'POST':
        form = OTP(request.POST)
        if form.is_valid():
            a = int(request.POST['otp'])
            if a == request.session['otp']:
                registrant = request.session['registrant']
                data = CreateEmployerForm(registrant)
                data.save()
                messages.success(request, 'Account created successfully. Please login.')
                return redirect('/rlogin')
            else:
                messages.info(request, "Wrong OTP. Please enter correct OTP.")
                return render(request, 'rotp.html')


@login_required(login_url='/slogin')
def studentProfile(request):
    if not student.objects.filter(username=request.user).exists():
        return render(request, 'slogin.html')
    profile = student.objects.get(username=request.user).profile
    context = {'profile': profile}
    return render(request, 'student.html', context)


@login_required(login_url='/slogin')
def studentProfileUpdate(request):
    if not student.objects.filter(username=request.user).exists():
        return render(request, 'slogin.html')
    profile = student.objects.get(username=request.user).profile
    context = {'profile': profile}
    if request.method == 'POST':
        user = student.objects.get(username=request.user)
        form = GetUserProfile(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('/studentProfile')
    return render(request, 'studentUpdate.html', context)


@login_required(login_url='/rlogin')
def recruiterProfile(request):
    if not employer.objects.filter(username=request.user).exists():
        return render(request, 'rlogin.html')
    recruiter = employer.objects.get(username=request.user)
    context = {'jobs': recruiter.job_set.all()}
    return render(request, 'recruiter.html', context)


@login_required(login_url='/rlogin')
def job(request):
    if not employer.objects.filter(username=request.user).exists():
        return render(request, 'rlogin.html')
    context = {}
    if request.method == 'POST':
        form = GetJob(request.POST)
        if form.is_valid():
            new_job = form.save(commit=False)
            new_job.employer = employer.objects.get(username=request.user)
            new_job.save()
            return redirect('/recruiterProfile')
    return render(request, 'job.html', context)


@login_required(login_url='/rlogin')
def jobEdit(request):
    if not employer.objects.filter(username=request.user).exists():
        return render(request, 'rlogin.html')
    if request.method == 'POST':
        current_job = Job.objects.get(id=request.POST['jobID'])
        recruiter = employer.objects.get(username=request.user)
        if current_job not in recruiter.job_set.all():
            return render(request, 'rlogin.html')
        context = {'job': current_job}
        form = GetJob(request.POST, instance=current_job)
        if form.is_valid():
            form.save()
            return redirect('/recruiterProfile')
        return render(request, 'jobEdit.html', context)
    return render(request, 'rlogin.html')


@login_required(login_url='/rlogin')
def studentSearch(request):
    if not employer.objects.filter(username=request.user).exists():
        return render(request, 'rlogin.html')
    if request.method == 'POST':
        query = request.POST['query']
        students = student.objects.filter(vector_column=query)
        context = {'students': students}
        return render(request, 'studentSearch.html', context)
    return render(request, 'rlogin.html')


@login_required(login_url='/rlogin')
def studentView(request):
    if not employer.objects.filter(username=request.user).exists():
        return render(request, 'rlogin.html')
    if request.method == 'POST':
        candidate = student.objects.get(id=request.POST['studentID'])
        context = {'student': candidate}
        return render(request, 'studentView.html', context)
    return render(request, 'rlogin.html')


@login_required(login_url='/slogin')
def jobSearch(request):
    if not student.objects.filter(username=request.user).exists():
        return render(request, 'slogin.html')
    if request.method == 'POST':
        query = request.POST['query']
        good_jobs = Job.objects.filter(vector_column=query)
        context = {'jobs': good_jobs}
        return render(request, 'jobSearch.html', context)
    return render(request, 'slogin.html')


@login_required(login_url='/slogin')
def jobView(request):
    if not student.objects.filter(username=request.user).exists():
        return render(request, 'slogin.html')
    if request.method == 'POST':
        required_job = Job.objects.get(id=request.POST['jobID'])
        context = {'job': required_job}
        return render(request, 'jobView.html', context)
    return render(request, 'slogin.html')
