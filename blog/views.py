from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.urls import reverse
import logging

from .models import Post, AboutUs
from django.http import Http404
from django.core.paginator import Paginator
from .forms import ContactForm 

# accounts/views.py
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from .forms import RegisterForm, LoginForm
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout

from blog import forms


# Create your views here.

# static demo data
# posts = [
#         {'id':1, 'title': 'Post 1', 'content': 'Content of Post 1'},
#         {'id':2, 'title': 'Post 2', 'content': 'Content of Post 2'},
#         {'id':3, 'title': 'Post 3', 'content': 'Content of Post 3'},
#         {'id':4, 'title': 'Post 4', 'content': 'Content of Post 4'},   
#     ]
def index(request):
    blog_title = "Latest Posts"

    # getting data from post model
    all_posts = Post.objects.all()

    # paginate
    paginator = Paginator(all_posts, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request,'blog/index.html', {'blog_title': blog_title, 'page_obj': page_obj})

def detail(request, slug):
    # static data 
    # post = next((item for item in posts if item['id'] == int(post_id)), None)
    if not (request.user.has_perm('blog.view_post') or request.user.groups.filter(name='Readers').exists()):
        messages.error(request, 'You do not have permission to view any posts.')
        return redirect('blog:dashboard')  # Redirect to the dashboard URL
    try:
        # getting data from model by post id
        post = Post.objects.get(slug=slug)
        related_posts  = Post.objects.filter(category = post.category).exclude(pk=post.id)

    except Post.DoesNotExist:
        raise Http404("Post Does not Exist!")

    # logger = logging.getLogger("TESTING")
    # logger.debug(f'post variable is {post}')=
    return render(request,'blog/detail.html', {'post': post, 'related_posts':related_posts})

def old_url_redirect(request):
    return redirect(reverse('blog:new_page_url'))

def new_url_view(request):
    return HttpResponse("This is the new URL")

def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')

        logger = logging.getLogger("TESTING")
        if form.is_valid():
            logger.debug(f'POST Data is {form.cleaned_data['name']} {form.cleaned_data['email']} {form.cleaned_data['message']}')
            #send email or save in database
            success_message = 'Your Email has been sent!'
            return render(request,'blog/contact.html', {'form':form,'success_message':success_message})
        else:
            logger.debug('Form validation failure')
        return render(request,'blog/contact.html', {'form':form, 'name': name, 'email':email, 'message': message})
    return render(request,'blog/contact.html')

def about(request):
    about_content = AboutUs.objects.first()
    if about_content is None or not about_content.content:
        about_content = "Default content goes here."  # Replace with your desired default string
    else:
        about_content = about_content.content
        
    return render(request,'blog/about.html',{'about_content':about_content})


def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])  # Hash the password
            user.save()
            messages.success(request, 'Registration successful! You can now log in.')
            return redirect('blog:login')  # Redirect to the login page or another page
    else:
        form = RegisterForm()
    return render(request, 'blog/register.html', {'form': form})

def login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                auth_login(request,user)
                return redirect('blog:dashboard')
    else:
        form = LoginForm()
    
    return render(request, 'blog/login.html', {'form': form})

def dashboard(request):
    blog_title = "My Posts"
    return render(request,'blog/dashboard.html', {'blog_title': blog_title})

def logout(request):
    auth_logout(request) 
    return redirect('blog:index')  # Redirect to the Home page 
