"""
URL configuration for Smithy project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from BackendWork.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),
    path('signin/', UserSignInView.as_view(), name='UserSignInView'),
    path('register/', UserRegisterView.as_view(), name='UserRegisterView'),
    path('signout/', user_logout, name='user_logout'),
    path('create_character/', create_character, name='create_character'),
    path('characters/<int:character_id>/builder/', include('Smithy.builder_urls')),
    path('dbRace/', ManageRace.as_view(), name='manageRace'),
    path('dbClass/', ManageClass.as_view(), name='manageClass'),
    path('dbCharacter/', ManageCharacter.as_view(), name='manageCharacter'),
]
