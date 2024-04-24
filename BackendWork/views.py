from django.shortcuts import render, redirect
from django.views import View

def home(request):
    return render(request, 'home.html', )