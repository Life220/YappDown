from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .models import User, Note
import hashlib
import os

def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        if not username or not password:
            error_message = 'Username and password are required.'
            return render(request, 'login.html', {'error_message': error_message})

        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            error_message = 'Username not found.'
            return render(request, 'login.html', {'error_message': error_message})

        storedPassword = user.password
        salt = user.salt

        pasSalt = password + salt
        hashedPassword = hashlib.sha256(pasSalt.encode()).hexdigest()
        if hashedPassword == storedPassword:
            request.session['user_id'] = user.user_ID
            return redirect('home')
                
        error_message = 'Incorrect password.'
        return render(request, 'login.html', {'error_message': error_message})
    else:
        return render(request, 'login.html')

def logout(request):
    request.session.flush()
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
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        # Encrypt password
        hashed_password, salt = encrypt(password)

        # Create new user
        if username == "admin":
            user = User(username=username, password=hashed_password, salt=salt, admin=True)
        else:
            user = User(username=username, password=hashed_password, salt=salt)
        user.save()
        
        # Automatically log in the user after registration
        request.session['user_id'] = user.user_ID
        return redirect('home')
    else:
        return render(request, 'register.html')

def home(request):
    user_id = request.session.get('user_id')
    if user_id:
        user = User.objects.get(user_ID=user_id)
        notes = Note.objects.filter(user_ID=user)
        total_storage_used = sum(len(note.content) for note in notes) / (1024 * 1024)  # Convert bytes to MB
        max_storage = 10  # 10 MB
        storage_left = max_storage - total_storage_used

        return render(request, 'home.html', {
            'notes': notes,
            'total_storage_used': total_storage_used,
            'storage_left': storage_left,
            'max_storage': max_storage,
            'is_admin': user.admin
        })
    else:
        return redirect('login')
            
def note(request, note_id=None):
    user_id = request.session.get('user_id')
    if user_id:
        user = User.objects.get(user_ID=user_id)
        notes = Note.objects.filter(user_ID=user)
        total_storage_used = sum(len(note.content) for note in notes) / (1024 * 1024)  # Convert bytes to MB
        max_storage = 10
        storage_left = max_storage - total_storage_used

        success_message = None
        error_message = None

        if request.method == 'POST':
            if 'delete' in request.POST:
                if note_id:
                    note = get_object_or_404(Note, pk=note_id)
                    note.delete()
                    success_message = "Note removed successfully."
                    return redirect('home')
            else:
                title = request.POST.get('title')
                content = request.POST.get('content')
                content_size_mb = len(content) / (1024 * 1024)  # Convert bytes to MB

                if title and content:
                    if note_id:
                        note = get_object_or_404(Note, pk=note_id)
                        if total_storage_used - len(note.content) / (1024 * 1024) + content_size_mb <= max_storage:
                            note.title = title
                            note.content = content
                            note.save()
                            success_message = "Note updated successfully."
                        else:
                            error_message = "Not enough storage space to update the note."
                    else:
                        if total_storage_used + content_size_mb <= max_storage:
                            Note.objects.create(title=title, content=content, user_ID_id=user_id)
                            success_message = "Note saved successfully."
                        else:
                            error_message = "Not enough storage space to create a new note."
                else:
                    error_message = "Title and content are required."

        if note_id:
            note = get_object_or_404(Note, pk=note_id)
        else:
            note = None

        return render(request, 'note.html', {
            'note': note,
            'notes': notes,
            'success_message': success_message,
            'error_message': error_message,
            'total_storage_used': total_storage_used,
            'storage_left': storage_left,
            'max_storage': max_storage
        })
    else:
        return redirect('login')

def note_detail(request, note_id):
    note = get_object_or_404(Note, pk=note_id)
    return render(request, 'note_detail.html', {'note': note})

def admin(request):
    user_id = request.session.get('user_id')
    if user_id:
        user = User.objects.get(user_ID=user_id)
        if user.admin:
            users = User.objects.all()
            total_storage = sum(user.storage_used for user in users)
            return render(request, 'admin.html', {
                'users': users,
                'total_storage': total_storage
            })
        else:
            return HttpResponse("You are not authorized to view this page.", status=403)
    else:
        return redirect('login')
    
def toggle_access(request, user_id):
    user = get_object_or_404(User, user_ID=user_id)
    if request.method == 'POST':
        user.hasAccess = not user.hasAccess
        user.save()
        return redirect('admin')
    return HttpResponse("Invalid request method.", status=405)