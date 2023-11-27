from django.urls import path
from main import views
from django.contrib.auth import views as auth_views

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
    path('reset_password/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
]