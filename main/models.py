from django.db import models
from django.contrib.auth.models import User
import uuid
from datetime import datetime

# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    userID = models.IntegerField()
    friend_count = models.IntegerField(default=0)
    like_count = models.IntegerField(default=0)
    comment_count = models.IntegerField(default=0)

    def __str__(self):
        return self.user.username

class Post(models.Model):
    #postID is the primary key of Post
    postID = models.UUIDField(primary_key=True, default=uuid.uuid4)
    content = models.CharField(max_length=100)
    timestamp = models.DateTimeField(default=datetime.now)
    #on_delete=models.CASCADE ensures posts will be deleted when owner is
    owner = models.ForeignKey(User, on_delete=models.CASCADE) 
    likes = models.IntegerField(default=0)

    def __str__(self):
        return self.owner.username

class Friend(models.Model):
    user = models.ForeignKey(User, related_name='sender', on_delete=models.CASCADE)
    user = models.CharField(max_length=100) #added by bo
    friend = models.ForeignKey(User, related_name='receiver', on_delete=models.CASCADE)
    friend = models.CharField(max_length=100) #added by bo

    #added by bo
    def __str__(self):
        return self.user
    



class Comment(models.Model):
    commentID = models.ForeignKey(Post, on_delete=models.CASCADE, default="defcom_ID")
    commenter = models.ForeignKey(User, on_delete=models.CASCADE)
    com_comment = models.CharField(max_length=100, default="default_comment")

class Search(models.Model):
    user_search = models.CharField(max_length=50)

class Share(models.Model):
    #User who has shared a post
    sharer = models.ForeignKey(User, on_delete=models.CASCADE)
    #Post that the users has shared
    share = models.ForeignKey(Post, on_delete=models.CASCADE)
    #This creates a 1 to M relationship where 1 user may have many shared posts