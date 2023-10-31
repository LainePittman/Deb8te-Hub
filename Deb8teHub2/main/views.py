from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from .models import Profile
from .models import Post

# Create your views here.
def home(request):
    return render(request, "index.html", {})

def auth(request):

    #If request comes form submission
    if request.method == 'POST':
        #Store signup variables
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']

        #Catch username already exists exception
        if User.objects.filter(username=username).exists():
            messages.info(request, 'Username Taken')
            return redirect('auth_form.html')
        else:
            #Catch email already used exception
            if User.objects.filter(email=email).exists():
                messages.info(request,'Email Taken')
                return redirect('auth_form.html')
            #Create new user account based upon signup variables
            else:
                user = User.objects.create_user(username=username, email=email, password=password)
                user.save()

                #log user in and redirect to user index page
                user_login = authenticate(username=username,password=password)
                login(request,user_login)

                #create profile object for new user
                user_model = User.objects.get(username=username)
                new_profile = Profile.objects.create(user=user_model, userID=user_model.id)
                new_profile.save()
                return redirect('user_index.html')

                

    else:
        return render(request, "auth_form.html", {})

#@login_required ensures only logged in users can access page
#redirects to login_form.html if not logged in already
@login_required(login_url='login_form.html')
def usr_home(request):
    
    #retrieve user profile
    user_prof = Profile.objects.get(user=request.user)

    #attempts to grab all posts
    try:
        all_posts = Post.objects.all()
    #make none if none exist
    except Post.DoesNotExist:
        all_posts = None

    return render(request, "user_index.html", {'user_prof':user_prof, 'all_posts':all_posts})

@login_required(login_url='login_form.html')
def usr_prof(request):

    #If request comes from form submission
    if request.method == 'POST':

        #store manage details variables
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']

        #Catch username already exists exception
        if User.objects.filter(username=username).exists():
            messages.info(request, 'Username Taken')
            return redirect('user_profile.html')
        else:
            #Catch email already used exception
            if User.objects.filter(email=email).exists():
                messages.info(request,'Email Taken')
                return redirect('user_profile.html')
            #Update user account based upon signup variables
            else:
                #Get request user
                user = request.user
                #Change user's attributes
                user.username = username
                user.email = email
                user.set_password(password)
                #Save changes to user object
                user.save()

                #logout user for them to reauthenticate
                logout(request)
                return redirect('login_form.html')
                




    else:
        user_prof = Profile.objects.get(user=request.user)
        return render(request, "user_profile.html", {'user_prof':user_prof})

@login_required(login_url='login_form.html')
def usr_feed(request):

    #If request comes from form submission
    if request.method == 'POST':

        #store create post variables
        post_content = request.POST['content']

        #generate post
        post = Post.objects.create(content=post_content,owner=request.user)
        post.save()

        user_prof = Profile.objects.get(user=request.user)

        #attempts to grab user posts
        try:
            user_post = Post.objects.filter(owner=request.user)
        #make none if none exist
        except Post.DoesNotExist:
            user_post = None

        return render(request, "user_feed.html", {'user_prof':user_prof,'user_post':user_post})

    else:

        user_prof = Profile.objects.get(user=request.user)

        #attempts to grab user posts
        try:
            user_post = Post.objects.filter(owner=request.user)
        #make none if none exist
        except Post.DoesNotExist:
            user_post = None

        return render(request, "user_feed.html", {'user_prof':user_prof,'user_post':user_post})

def signin(request):

    #If request comes from form submission
    if request.method == 'POST':
        #Store login variables
        username = request.POST['username']
        password = request.POST['password']

        #returns user object if valid username/password
        user = authenticate(username=username,password=password)

        #if user object exists
        if user is not None:
            #login
            login(request,user)
            return redirect('user_index.html')
        #if not
        else:
            #report invalid credentials
            messages.info(request, 'Invalid Credentials')
            return redirect('login_form.html')

    else:
        return render(request, "login_form.html", {})

@login_required(login_url='login_form.html')    
def leave(request):
    logout(request)
    return redirect('login_form.html')