from django.shortcuts import redirect
from django.urls import reverse

class RedirectAuthenticatedUserMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Check if the user is authenticated
        if request.user.is_authenticated:
            # List of paths to check
            paths_to_redirect = [reverse('blog:login'), reverse('blog:register')]
            # If the user is on a login or register page, redirect them
            if request.path in paths_to_redirect:
                return redirect(reverse('blog:index'))  # Change 'home' to your desired URL
        
        response = self.get_response(request)
        return response
from django.shortcuts import redirect
from django.urls import reverse

class RestrictUnauthenticatedUserMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # List of paths to restrict
        restricted_paths = [reverse('blog:dashboard')]  # Add other restricted paths as needed

        # If the user is not authenticated and is trying to access restricted paths
        if not request.user.is_authenticated and request.path in restricted_paths:
            return redirect(reverse('blog:login'))  # Change 'login' to your desired login URL

        response = self.get_response(request)
        return response
