from django import forms
from django.contrib.auth.forms import UserCreationForm

from django import forms
from django.contrib.auth.models import User
from .models import Secretaire
from .models import Medecin, Patient, RendezVous

class SecretaireCreationForm(forms.ModelForm):
    username = forms.CharField(max_length=150, label="Nom d'utilisateur")
    password = forms.CharField(widget=forms.PasswordInput, label="Mot de passe")

    class Meta:
        model = Secretaire
        fields = []

    def save(self, commit=True):
        user = User.objects.create_user(
            username=self.cleaned_data['username'],
            password=self.cleaned_data['password']
        )
        secretaire = super().save(commit=False)
        secretaire.user = user
        if commit:
            secretaire.save()
        return secretaire




# Formulaire pour la création d'un médecin
from django import forms
from .models import Medecin
from django.contrib.auth.models import User

class MedecinForm(forms.ModelForm):
    username = forms.CharField(max_length=150, label="Nom d'utilisateur")
    password = forms.CharField(widget=forms.PasswordInput, label="Mot de passe")
    specialite = forms.CharField(max_length=100, label="Spécialité")
    email = forms.EmailField(label="Email")

    class Meta:
        model = Medecin
        fields = ['specialite']  # Inclure uniquement les champs nécessaires au modèle Medecin

    def save(self, commit=True):
        # Créer un nouvel utilisateur avec username et password
        user = User.objects.create_user(
            username=self.cleaned_data['username'],
            password=self.cleaned_data['password']
        )
        # Associer l'utilisateur au médecin
        medecin = super().save(commit=False)
        medecin.user = user
        if commit:
            medecin.save()
        return medecin

#class MedecinForm(forms.ModelForm):
    #class Meta:
        #model = Medecin
        #fields = [ 'specialite']

    #user_username = forms.CharField(max_length=150, label="Nom d'utilisateur")
    #user_password = forms.CharField(widget=forms.PasswordInput, label="Mot de passe")

# Formulaire pour la création d'un patient
#class PatientForm(forms.ModelForm):
    #class Meta:
        #model = Patient
        #fields = ['telephone']

    #user_username = forms.CharField(max_length=150, label="Nom d'utilisateur")
    #user_password = forms.CharField(widget=forms.PasswordInput, label="Mot de passe")

class PatientForm(forms.ModelForm):
    username = forms.CharField(max_length=150, label="Nom d'utilisateur")
    password = forms.CharField(widget=forms.PasswordInput, label="Mot de passe")
    telephone = forms.CharField(max_length=15, label="Téléphone")
    email = forms.EmailField(label="Email")
    class Meta:
        model = Patient
        fields = ['telephone']  # Inclure seulement les champs spécifiques au patient

    def save(self, commit=True):
        # Créer un utilisateur
        user = User.objects.create_user(
            username=self.cleaned_data['username'],
            password=self.cleaned_data['password'],
            email = self.cleaned_data['email']
        )
        # Associer l'utilisateur au patient
        patient = super().save(commit=False)
        patient.user = user
        if commit:
            patient.save()
        return patient

# Formulaire pour la création ou mise à jour d'un rendez-vous
"""class RendezVousForm(forms.ModelForm):
    class Meta:
        model = RendezVous
        fields = ['patient', 'medecin', 'date_rdv', 'motif']
        widgets = {
            'date_rdv': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }
"""
from django.utils.timezone import now  # Utilisé pour comparer avec la date actuelle
from django.core.exceptions import ValidationError

class RendezVousForm(forms.ModelForm):
    class Meta:
        model = RendezVous
        fields = ['patient', 'medecin', 'date_rdv', 'motif']
        widgets = {
            'date_rdv': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }

    def clean_date_rdv(self):
        date_rdv = self.cleaned_data['date_rdv']

        # Validation 1 : La date ne doit pas être dans le passé
        if date_rdv < now():
            raise ValidationError("La date du rendez-vous ne peut pas être dans le passé.")
        return date_rdv

    def clean(self):
        cleaned_data = super().clean()
        date_rdv = cleaned_data.get('date_rdv')
        medecin = cleaned_data.get('medecin')

        # Validation 2 : Vérifier si un rendez-vous existe déjà à cette date et heure pour le médecin
        if medecin and date_rdv:
            rendezvous_existants = RendezVous.objects.filter(
                medecin=medecin,
                date_rdv=date_rdv
            )
            if rendezvous_existants.exists():
                raise ValidationError("Ce médecin a déjà un rendez-vous à cette date et heure.")
        return cleaned_data

