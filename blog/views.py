from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.urls import reverse
import logging

from django.views import View
from .models import Post, AboutUs, Category
from django.http import Http404
from django.core.paginator import Paginator
from .forms import ContactForm, PasswordResetRequestForm, SetNewPasswordForm
from django.contrib.auth.views import PasswordResetView
from django.urls import reverse_lazy
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth import update_session_auth_hash




# accounts/views.py
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from .forms import UserRegistrationForm, UserLoginForm, PostForm
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.decorators import login_required
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_str

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

def contact_view(request):
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

def about_view(request):
    about_content = AboutUs.objects.first()
    if about_content is None or not about_content.content:
        about_content = "Default content goes here."  # Replace with your desired default string
    else:
        about_content = about_content.content
        
    return render(request,'blog/about.html',{'about_content':about_content})


def register_view(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])  # Hash the password
            user.save()
            messages.success(request, 'Registration successful! You can now log in.')
            return redirect('/login')  # Redirect to the login page or another page
    else:
        form = UserRegistrationForm()
    
    return render(request, 'blog/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                auth_login(request,user)
                return redirect('blog:dashboard')
    else:
        form = UserLoginForm()
    
    return render(request, 'blog/login.html', {'form': form})

def dashboard_view(request):
    blog_title = "My Posts"

    # getting data from post model
    all_posts = Post.objects.filter(user=request.user)  # Retrieve posts created by the logged-in user

    # paginate
    paginator = Paginator(all_posts, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request,'blog/dashboard.html', {'blog_title': blog_title, 'page_obj': page_obj})

from django.contrib.auth import logout

def logout_view(request):
    logout(request)  # Logs out the user
    return redirect('/login')  # Redirect to the login page or home page

@login_required
def newpost_view(request):
    categories = Category.objects.all()
    
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user  # Set the author to the logged-in user
            post.save()
            return redirect('blog:dashboard')  # Change 'blog:dashboard' to your dashboard URL name
        else:
            print("Form errors:", form.errors)  # Debug line for form errors
    else:
        form = PostForm()
    return render(request,'blog/newpost.html', {'categories':categories,'form': form})  # Redirect to the login page or home page

@login_required
def editpost_view(request, post_id):
    post = get_object_or_404(Post, id=post_id)  # Fetch the post by ID
    categories = Category.objects.all()  # Fetch all categories
    
    if request.method == "POST":
        form = PostForm(request.POST,request.FILES, instance=post)  # Bind the form to the post instance
        if form.is_valid():
            form.save()  # Save the updated Post instance
            return redirect('blog:dashboard')  # Redirect after saving
    else:
        form = PostForm(instance=post)  # Pre-fill the form with the current post data
    
    return render(request, 'blog/editpost.html', {'form': form, 'categories': categories, 'post': post})

def deletepost(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    post.delete()
    messages.success(request, 'Post Deleted!')
    return redirect('blog:dashboard')

def password_reset(request):
    form = PasswordResetRequestForm()
    if request.method == 'POST':
        form = PasswordResetRequestForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data["email"]
            user = User.objects.get(email=email)
            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            current_site = get_current_site(request)
            subject = "Password Reset Requested"
            message = render_to_string('blog/reset_email.html', {
                'email': user.email,
                'domain': current_site.domain,
                'uid': uid,
                'token': token,
            })
            send_mail(subject, message, 'noreply@example.com', [email])
            messages.success(request, 'Email has been sent.')
    return render(request, 'blog/password_reset_request.html', {'form': form}) 
    

def password_reset_confirm(request, uidb64, token):
    if request.method == 'POST':
        form = SetNewPasswordForm(request.POST)

        if form.is_valid():
            new_password = form.cleaned_data['new_password']
            # Decode the uidb64 to get the user ID
            try:
                uid = force_str(urlsafe_base64_decode(uidb64))
                user = User.objects.get(pk=uid)
            except (TypeError, ValueError, OverflowError, User.DoesNotExist):
                user = None

            if user is not None and default_token_generator.check_token(user, token):
                user.set_password(new_password)
                user.save()
                update_session_auth_hash(request, user)  # Keep the user logged in
                messages.success(request, 'Your password has been reset successfully.')
                return redirect('blog:login')
            else:
                messages.error(request, 'The password reset link is invalid.')
    else:
        form = SetNewPasswordForm()

    return render(request, 'blog/reset_confirm.html', {'form': form})