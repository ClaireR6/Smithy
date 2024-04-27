from math import floor

from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    email = models.EmailField(unique=True)
    friends = models.ManyToManyField('self', blank=True)


class Proficiency(models.Model):
    ARMOR_CHOICES = (
        ('light', 'Light Armor'),
        ('medium', 'Medium Armor'),
        ('heavy', 'Heavy Armor'),
        ('shield', 'Shield'),
    )

    WEAPON_CHOICES = (
        ('simple', 'Simple Weapons'),
        ('martial', 'Martial Weapons'),
    )

    TOOL_CHOICES = (
        ('artisan', 'Artisan\'s Tools'),
        ('disguise_kit', 'Disguise Kit'),
        ('forgery_kit', 'Forgery Kit'),
        ('gaming_set', 'Gaming Set'),
        ('herbalism_kit', 'Herbalism Kit'),
        ('navigators_tools', 'Navigator\'s Tools'),
        ('poisoners_kit', 'Poisoner\'s Kit'),
        ('thieves_tools', 'Thieves\' Tools'),
    )

    SAVING_THROW_CHOICES = (
        ('str', 'Strength'),
        ('dex', 'Dexterity'),
        ('con', 'Constitution'),
        ('wis', 'Wisdom'),
        ('int', 'Intelligence'),
        ('cha', 'Charisma')
    )

    SKILL_CHOICES = (
        ('acrobatics', 'Acrobatics'),
        ('animal_handling', 'Animal Handling'),
        ('arcana', 'Arcana'),
        ('athletics', 'Athletics'),
        ('deception', 'Deception'),
        ('history', 'History'),
        ('insight', 'Insight'),
        ('intimidation', 'Intimidation'),
        ('investigation', 'Investigation'),
        ('medicine', 'Medicine'),
        ('nature', 'Nature'),
        ('perception', 'Perception'),
        ('performance', 'Performance'),
        ('persuasion', 'Persuasion'),
        ('religion', 'Religion'),
        ('sleight_of_hand', 'Sleight of Hand'),
        ('stealth', 'Stealth'),
        ('survival', 'Survival'),
    )

    INSTRUMENT_CHOICES = (
        # Add your instrument choices here
    )

    PROFICIENCY_TYPES = (
        ('armor', 'Armor'),
        ('weapons', 'Weapons'),
        ('tools', 'Tools'),
        ('saving throws', 'Saving Throws'),
        ('skills', 'Skills'),
        ('instrument', 'Instrument'),
    )

    profId = models.AutoField(primary_key=True)
    type = models.CharField(max_length=10, choices=PROFICIENCY_TYPES)
    subtype = models.CharField(max_length=20, choices=(), blank=True)

    def save(self, *args, **kwargs):
        if self.type == 'armor':
            self.subtype = models.CharField(max_length=10, choices=self.ARMOR_CHOICES)
        elif self.type == 'weapons':
            self.subtype = models.CharField(max_length=10, choices=self.WEAPON_CHOICES)
        elif self.type == 'tools':
            self.subtype = models.CharField(max_length=20, choices=self.TOOL_CHOICES)
        elif self.type == 'saving throws':
            self.subtype = models.CharField(max_length=20, choices=self.SAVING_THROW_CHOICES)
        elif self.type == 'skills':
            self.subtype = models.CharField(max_length=20, choices=self.SKILL_CHOICES)
        elif self.type == 'instrument':
            self.subtype = models.CharField(max_length=20, choices=self.INSTRUMENT_CHOICES)

        super().save(*args, **kwargs)


class Spell:
    pass


class Feat:
    pass


class CharacterClass(models.Model):
    classId = models.AutoField(primary_key=True)
    name = models.CharField(max_length=20, unique=True)
    spellcasting_ability = models.CharField(max_length=20, null=True, blank=True)
    spells = models.ManyToManyField(Spell, blank=True)
    features = models.ManyToManyField(Feat, blank=True)

    def is_spellcaster(self):
        return self.spellcasting_ability is not None

    def available_spells(self):
        return self.spells.all() if self.is_spellcaster() else None

class CharacterSubclass(models.Model):
    subclassId = models.AutoField(primary_key=True)
    superClass = models.ForeignKey(CharacterClass, on_delete=models.CASCADE)
    name = models.CharField(max_length=20, unique=True)

class Character(models.Model):
    characterId = models.AutoField(primary_key=True)
    owner = models.ForeignKey(user=User, on_delete=models.CASCADE)
    # campaign = models.ForeignKey(campaign=Campaign, on_delete=models.CASCADE)
    name = models.CharField(max_length=20)
    totalLevel = models.IntegerField()
    dex = models.IntegerField()
    str = models.IntegerField()
    con = models.IntegerField()
    wis = models.IntegerField()
    int = models.IntegerField()
    cha = models.IntegerField()
    speed = models.IntegerField()
    maxHp = models.IntegerField()
    currentHp = models.IntegerField(default=maxHp)
    tempHp = models.IntegerField(default=0)
    proficiencies = models.ManyToManyField(Proficiency)

    def get_attr_mod(self, attr):
        if attr is 'dex':
            return int(floor(self.dex / 2))
        if attr is 'str':
            return int(floor(self.str / 2))
        if attr is 'con':
            return int(floor(self.con / 2))
        if attr is 'wis':
            return int(floor(self.wis / 2))
        if attr is 'int':
            return int(floor(self.int / 2))
        if attr is 'cha':
            return int(floor(self.cha / 2))

    @property
    def get_prof_bonus(self):
        if self.totalLevel < 5:
            return 2
        elif self.totalLevel < 9:
            return 3
        elif self.totalLevel < 13:
            return 4
        elif self.totalLevel < 17:
            return 5
        else:
            return 6


class ClassLevel(models.Model):
    classLvlId = models.AutoField(primary_key=True)
    charClass = models.ForeignKey(CharacterClass, on_delete=models.CASCADE)
    level = models.IntegerField(default=1)
    character = models.ForeignKey(Character, on_delete=models.CASCADE)
