from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import Group
from django.shortcuts import render, redirect

from backend.models import Gender, CustomUser


# Create your views here.
def home(request):
    return render(request, 'frontend/home.html')

def auth_login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        # Authenticate the user
        user = authenticate(request, username=email,password=password)

        if user is not None:
            # Login the user
            login(request,user)
            return redirect('home') # Redirect to a success page
        else:
            messages.error(request,'Invalid email or password')

    context = {
        'page_title': 'Login'
    }
    return render(request,'frontend/auth/login.html',context)

def auth_logout(request):
    logout(request) # Log out the user
    return redirect('home')  # Redirect to the login page or home page

def author_register(request):

    if request.method == 'POST':
        email = request.POST.get('email', '').strip()
        gender = request.POST.get('gender', Gender.MALE)
        password = request.POST.get('password','')
        confirm_password = request.POST.get('confirmPassword','')

        # Validate required fields
        if not email or not password or not confirm_password:
            messages.error(request, 'All fields are required.')
        elif password != confirm_password:
            messages.error(request,'Passwords do not match.')
        elif CustomUser.objects.filter(email=email).exists():
            messages.error(request, 'Phone Number already exists.')
        else:
            #create the user
            user=CustomUser.objects.create(
                email=email,
                gender=gender,
                password=make_password(password),
            )

            # Add user to a group
            group_name = "Author"  # Change to your actual group name
            group, created = Group.objects.get_or_create(name=group_name)
            user.groups.add(group)

            messages.success(request,'Account Created Successfully.☺ Please login')
            return redirect('login') # Change 'login' to your actual login URL name

    context = {
        'page_title':'Author Register'
    }
    return render(request,'frontend/auth/author/register.html',context)


def member_register(request):
    if request.method == 'POST':
        email = request.POST.get('email', '').strip()
        gender = request.POST.get('gender', Gender.MALE)
        password = request.POST.get('password', '')
        confirm_password = request.POST.get('confirmPassword', '')

        # Validate required fields
        if not email or not password or not confirm_password:
            messages.error(request, 'All fields are required.')
        elif password != confirm_password:
            messages.error(request, 'Passwords do not match.')
        elif CustomUser.objects.filter(email=email).exists():
            messages.error(request, 'Phone Number already exists.')
        else:
            # create the user
            user = CustomUser.objects.create(
                email=email,
                gender=gender,
                password=make_password(password),
            )

            # Add user to a group
            group_name = "Member"  # Change to your actual group name
            group, created = Group.objects.get_or_create(name=group_name)
            user.groups.add(group)

            messages.success(request, 'Account Created Successfully.☺ Please login')
            return redirect('login')  # Change 'login' to your actual login URL name
    context ={
        'page_title':'Member Register'
    }
    return render(request, 'frontend/auth/member/register.html',context)

@login_required(login_url='login')  # Redirect to login if not authenticated
def profile(request):
    user = request.user  # Get the currently logged-in user

    # Get the user's groups (if you want to show their role)
    groups = user.groups.values_list('name', flat=True)

    context = {
        'page_title': 'Profile',
        'user': user,
        'groups': groups,
    }
    return render(request, 'frontend/auth/profile.html', context)