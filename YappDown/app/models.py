from django.db import models

# # User table
class User(models.Model):
    user_ID = models.AutoField(primary_key=True)
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=50)
    password = models.CharField(max_length=200)
    salt = models.CharField(max_length=32, blank=True, null=True)
    joinedDate = models.DateTimeField(auto_now_add=True)
    hasAccess = models.BooleanField(default=True)
    admin = models.BooleanField(default=False)

    def __str__(self):
        return self.username
    
# Note table
class Note(models.Model):
    user_ID = models.ForeignKey(User, on_delete=models.CASCADE)
    note_ID = models.AutoField(primary_key=True)
    title = models.CharField(max_length=100)
    content = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    lastUpdated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title