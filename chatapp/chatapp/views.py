from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from .forms import LoginForm, SignupForm, UserProfileForm
from .models import UserProfile
from django.contrib.auth.decorators import login_required
from .constants import default_profile_picture

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

def custom_404_view(request, exception):
    if not request.user.is_authenticated:
        return redirect('login')
    return redirect('users')

def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def profile(request):
    user = request.user
    profile, created = UserProfile.objects.get_or_create(user=user)

    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=profile, user=user)
        if form.is_valid():
            user.first_name = form.cleaned_data['first_name']
            user.last_name = form.cleaned_data['last_name']
            user.email = form.cleaned_data['email']
            user.save()
            form.save()
            return redirect('profile')
    else:
        form = UserProfileForm(instance=profile, user=user)

    return render(request, 'pages/profile.html', {'form': form, "default_profile_picture": default_profile_picture})

@login_required
def users(request):
    all_users = User.objects.exclude(id=request.user.id)
    return render(request, 'pages/users.html', {
        'users': all_users,
        'current_user': request.user,
        "default_profile_picture": default_profile_picture
    })

def chat(request, user_id):
    return render(request,"pages/chat.html",{"user_id": user_id})
