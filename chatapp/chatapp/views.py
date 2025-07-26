from django.http import HttpResponse
from django.shortcuts import render

def login(request):
    return render(request,"pages/login.html")

def signup(request):
    return render(request,"pages/signup.html")

def profile(request):
    return render(request,"pages/profile.html")

def users(request):
    return render(request,"pages/users.html")

def chat(request, user_id):
    return render(request,"pages/chat.html",{"user_id": user_id})
