from django.db import models
from django.contrib.auth.models import AbstractBaseUser

from django.contrib.auth.models import User


# Create your models here.
#class user(models.Model):
    #nom = models.CharField(max_length=50)
    #password = models.CharField(max_length=50)

class user (AbstractBaseUser):
    nom = models.CharField(max_length=50)
    password = models.CharField(max_length=50) 

#travail sur vue docteur



    








class Patient(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    telephone = models.CharField(max_length=15)

    def __str__(self):
        return self.user.username

class Medecin(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    specialite = models.CharField(max_length=100)

    def __str__(self):
        return self.user.username

class Secretaire(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username

class RendezVous(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    medecin = models.ForeignKey(Medecin, on_delete=models.CASCADE)
    date_rdv = models.DateTimeField()
    motif = models.CharField(max_length=200)

    def __str__(self):
        return f"RDV de {self.patient.user.username} avec {self.medecin.user.username} le {self.date_rdv}"


