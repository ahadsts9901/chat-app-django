from django.shortcuts import redirect
from django.urls import reverse

class LoginRedirectMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        path = request.path
        exempt_urls = [reverse('login'), reverse('signup'), '/admin/login/']

        if not request.user.is_authenticated and path not in exempt_urls:
            return redirect('login')

        if request.user.is_authenticated and path in exempt_urls:
            return redirect('users')

        return self.get_response(request)
