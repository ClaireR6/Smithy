from django.contrib.auth import admin
from django.contrib import admin
from .forms import UserCreationForm as UserCreationForm
from .models import *


class ClassLevelInline(admin.TabularInline):
    model = ClassLevel
    extra = 1  # Number of extra inline forms to display
    fields = ['charClass', 'level']


class CharacterAdmin(admin.ModelAdmin):
    inlines = [ClassLevelInline]


admin.site.register(Character, CharacterAdmin)

admin.site.register(User)
admin.site.register(CharacterClass)
admin.site.register(CharacterSubclass)
admin.site.register(ClassLevel)
admin.site.register(Proficiency)
