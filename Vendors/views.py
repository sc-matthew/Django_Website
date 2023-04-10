from django.shortcuts import render
from django.views import View
from .middlewares.auth import auth_middleware

class Homepage(View):
    def get(self, request):
        return render(request, 'vendor_landing.html', {})
