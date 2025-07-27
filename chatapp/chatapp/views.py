from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from .forms import LoginForm, SignupForm
from .models import UserProfile

def login_view(request):
    form = LoginForm(request.POST or None)
    error = None

    if request.method == 'POST' and form.is_valid():
        email = form.cleaned_data['email']
        password = form.cleaned_data['password']

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            user = None

        if user:
            user = authenticate(username=user.username, password=password)
            if user:
                login(request, user)
                return redirect('users')  # replace with your actual route
            else:
                error = "Incorrect password."
        else:
            error = "Invalid credentials."

    return render(request, 'pages/login.html', {'form': form, 'error': error})

def signup(request):
    form = SignupForm(request.POST or None, request.FILES or None)
    if request.method == 'POST' and form.is_valid():
        first_name = form.cleaned_data['first_name']
        last_name = form.cleaned_data['last_name']
        email = form.cleaned_data['email']
        password = form.cleaned_data['password']
        image = request.FILES.get('image')  # Optional image

        username = email.split('@')[0]
        user = User.objects.create_user(username=username, email=email, password=password)
        user.first_name = first_name
        user.last_name = last_name
        user.save()

        # ✅ Save image only if provided
        if image:
            UserProfile.objects.create(user=user, image=image)
        else:
            UserProfile.objects.create(user=user)

        login(request, user)
        return redirect('users')

    return render(request, 'pages/signup.html', {'form': form})

def profile(request):
    return render(request,"pages/profile.html")

def users(request):
    return render(request,"pages/users.html")

def chat(request, user_id):
    return render(request,"pages/chat.html",{"user_id": user_id})

def custom_404_view(request, exception):
    if not request.user.is_authenticated:
        return redirect('login')
    return redirect('users')
