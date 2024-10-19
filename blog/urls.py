from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'blog'

urlpatterns = [
    path("", views.index, name="index" ),
    path("post/<str:slug>", views.detail, name="detail"),
    path("new_something_url", views.new_url_view, name="new_page_url" ),
    path("old_url", views.old_url_redirect, name="old_url" ),
    path("contact", views.contact_view, name="contact" ),
    path("about", views.about_view, name="about" ),
    path("register", views.register_view, name='register'),
    path('login', views.login_view, name='login'),
    path('dashboard', views.dashboard_view, name='dashboard'),
    path('logout', views.logout_view, name='logout'),
]