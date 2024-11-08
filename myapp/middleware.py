from django.urls import reverse
from django.shortcuts import redirect

class RedirectAuthenticatedUserMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        #check the user is authenticated
        if request.user.is_authenticated:
            #List of paths to check
            paths_to_redirect = [reverse('blog:login'), reverse('blog:register')]

            if request.path in paths_to_redirect:
                return redirect(reverse('blog:index')) #change to home page
            
        response = self.get_response(request)
        return response