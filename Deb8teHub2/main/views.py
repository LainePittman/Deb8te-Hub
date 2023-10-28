from django.shortcuts import render

# Create your views here.
def home(request):
    return render(request, "index.html", {})

def auth(request):
    return render(request, "auth_form.html", {})

def tmp(request):
    return render(request, "tmp_page_dir.html", {})

def usr_home(request):
    return render(request, "user_index.html", {})

def usr_prof(request):
    return render(request, "user_profile.html", {})

def usr_feed(request):
    return render(request, "user_feed.html", {})