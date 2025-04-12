from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
import random
import string

class MyUserManager(BaseUserManager):
    
    def create_user(self, telephone, email, password=None, **extra_fields):
        if not telephone:
            raise ValueError('Le champ numéro de téléphone est obligatoire.')
        if not password:
            raise ValueError('Le champ mot de passe est obligatoire.')

        if email:
            email= self.normalize_email(email)
            
        user = self.model(telephone=telephone, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user


    def create_superuser(self, telephone, password=None, **extra_fields):
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_active',True)
        return self.create_user(telephone, password, **extra_fields)
    
    
class Participant(AbstractBaseUser):
    ine = models.CharField(max_length=25)
    nom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    telephone = models.CharField(unique=True, max_length=15)
    genre = models.CharField(max_length=50)
    etablissement = models.CharField(max_length=255)
    profession=models.CharField(max_length=255)
    niveau_etude= models.CharField( max_length=50)
    can_continue = models.BooleanField(default=True)
    date_inscription = models.DateField(auto_now_add=True)
    objects= MyUserManager()
    USERNAME_FIELD = 'telephone'

    def __str__(self):
        return f"{self.nom} {self.prenom}"
    
class Activite(models.Model):
    libelle = models.CharField(max_length=255)
    code = models.CharField(max_length=8, unique=True)  
    
    def __str__(self):
        return f"{self.libelle} ({self.code})"
    
    def save(self, *args, **kwargs):
        if not self.code:  
            self.code = self.generate_unique_code()
        super().save(*args, **kwargs)
    
    @classmethod
    def generate_unique_code(cls, length=6):
        while True:
            letters = ''.join(random.choices(string.ascii_uppercase, k=2))
            numbers = ''.join(random.choices(string.digits, k=4))
            code = f"{letters}{numbers}"
            
            if not cls.objects.filter(code=code).exists():
                return code
    
class Seance(models.Model):
    activite = models.ForeignKey(Activite, on_delete=models.CASCADE)
    titre=models.CharField(max_length=255, blank=True, null=True)
    date_debut = models.DateTimeField(auto_now_add=True)
    date_fin = models.DateTimeField(auto_now_add = True)
    description = models.TextField(blank=True, null=True)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)

class Presence(models.Model):
    participant = models.ForeignKey(Participant, on_delete=models.CASCADE)
    seance = models.ForeignKey(Seance, on_delete=models.CASCADE)
    presence = models.BooleanField(default=False)
    adresse_ip = models.GenericIPAddressField(null=True, blank=True)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    heure = models.DateTimeField(auto_now_add=True)


class Groupe(models.Model):
    nom = models.CharField(unique=True, max_length=255)
    participant = models.ForeignKey(Participant, on_delete=models.CASCADE)
    