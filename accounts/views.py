import random
import re

from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User, auth
from django.core.mail import send_mail
from django.http import HttpResponse
from django.shortcuts import render, redirect

from .forms import ProfileUpdateForm, UserUpdateForm
from .models import UserOTP


# Create your views here.
def register(request):
    if request.method == "POST":
        get_otp = request.POST.get('otp')

        if get_otp:
            get_usr = request.POST.get('usr')
            usr = User.objects.get(username=get_usr)
            if int(get_otp) == UserOTP.objects.filter(user=usr).last().otp:
                usr.is_active = True
                usr.save()
                messages.info(request, f'Account Created Successfully')
                return redirect('/login')
            else:
                messages.info(request, f'You Entered a Wrong OTP')
                return render(request, 'accounts/register.html', {'otp': True, 'usr': usr})
        if request.POST['password1'] == request.POST['password2']:
            if User.objects.filter(username=request.POST['username']).exists():
                messages.info(request, 'Username Taken')
                return redirect('accounts:register')
            elif User.objects.filter(email=request.POST['email']).exists():
                messages.info(request, 'Email Taken')
                return redirect('accounts:register')
            elif len(request.POST['password1']) < 8:
                messages.info(request, 'Password should be more than 8 in length')
                return redirect('accounts:register')
            elif re.search('[0-9]', request.POST['password1']) is None:
                messages.info(request, 'Password must contain at least one numerical value')
                return redirect('accounts:register')
            elif re.search('[A-Z]', request.POST['password1']) is None:
                messages.info(request, 'Password must contain at least one capital letter')
                return redirect('accounts:register')
            elif re.search('[a-z]', request.POST['password1']) is None:
                messages.info(request, 'Password must contain at least one small letter')
                return redirect('accounts:register')
            else:
                user = User.objects.create_user(username=request.POST['username'], email=request.POST['email'],
                                                password=request.POST['password1'],
                                                first_name=request.POST['first_name'],
                                                last_name=request.POST['last_name'], is_active=False)
                usr_otp = random.randint(100000, 999999)
                usern = request.POST['username']
                usr = User.objects.get(username=usern)
                UserOTP.objects.create(user=usr, otp=usr_otp)
                mess = f"Hello {usr.first_name}.Please Verify your Account,\nYour OTP is {usr_otp}\n Thanks!"
                send_mail(
                    "No Reply- Welcome to AniWatch",
                    mess,
                    settings.EMAIL_HOST_USER,
                    [usr.email],
                    fail_silently=False
                )
                return render(request, 'accounts/register.html', {'otp': True, 'usr': usr})
        else:
            messages.info(request, 'Password Mismatch')
            return redirect('accounts:register')
    else:
        return render(request, 'accounts/register.html')


@login_required()
def change_password(request):
    context = {}
    ch = User.objects.filter(id=request.user.id)
    if len(ch) > 0:
        data = User.objects.get(id=request.user.id)
        context["data"] = data
    if request.method == "POST":
        current = request.POST["cpwd"]
        new_pas = request.POST["npwd"]

        user = User.objects.get(id=request.user.id)
        check = user.check_password(current)
        if check == True:
            user.set_password(new_pas)
            user.save()
            messages.info(request, 'Password Changed Successfully, Please Login again')
            return redirect('accounts:login')

        else:
            messages.info(request, 'Password Incorrect')

    return render(request, "accounts/change_password.html", context)


@login_required()
def profile(request):
    if request.method == "POST":
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            # messages.success(request, f'Your account has been updated!')
            return redirect('accounts:profile')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'u_form': u_form,
        'p_form': p_form,
    }
    return render(request, 'accounts/profile.html', context)


@login_required()
def deleteUser(request, pk):
    user = User.objects.get(pk=pk)
    user.delete()
    messages.info(request, 'Your Account has Successfully been Deleted')
    return render(request, 'accounts/register.html')


def login(request):
    if request.user.is_authenticated:
        return redirect('/')
    if request.method == 'POST':
        get_otp = request.POST.get('otp')  # 213243 #None

        if get_otp:
            get_usr = request.POST.get('usr')
            usr = User.objects.get(username=get_usr)
            if int(get_otp) == UserOTP.objects.filter(user=usr).last().otp:
                usr.is_active = True
                usr.save()
                messages.info(request, f'Your account has been verified. please Login to Proceed')
                return redirect('/login')
            else:
                messages.info(request, f'You Entered a Wrong OTP')
                return render(request, 'accounts/login.html', {'otp': True, 'usr': usr})

        usrname = request.POST['username']
        passwd = request.POST['password']

        user = authenticate(request, username=usrname, password=passwd)  # None
        if user is not None:
            auth.login(request, user)
            return redirect('/')
        elif not User.objects.filter(username=usrname).exists():
            messages.info(request,
                          f'Username not exist')
            return redirect('accounts:login')
        elif not User.objects.get(username=usrname).is_active:
            messages.info(request, f'Your account need verification. Check Your email for OTP and enter here.')
            usr = User.objects.get(username=usrname)
            usr_otp = random.randint(100000, 999999)
            UserOTP.objects.create(user=usr, otp=usr_otp)
            mess = f"Hello {usr.first_name},\nYour OTP is {usr_otp}\nThanks!"

            send_mail(
                "Welcome to AniWatch - Verify Your Email",
                mess,
                settings.EMAIL_HOST_USER,
                [usr.email],
                fail_silently=False
            )
            return render(request, 'accounts/login.html', {'otp': True, 'usr': usr})
        else:
            messages.info(request,
                          f'Please enter a correct username and password. Note that both fields may be case-sensitive.')
            return redirect('accounts:login')

    return render(request, 'accounts/login.html')


def logout_view(request):
    logout(request)
    messages.info(request, 'You have successfully logged out')
    return redirect('accounts:login')


def resend_otp(request):
    if request.method == "GET":
        get_usr = request.GET['usr']
        if User.objects.filter(username=get_usr).exists() and not User.objects.get(username=get_usr).is_active:
            usr = User.objects.get(username=get_usr)
            usr_otp = random.randint(100000, 999999)
            UserOTP.objects.create(user=usr, otp=usr_otp)
            mess = f"Hello {usr.first_name}.Please Verify your Account,\nYour OTP is {usr_otp}\n Thanks!"
            send_mail(
                "No Reply- Welcome to AniWatch",
                mess,
                settings.EMAIL_HOST_USER,
                [usr.email],
                fail_silently=False
            )
            return HttpResponse("Resend")
    return HttpResponse("Cannot send")
