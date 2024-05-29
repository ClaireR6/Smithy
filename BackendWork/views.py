import json

from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views import View
from BackendWork.forms import *
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from BackendWork.models import *


def home(request):
    return render(request, 'home.html')


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


@login_required()
def user_logout(request):
    logout(request)
    return redirect('/')


@login_required()
def create_character(request):
    num = Character.objects.filter(owner=request.user).count() + 1
    print(request.user)
    character = Character.objects.create(name=request.user.username + '\'s Character(' + str(num) + ')',
                                         owner=request.user)
    character.save()

    return redirect('builder_base', character_id=character.characterId)


@login_required()
def builder_base(request, character_id):
    return redirect('builder_race', character_id=character_id)


@login_required()
def builder_race(request, character_id):
    races = Race.objects.all()
    character = Character.objects.get(characterId=character_id)
    return render(request, 'builder_base.html',
                  {"character": character, "races": races, "link": 'builder_race.html'})


@login_required()
def builder_class(request, character_id):
    classes = CharacterClass.objects.all().exclude(classLevel__character=character_id)
    character = Character.objects.get(characterId=character_id)
    return render(request, 'builder_base.html',
                  {"character": character, "classes": classes, "link": 'builder_class.html'})


class ManageRace(View):
    @staticmethod
    def post(request):
        raceId = request.POST.get("race_id")
        action = request.POST.get("action")

        if action == "get":
            # send back race speed, size, traits, age
            race = Race.objects.get(raceId=raceId)
            data = {"raceName": race.raceName, "speed": race.speed,
                    "traits": list(race.traits.all().values("name", "description"))}
            return JsonResponse(data, safe=False)


class ManageClass(View):
    @staticmethod
    def post(request):
        classId = request.POST.get("class_id")
        action = request.POST.get("action")

        if action == "get":
            # send back race speed, size, traits, age
            charClass = CharacterClass.objects.get(classId=classId)
            data = {"classInfo": {"classId": charClass.classId, "name": charClass.name},
                    "features": list(charClass.features.all().values("featId", "name", "description", "levelReq"))}
            return JsonResponse(data, safe=False)

        if action == "add": #Changes needed to prevent duplicates
            characterId = request.POST.get("character_id")
            character = Character.objects.get(characterId=characterId)
            charClass = CharacterClass.objects.get(classId=classId)

            classlvl = ClassLevel.objects.filter(charClass=charClass, character=character).first()
            if classlvl:
                return redirect('builder_class', character_id=character.characterId)
            else:
                classlvl = ClassLevel.objects.create(charClass=charClass, character=character)
                classlvl.save()
                return redirect('builder_class', character_id=character.characterId)
