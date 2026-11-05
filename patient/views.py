from django.shortcuts import render

# Create your views here. 

def index(request):
    return render(request, 'index.html')

def login_user(request):
    return render(request, 'login.html')

def dashboard(request):
    return render(request, 'dashboard.html')

def book_appointment(request):
    return render(request, 'book_appointment.html')

def profile(request):
    return render(request, 'profile.html')
