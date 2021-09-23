from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import auth
from django.contrib.auth import authenticate, login, logout
from django.core.exceptions import ObjectDoesNotExist


# Create your views here.

def login_page(request):
    if not request.user.is_authenticated:
        if request.method == 'POST':
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                return render(request, 'employee/loginpage.html', {'title' : 'Login Page', 'error': 'Username and password donot match'})
        else:
            return render(request, 'employee/loginpage.html', {'title' : 'Login Page'})
    else:
        current_user = request.user
        last_name = current_user.last_name
        return render(request, 'employee/welcomepage.html', {'title': 'Home Page', 'name': last_name})


def logout_page(request):
    if request.method == "POST":
        logout(request)
        return redirect('login')

def home_page(request):
    if not request.user.is_authenticated:
        return render(request, 'employee/loginpage.html', {'title' : 'Login Page', 'error': 'Please login first!'})
    else:
        current_user = request.user
        last_name = current_user.last_name
        return render(request, 'employee/welcomepage.html', {'title': 'Home Page', 'name': last_name})

def employee_list_view(request):
    if not request.user.is_authenticated:
        return render(request, 'employee/loginpage.html', {'title' : 'Login Page', 'error': 'Please login first!'})
    else:
        current_user = request.user
        last_name = current_user.last_name
        user = User.objects.all()
        return render(request, 'employee/employeelist.html', {'title': 'Employee List', 'name': last_name, 'user': user})

def registration_page(request):
    if request.method == 'POST':
        if request.POST['password'] == request.POST['cpassword']:
            try:
                username = request.POST['email'].split('@')[0]
                user = User.objects.get(username= username)
                return render(request, 'employee/registrationpage.html', {'title': 'Registration Page', 'error': 'This email is registered with another account!'})
            except ObjectDoesNotExist:
                user = User.objects.create_user( username, request.POST['email'], request.POST['password'], first_name=request.POST['fname'], last_name=request.POST['lname'])
                login(request, user)
                return redirect('home')
        else:
            return render(request, 'employee/registrationpage.html', {'title': 'Registration Page', 'error': 'Password and confrim password donot match' })
    else:
        return render(request, 'employee/registrationpage.html', {'title': 'Registration Page'})