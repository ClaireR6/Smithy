import json

from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views import View
from BackendWork.forms import *
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from BackendWork.models import User


def home(request):
    return render(request, 'home.html', )


class UserSignInView(View):
    @staticmethod
    def get(request):
        return render(request, 'signin.html')

    @staticmethod
    def post(request):
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            # Redirect to a success page
            return redirect('/')
        else:
            # Return an 'invalid login' error message.
            return render(request, 'signin.html', {'error': 'Invalid login credentials.'}, status=401)


class UserRegisterView(View):
    @staticmethod
    def get(request):
        return render(request, 'register.html')

    @staticmethod
    def post(request):
        data = json.loads(request.body)
        username = data.get('username')
        email = data.get('email')
        password1 = data.get('password1')
        password2 = data.get('password2')

        form_data = {
            'email': email,
            'username': username,
            'password1': password1,
            'password2': password2,  # Assuming you want both password fields to have the same value
        }

        form = RegistrationForm(form_data)
        if form.is_valid():
            form.save()
            return JsonResponse({'message': 'Account Registered! Redirecting you to login to sign in...'}, status=200)
        else:
            return JsonResponse({'message': form.errors}, status=401)

def user_logout(request):
    logout(request)
    return redirect('/')