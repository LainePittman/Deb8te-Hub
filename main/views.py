from django.shortcuts import render, get_object_or_404
from django.shortcuts import redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from .models import Profile, Friend, Comment, Post, FriendRequest

def accept_friend_request(request, request_id):
    # Your implementation for accepting friend request
    return HttpResponse(f'Accept friend request with ID {request_id}')

def decline_friend_request(request, request_id):
    # Your implementation for declining friend request
    return HttpResponse(f'Decline friend request with ID {request_id}')


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
    user_prof = Profile.objects.get(user=request.user)
    

    # Handle accepting or declining friend requests
    if request.method == 'POST':
        if 'accept_request' in request.POST or 'decline_request' in request.POST:
            friend_request_id = request.POST.get('friend_request_id')

            try:
                friend_request = FriendRequest.objects.get(id=friend_request_id)

                if friend_request.receiver == request.user:
                    if 'accept_request' in request.POST:
                        # Accept the friend request
                        Friend.objects.create(user=request.user, friend=friend_request.sender)
                        friend_request.accepted = True
                        friend_request.save()
                        messages.success(request, f"You are now friends with {friend_request.sender.username}.")
                    elif 'decline_request' in request.POST:
                        # Decline the friend request
                        friend_request.delete()
                        messages.info(request, f"You declined the friend request from {friend_request.sender.username}.")
                else:
                    messages.error(request, "Invalid friend request.")

            except FriendRequest.DoesNotExist:
                messages.error(request, "Friend request not found.")

    # Get the user's friend requests
    friend_requests = FriendRequest.objects.filter(receiver=request.user, accepted=False)

    return render(request, "user_profile.html", {'user': request.user, 'user_prof': user_prof, 'friend_requests': friend_requests})

@login_required(login_url='login_form.html')
def usr_feed(request):

    user_prof = Profile.objects.get(user=request.user)
   
    # Attempt to grab user posts
    try:
        user_post = Post.objects.filter(owner=request.user)
    # Make none if none exist
    except Post.DoesNotExist:
        user_post = None
    
    #If request comes from form submission
    if request.method == 'POST':
        if 'content' in request.POST:
            # Store create post variables
            post_content = request.POST.get('content', '')

            # Generate post
            post = Post.objects.create(content=post_content, owner=request.user)
            post.save()

        elif 'friend_username' in request.POST:

            # Handle friend request
            friend_username = request.POST['friend_username']

            try:
                friend_user = User.objects.get(username= friend_username)

                #Check if already friends
                if not Friend.objects.filter(user=request.user, friend=friend_user).exists():
                    Friend.objects.create(user=request.user, friend=friend_user)

            except User.DoesNotExist:
                messages.info(request, "No one's here")\

            except IntegrityError:
                #already friends
                messages.info(request, "Friend Request Already Sent")


        return render(request, "user_feed.html", {'user_prof':user_prof,'user_post':user_post})
        

    elif request.method == 'POST' and 'comment' in request.POST:

        comment_content = request.POST['comment']

        comment = Comment.objects.create(commentID=post, commenter=request.user, com_comment=comment_content)
        comment.save()

        #attempts to grab user posts
        try:
            user_comment = Comment.objects.filter(commenter=request.user)
        #make none if none exist
        except Comment.DoesNotExist:
            user_comment = None

        return render(request, "user_feed.html", {'user_prof':user_prof,'user_comment':user_comment})

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
            return redirect('user_feed.html')
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

def post_comment(request, postID):

    post = get_object_or_404(Post, postID=postID)

    comments = Comment.objects.filter(commentID=post)

    return render(request, "post_comment.html", {'post': post, 'comments': comments})


def add_comment(request, postID):

    post = get_object_or_404(Post, postID=postID)

    comment_content = request.POST.get('comment')

    Comment.objects.create(commentID=post, commenter=request.user, com_comment=comment_content)

    return redirect('post_comment', postID=postID)


def search(request):
    if request.method == 'POST':
        user_search = request.POST.get('user_search')
        search_results = Profile.objects.filter(user__username__icontains=user_search)

        return render(request, "search_results.html", {'search_results': search_results})

    return render(request, "user_profile.html")


    
