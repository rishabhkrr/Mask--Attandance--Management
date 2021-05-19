
from django.conf.urls import url
from django.contrib.auth import REDIRECT_FIELD_NAME
from django.contrib.auth.models import User
from django.http import request
from django.http.response import HttpResponse
from django.shortcuts import render,redirect
from django.contrib.auth import login,logout,authenticate
from django.contrib.auth.decorators import login_required
from .models import AttendanceTable, UserProfile,Account
from .forms import createUserForm,UserProfileForm
from .camera import VideoDetect
from datetime import date

#admin
@login_required(login_url='login')
def home(request):
    if request.user.is_superuser == False:
        return redirect('user')

    empc = Account.objects.filter(is_superuser = False).count()
    att_M = AttendanceTable.objects.filter(mask_detail = True)
    maskc = att_M.count()
    att_WM = AttendanceTable.objects.filter(mask_detail = False)
    withoutmaskc = att_WM.count()
    c = {"N_emp":empc,"N_M":maskc,"N_WM":withoutmaskc}

    return render(request, 'main_base/home.html',c)


@login_required(login_url='login')
def userpage(request):
    if request.user.is_superuser:
        return redirect('home')

    user = request.user
    emp = UserProfile.objects.get(user = user)
    att = AttendanceTable.objects.filter(employee = emp)

    attc = att.count()
    maskc = att.filter(mask_detail = True).count()
    withoutmaskc = att.filter(mask_detail = False).count()

    c = {"N_att":attc,"N_M":maskc,"N_WM":withoutmaskc}

    return render(request, 'main_base/userpage.html',c)

#admin
@login_required(login_url='login')
def registration(request):
    
    if request.user.is_superuser == False:
        return redirect('user')
    
    form1 = createUserForm()
    form2 = UserProfileForm()
    c = {"form1":form1,"form2":form2}
    if request.method == "POST":
        form1 = createUserForm(request.POST)
        form2 = UserProfileForm(request.POST)
        if form1.is_valid and form2.is_valid:
            user = form1.save()
            emp = form2.save(commit=False)
            emp.user = user
            emp.save()
            return redirect('home')

    return render(request, 'main_base/registration.html',c)

def loginUser(request):
    if request.user.is_authenticated:
        if request.user.is_superuser:
            return redirect('home')
        else:
            return redirect('user')
    c = {}
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request,username = username,password = password)
        if user is not None:
            login(request,user)
            if request.user.is_superuser:
                return redirect('home')                
            return redirect('user')
    return render(request,"main_base/login.html",c)

    

def logoutUser(request):

    logout(request)
    return redirect('login')


#admin
@login_required(login_url='login')
def employeelist(request):
    if request.user.is_superuser == False:
        return redirect('user')
    return render(request, 'main_base/employeelist.html')


@login_required(login_url='login')
def userdetails(request):

    return render(request, 'main_base/user_details.html')


@login_required(login_url='login')
def messageadmin(request):

    return render(request, 'main_base/messageadmin.html')


@login_required(login_url='login')
def user_details(request):

    return render(request, 'main_base/user_details.html')


#user only
@login_required(login_url='login')
def TakeAttendance(request):
    if request.user.is_superuser:
        return redirect('home')
    return render(request,'main_base/attendance_page.html')


#user only
@login_required(login_url='login')
def RecognitionSubmit(request):
    if request.user.is_superuser:
        return redirect('home')
    label = VideoDetect()
    mask_detail = False
    if label == "Mask":
        mask_detail = True
    else: 
        mask_detail = False
    user = request.user

    emp = UserProfile.objects.get(user = user)
    d   = date.today()

    att = AttendanceTable(employee = emp, date = d,mask_detail = mask_detail)
    att.save()

    return redirect('user')