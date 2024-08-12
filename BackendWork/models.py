from math import floor

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import Sum
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver


class User(AbstractUser):
    email = models.EmailField(unique=True)
    friends = models.ManyToManyField('self', blank=True)

    def get_characters(self):
        return Character.objects.filter(owner=self)


class Proficiency(models.Model):
    profId = models.AutoField(primary_key=True)
    name = models.CharField(max_length=20, unique=True)
    type = models.CharField(max_length=20)

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

    def __str__(self):
        return self.name


class Spell(models.Model):
    pass


class Feature(models.Model):
    featId = models.AutoField(primary_key=True)
    name = models.CharField(max_length=20)
    description = models.CharField(max_length=500)
    levelReq = models.IntegerField()

    def __str__(self):
        return self.name


class Language(models.Model):
    languageId = models.AutoField(primary_key=True)
    name = models.CharField(max_length=20)


class Trait(models.Model):
    traitId = models.AutoField(primary_key=True)
    name = models.CharField(max_length=20)
    description = models.CharField(max_length=200)

    # has_choices = models.BooleanField(default=False)  # Indicates if this trait has options
    def __str__(self):
        return self.name


# class TraitChoice(models.Model):
#     traitChoiceId = models.AutoField(primary_key=True)
#     trait = models.ForeignKey(Trait, on_delete=models.CASCADE, related_name='choices')
#     name = models.CharField(max_length=50)
#     # Add action field. On choice select, add action to character


class Race(models.Model):
    raceId = models.AutoField(primary_key=True)
    raceName = models.CharField(max_length=20)
    speed = models.PositiveIntegerField()
    traits = models.ManyToManyField(Trait, related_name='race')

    def __str__(self):
        return self.raceName


class CharacterClass(models.Model):
    classId = models.AutoField(primary_key=True)
    name = models.CharField(max_length=20, unique=True)
    spellcasting_ability = models.CharField(max_length=20, null=True, blank=True)
    subclassAtLevel = models.IntegerField()

    # spells = models.ManyToManyField(Spell, blank=True)
    features = models.ManyToManyField(Feature, blank=True)

    def is_spellcaster(self):
        return self.spellcasting_ability is not None

    def available_spells(self):
        return self.spells.all() if self.is_spellcaster() else None

    def __str__(self):
        return self.name


class CharacterSubclass(models.Model):
    subclassId = models.AutoField(primary_key=True)
    superClass = models.ForeignKey(CharacterClass, on_delete=models.CASCADE, related_name='characterSubclass')
    name = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return self.name


class Character(models.Model):
    characterId = models.AutoField(primary_key=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='character')
    race = models.ForeignKey(Race, on_delete=models.CASCADE, related_name='character', blank=True, null=True)
    # campaign = models.ForeignKey(campaign=Campaign, on_delete=models.CASCADE, related_name='characters')
    name = models.CharField(max_length=20, blank=True)
    totalLevel = models.IntegerField(blank=True, null=True)
    dex = models.IntegerField(blank=True, null=True)
    str = models.IntegerField(blank=True, null=True)
    con = models.IntegerField(blank=True, null=True)
    wis = models.IntegerField(blank=True, null=True)
    int = models.IntegerField(blank=True, null=True)
    cha = models.IntegerField(blank=True, null=True)
    maxHp = models.IntegerField(blank=True, null=True)
    currentHp = models.IntegerField(blank=True, null=True)
    tempHp = models.IntegerField(default=0)
    proficiencies = models.ManyToManyField(Proficiency)

    def save(self, *args, **kwargs):
        if not self.name:
            self.name = f"{self.owner.username}'s Character"
        super().save(*args, **kwargs)

    def update_total_level(self):
        self.totalLevel = self.classLevel.aggregate(Sum('level'))['level__sum'] or 0
        self.save()

    def get_attr_mod(self, attr):
        if attr == 'dex':
            return int(floor(self.dex / 2))
        if attr == 'str':
            return int(floor(self.str / 2))
        if attr == 'con':
            return int(floor(self.con / 2))
        if attr == 'wis':
            return int(floor(self.wis / 2))
        if attr == 'int':
            return int(floor(self.int / 2))
        if attr == 'cha':
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

    def __str__(self):
        return self.name


class ClassLevel(models.Model):  # Many to Many relationship between character and characterClass with additional level information
    classLvlId = models.AutoField(primary_key=True)
    charClass = models.ForeignKey(CharacterClass, on_delete=models.CASCADE, related_name='classLevel')
    charSubclass = models.ForeignKey(CharacterSubclass, on_delete=models.CASCADE, related_name='classLevel', blank=True,
                                     null=True)
    level = models.IntegerField(default=1)
    character = models.ForeignKey(Character, on_delete=models.CASCADE, related_name='classLevel')

    def __str__(self):
        if self.charSubclass is not None:
            return f"{self.charClass} {self.charSubclass} {self.level} {self.character}"
        else:
            return f"{self.charClass} {self.character}"


@receiver(post_save, sender=ClassLevel)
@receiver(post_delete, sender=ClassLevel)
def update_character_total_level(sender, instance, **kwargs):
    instance.character.update_total_level()
