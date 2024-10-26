from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'blog'

urlpatterns = [
    path("", views.index, name="index" ),
    path("post/<str:slug>", views.detail, name="detail"),
    path("new_something_url", views.new_url_view, name="new_page_url" ),
    path("old_url", views.old_url_redirect, name="old_url" ),
    path("contact", views.contact, name="contact" ),
    path("about", views.about, name="about" ),
    path("register", views.register, name='register'),
    path('login', views.login, name='login'),
    path('dashboard', views.dashboard, name='dashboard'),
    path('logout', views.logout, name='logout'),
    path('newpost', views.new_post, name='new_post'),
    path('editpost/<int:post_id>/', views.edit_post, name='edit_post'),
    path('deletepost/<int:post_id>', views.delete_post, name='delete_post'),
    path('publishpost/<int:post_id>', views.publish_post, name='publish_post'),
    path('password_reset/', views.password_reset, name='password_reset'),
    path('reset/<uidb64>/<token>/',views.password_reset_confirm , name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
]