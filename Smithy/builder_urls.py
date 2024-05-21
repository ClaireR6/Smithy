from django.contrib import admin
from django.urls import path
from BackendWork.views import *


urlpatterns = [
    path('', builder_base, name='builder_base'),
    path('race/', builder_race, name='builder_race'),
    path('class/', builder_class, name='builder_class'),
    # other sub-URLs
]