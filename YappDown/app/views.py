from django.shortcuts import render, redirect
from django.http import HttpResponse

username = ""

def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        if authYapper():
            return redirect('home')
        else:
            return HttpResponse('Invalid login credentials')
    return render(request, 'login.html')

def authYapper(password):
    if username:
        return True
    return False

def home(request):
    return render(request, 'home.html')