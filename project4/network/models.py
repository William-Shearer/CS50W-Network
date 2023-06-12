from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    username = models.CharField(max_length = 50, unique = True, blank = False, null = False)
    email = models.EmailField(blank = False, null = False)
    password = models.CharField(max_length = 255, blank = False, null = False)

    def __str__(self):
        return f"Member {self.username}"

class Profile(models.Model):
    member = models.OneToOneField(User, on_delete = models.CASCADE, related_name = "profile_by_member")
    created = models.DateTimeField(auto_now = False, auto_now_add = True)
    biography = models.TextField(blank = True, null = True)
    followed = models.ManyToManyField(User, related_name = "profile_by_followed", blank = True)
    userimage = models.ImageField(upload_to = "images/", blank = True, null = True)

    def __str__(self):
        return f"Profile of {self.member.username} created {self.created.strftime('%Y %m %d')}"

class Post(models.Model):
    author = models.ForeignKey(User, on_delete = models.CASCADE, related_name = "post_by_author")
    subject = models.CharField(max_length = 50, blank = False, null = False)
    content = models.TextField(blank = False, null = False)
    date_created = models.DateTimeField(auto_now = False, auto_now_add = True)
    last_edit = models.DateTimeField(auto_now = True, auto_now_add = False)
    liked = models.ManyToManyField(User, blank = True, related_name = "post_by_liked")

    def __str__(self):
        return f"Post by {self.author.username} about {self.subject}"
