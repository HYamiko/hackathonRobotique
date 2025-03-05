from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser


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
    filiere = models.CharField(max_length=255)
    niveau_etude= models.CharField( max_length=50)
    can_continue = models.BooleanField(default=True)
    date_inscription = models.DateField(auto_now_add=True)
    object= MyUserManager()
    USERNAME_FIELD = 'telephone'

    def __str__(self):
        return f"{self.nom} {self.prenom}"

class Seance(models.Model):
    date_debut = models.DateTimeField(auto_now_add=True)
    date_fin = models.DateTimeField(auto_now_add = True)
    description = models.TextField(blank=True)

class Presence(models.Model):
    participant = models.ForeignKey(Participant, on_delete=models.CASCADE)
    seance = models.ForeignKey(Seance, on_delete=models.CASCADE)
    presence = models.BooleanField(default=False)


class Groupe(models.Model):
    nom = models.CharField(unique=True, max_length=255)
    participant = models.ForeignKey(Participant, on_delete=models.CASCADE)
    