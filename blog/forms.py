from django import forms
# accounts/forms.py
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from .models import Post, Category

class ContactForm(forms.Form):
    name = forms.CharField(label='Name', max_length=100, required=True)
    email = forms.EmailField(label='Email',  required=True)
    message = forms.CharField(label='Message',  required=True)

class UserRegistrationForm(forms.ModelForm):
    username = forms.CharField(label='username', max_length=100, required=True)
    email = forms.CharField(label='email', max_length=100, required=True)
    password = forms.CharField(label='password', max_length=100, required=True)
    password_confirm = forms.CharField(label='password confirm', max_length=100, required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password_confirm = cleaned_data.get("password_confirm")

        if password and password_confirm and password != password_confirm:
            raise forms.ValidationError("Passwords do not match.")

class UserLoginForm(forms.Form):
    username = forms.CharField(label='username', max_length=100, required=True)
    password = forms.CharField(label='password', max_length=100, required=True)

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get("username")
        password = cleaned_data.get("password")
        if username and password:
                user = authenticate(username=username, password=password)
                if user is None:
                    raise forms.ValidationError("Invalid username or password")
        return cleaned_data

class PostForm(forms.ModelForm):
    title = forms.CharField(label='Title', max_length=200, required=True)
    content = forms.CharField(label='Content',  required=True)
    category = forms.ModelChoiceField(queryset=Category.objects.all(), label='Category', required=True)
    img_url = forms.ImageField(label='Image', required=False)
    class Meta:
        model = Post
        fields = ['title', 'content', 'category', 'img_url']

    def clean(self):
        cleaned_data = super().clean()
        title = cleaned_data.get("title")
        content = cleaned_data.get("content")
        # Custom validation example
        if title and len(title) < 5:
            raise  forms.ValidationError("Title must be at least 5 characters long.")

        if content and len(content) < 10:
            raise  forms.ValidationError("Content must be at least 10 characters long.")
    def save(self, commit=True):
        # Create a Post instance but don't save it yet
        post = super().save(commit=False)
        
        if self.cleaned_data.get('img_url'):
            post.img_url = self.cleaned_data['img_url']
        else:
            post.img_url = 'https://upload.wikimedia.org/wikipedia/commons/1/14/No_Image_Available.jpg'  # Default image URL
        if commit:
            post.save()  # Save the instance to the database
        return post