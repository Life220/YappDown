from django.shortcuts import render, redirect, get_object_or_404
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse
from .models import User, Note
import hashlib
import os
import shutil
import psutil

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
            'user': user,
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
        success_message = None
        error_message = None

        user = get_object_or_404(User, user_ID=user_id)
        if user.hasAccess:
            notes = Note.objects.filter(user_ID=user)
            total_storage_used = sum(len(note.content) for note in notes) / (1024 * 1024)  # Convert bytes to MB
            max_storage = 10  # 10 MB
            storage_left = max_storage - total_storage_used

            if request.method == 'POST':
                title = request.POST.get('title')
                content = request.POST.get('content')
                file = request.FILES.get('file')
                new_content_size = len(content) / (1024 * 1024)  # Convert bytes to MB

                if file and not title:
                    fs = FileSystemStorage()
                    filename = fs.save(file.name, file)
                    file_url = fs.url(filename)
                    new_content_size += file.size / (1024 * 1024)  # Add file size to content size

                    if file.content_type == 'text/plain':
                        file_content = file.read().decode('utf-8')
                        lines = file_content.split('\n')
                        title = lines[0]
                        content = '\n'.join(lines[1:])
                    else:
                        content = ""
                        title = file.name

                if 'delete' in request.POST:
                    if note_id:
                        note = get_object_or_404(Note, pk=note_id, user_ID_id=user_id)
                        note.delete()
                        success_message = "Note removed successfully."
                        return redirect('home')
                else:
                    if title and (content or file):
                        if note_id:
                            note = get_object_or_404(Note, pk=note_id, user_ID_id=user_id)
                            current_note_size = len(note.content) / (1024 * 1024)  # Convert bytes to MB
                            if Note.objects.filter(title=title, user_ID_id=user_id).exclude(pk=note_id).exists():
                                error_message = "A note with this title already exists."
                            elif total_storage_used - current_note_size + new_content_size > max_storage:
                                error_message = "Not enough storage space to update this note."
                            else:
                                note.title = title
                                note.content = content
                                if file:
                                    note.file_url = file_url
                                note.save()
                                success_message = "Note updated successfully."
                        else:
                            if Note.objects.filter(title=title, user_ID_id=user_id).exists():
                                error_message = "A note with this title already exists."
                            elif total_storage_used + new_content_size > max_storage:
                                error_message = "Not enough storage space to add this note."
                            else:
                                note = Note.objects.create(title=title, content=content, user_ID_id=user_id)
                                note.save()
                                success_message = "Note saved successfully."
                    else:
                        error_message = "Title and content are required."

            if note_id:
                note = get_object_or_404(Note, pk=note_id, user_ID_id=user_id)
            else:
                note = None

            notes = Note.objects.filter(user_ID_id=user_id, parent_Note_ID__isnull=True)
            return render(request, 'note.html', {
                'note': note,
                'notes': notes,
                'success_message': success_message,
                'error_message': error_message,
                'storage_left': storage_left
            })
        else:
            return redirect('home')
    else:
        return redirect('login')
    
def admin(request):
    user_id = request.session.get('user_id')
    if user_id:
        user = User.objects.get(user_ID=user_id)
        if user.admin:
            users = User.objects.all()
            total_storage = sum(user.storage_used for user in users)
            
            # Get disk usage
            total, used, free = shutil.disk_usage("/")
            disk_storage_left = free / (1024 * 1024 * 1024)  # Convert bytes to GB
            
            # Get CPU usage
            cpu_usage = psutil.cpu_percent(interval=1)
            
            return render(request, 'admin.html', {
                'users': users,
                'total_storage': total_storage,
                'disk_storage_left': disk_storage_left,
                'cpu_usage': cpu_usage
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