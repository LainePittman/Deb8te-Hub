from django.urls import path
from main import views
from .views import accept_friend_request, decline_friend_request

urlpatterns = [
    path("", views.home, name='home'),
    path("index.html", views.home, name='home'),
    path("auth_form.html", views.auth, name='auth'),
    path("user_index.html", views.usr_home, name='usr_home'),
    path("user_profile.html", views.usr_prof, name='usr_prof'),
    path("user_feed.html/", views.usr_feed, name='usr_feed'),
    path("login_form.html", views.signin, name='login'),
    path('logout', views.leave, name='logout'),
    path('post_comment.html', views.usr_feed, name='comment'),
    path('post_comment/<uuid:postID>/', views.post_comment, name='post_comment'),
    path('add_comment/<uuid:postID>/', views.add_comment, name='add_comment'),
    path('search_results.html', views.search, name='search_results'),
    path('accept_friend_request/<int:request_id>/', accept_friend_request, name='accept_friend_request'),
    path('decline_friend_request/<int:request_id>/', decline_friend_request, name='decline_friend_request'),
]