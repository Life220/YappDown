from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import User, Note
import hashlib
import os

autherised = False

def login(request):
    global autherised
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        usernames = User.objects.filter(username=username)

        if not usernames.exists():
            error_message = 'Username not found.'
            return render(request, 'login.html', {'error_message': error_message})

        if usernames.count() > 1:
            for user in usernames:
                storedPassword = user.password
                salt = user.salt

                pasSalt = password + salt
                hashedPassword = hashlib.sha256(pasSalt.encode()).hexdigest()
                if hashedPassword == storedPassword:
                    autherised = True
                    return render(request, 'home.html')
                
        error_message = 'Incorrect password.'
        return render(request, 'login.html', {'error_message': error_message})
    else:
        return render(request, 'login.html')

def logout(request):
    global autherised
    autherised = False
    return redirect('login')

def encrypt(password):
    if len(password) < 10:
        salt = os.urandom(16).hex()
        pasSalt = password + salt
    else:
        salt = ""
    hashedPassword = hashlib.sha256(pasSalt.encode()).hexdigest()
    return hashedPassword, salt

def register(request):
    global autherised
    if request.method == 'POST':
        email = request.POST['email']
        username = request.POST['username']
        password = request.POST['password']
        
        if User.objects.filter(email=email).exists():
            error_message = 'Email already in use.'
            return render(request, 'register.html', {'error_message': error_message})
    
        # Encrypt password
        hashed_password, salt = encrypt(password)

        # Create new user
        user = User(email=email, username=username, password=hashed_password, salt=salt)
        user.save()
        
        # Automatically log in the user after registration
        autherised = User.objects.filter(username=username, email=email).exists()
        if autherised:
            return redirect('home')
        else:
            error_message = 'Registration successful, but login failed.'
            return render(request, 'login.html', {'error_message': error_message})
    else:
        return render(request, 'register.html')

def home(request):
    if autherised:
        return render(request, 'home.html')
    else:
        return redirect('login')
    
def note(request):
    if autherised:
        return render(request, 'note.html')
    else:
        return redirect('login')
