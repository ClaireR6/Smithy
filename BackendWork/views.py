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
    character = Character.objects.create(owner=request.user)
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
            data = {"raceInfo": {"raceId": race.raceId, "raceName": race.raceName, "speed": race.speed},
                    "traits": list(race.traits.all().values("traitId", "name", "description"))}
            return JsonResponse(data, safe=False)
        if action == "set":
            characterId = request.POST.get("character_id")
            character = Character.objects.get(characterId=characterId)
            race = Race.objects.get(raceId=raceId)
            character.race = race
            character.save()
            return redirect('builder_race', character_id=character.characterId)


class ManageClass(View):
    @staticmethod
    def post(request):
        classId = request.POST.get("class_id")
        characterId = request.POST.get("character_id")
        character = Character.objects.get(characterId=characterId)
        action = request.POST.get("action")

        if action == "get":
            # send back race speed, size, traits, age
            charClass = CharacterClass.objects.get(classId=classId)
            data = {"classInfo": {"classId": charClass.classId, "name": charClass.name},
                    "features": list(charClass.features.all().values("featId", "name", "description", "levelReq"))}
            return JsonResponse(data, safe=False)

        if action == "add":  # Changes needed to prevent duplicates
            charClass = CharacterClass.objects.get(classId=classId)

            classLvl = ClassLevel.objects.filter(charClass=charClass, character=character).first()
            if classLvl:
                return redirect('builder_class', character_id=characterId)
            else:
                classLvl = ClassLevel.objects.create(charClass=charClass, character=character)
                classLvl.save()
                return redirect('builder_class', character_id=characterId)

        if action == "level":  # Change in level
            classLvlId = request.POST.get("classlvl_id")
            classLvl = ClassLevel.objects.get(classLvlId=classLvlId, character=character)
            if not classLvl:  # Ensure character has associated classLvl
                return JsonResponse({'error': 'Invalid class level'}, status=400)

            newLevel = int(request.POST.get("level"))
            if character.totalLevel - classLvl.level + newLevel > 20:  # Condition in case of tampering with input options
                return JsonResponse({'error': 'New level exceeds level limit'}, status=400)

            classLvl.level = newLevel
            classLvl.save()
            return redirect('builder_class', character_id=character.characterId)

        if action == "remove":  # Remove class level
            classLvlId = request.POST.get("classlvl_id")
            classLvl = ClassLevel.objects.get(classLvlId=classLvlId, character=character)
            if classLvl:
                classLvl.delete()
                return redirect('builder_class', character_id=character.characterId)

            return JsonResponse({'error': 'Class Level does not exist'}, status=400)


class ManageCharacter(View):
    @staticmethod
    def get(request):
        pass

    @staticmethod
    def post(request):
        characterId = request.POST.get("character_id")
        action = request.POST.get("action")

        if action == "remove":
            character = Character.objects.filter(characterId=characterId).first()
            if character:
                character.delete()
                return JsonResponse({'message': 'Character successfully deleted'}, status=200)
            else:
                return JsonResponse({'message': 'Character does not exist'}, status=400)
