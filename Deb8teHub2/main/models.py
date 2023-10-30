from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    userID = models.IntegerField()
    friend_count = models.IntegerField(default=0)
    like_count = models.IntegerField(default=0)
    comment_count = models.IntegerField(default=0)
    shares_count = models.IntegerField(default=0)

    def __str__(self):
        return self.user.username

class Post(models.Model):
    postID = models.IntegerField()
    content = models.CharField(max_length=100)
    timestamp = models.DateField()
    #on_delete=models.CASCADE ensures posts will be deleted when owner is
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    likes = models.IntegerField()
    shares = models.IntegerField()

class Friend(models.Model):
    user = models.ForeignKey(User, related_name='sender', on_delete=models.CASCADE)
    friend = models.ForeignKey(User, related_name='receiver', on_delete=models.CASCADE)

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    commenter = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.CharField(max_length=100)
