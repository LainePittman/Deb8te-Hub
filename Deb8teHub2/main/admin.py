from django.contrib import admin
from .models import Profile
from .models import Post

# Register your models here.

#adds custom Profile, Post model to admin site view
admin.site.register(Profile)
admin.site.register(Post)