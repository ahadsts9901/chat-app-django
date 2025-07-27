from django.shortcuts import redirect
from django.urls import reverse

class LoginRedirectMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        path = request.path

        # List of paths or prefixes that are allowed without login
        exempt_paths_exact = [reverse('login'), reverse('signup')]
        exempt_paths_prefixes = ['/admin/']  # ✅ allow all admin URLs

        # Allow if path starts with any of the exempt prefixes
        if not request.user.is_authenticated:
            if path in exempt_paths_exact or any(path.startswith(prefix) for prefix in exempt_paths_prefixes):
                pass
            else:
                return redirect('login')

        # Redirect logged-in users away from login/signup
        if request.user.is_authenticated and path in exempt_paths_exact:
            return redirect('users')

        return self.get_response(request)
