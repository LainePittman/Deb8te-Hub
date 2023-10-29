from django.contrib import admin
from .models import Profile

# Register your models here.

#adds custom Profile model to admin site view
admin.site.register(Profile)