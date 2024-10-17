from django.db import models

# User table
class User(models.Model):
    user_ID = models.AutoField(primary_key=True)
    username = models.CharField(max_length=50)
    password = models.CharField(max_length=200)
    joinedDate = models.DateTimeField(auto_now_add=True)

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