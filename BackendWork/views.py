from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required


def home(request):
    return render(request, 'home.html', )


class UserSignInView(View):
    @staticmethod
    def get(request):
        return render(request, 'signin.html')

    @staticmethod
    def post(request):
        pass

class UserRegisterView(View):
    @staticmethod
    def get(request):
        return render(request, 'register.html')

    def post(request):
        pass