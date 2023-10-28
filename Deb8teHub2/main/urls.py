from django.urls import path
from main import views

urlpatterns = [
    path("", views.home, name='home'),
    path("index.html", views.home, name='home'),
    path("auth_form.html", views.auth, name='auth'),
    path("tmp_page_dir.html", views.tmp, name='tmp'),
    path("user_index.html", views.usr_home, name='usr_home'),
    path("user_profile.html", views.usr_prof, name='usr_prof'),
    path("user_feed.html", views.usr_feed, name='usr_feed'),
]