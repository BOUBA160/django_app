from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm

from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated


from .models import Medecin, Patient, RendezVous

from .forms import RendezVousForm, MedecinForm, PatientForm


#class ProtectedView(APIView):
   # permission_classes = [IsAuthenticated]

    #def get(self, request):
        #return Response({"message": "Vous avez accès à cette vue protégée !"})

from rest_framework.renderers import JSONRenderer

class ProtectedView(APIView):
    permission_classes = [IsAuthenticated]
    renderer_classes = [JSONRenderer]  # Limiter le rendu au format JSON

    def get(self, request, *args, **kwargs):
        return Response({"message": "Réponse JSON depuis la vue protégée."}, status=200)

#creation des roles 
from django.core.exceptions import PermissionDenied

def role_requis_secretaire(view_func):
    def wrapper(request, *args, **kwargs):
        if not hasattr(request.user, 'secretaire'):
            raise PermissionDenied
        return view_func(request, *args, **kwargs)
    return wrapper

def role_requis_medecin(view_func):
    def wrapper(request, *args, **kwargs):
        if not hasattr(request.user, 'medecin'):
            raise PermissionDenied
        return view_func(request, *args, **kwargs)
    return wrapper

def role_requis_patient(view_func):
    def wrapper(request, *args, **kwargs):
        if not hasattr(request.user, 'patient'):
            raise PermissionDenied
        return view_func(request, *args, **kwargs)
    return wrapper
# Create your views here.

def connexion(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            # Redirection basée sur le rôle
            if hasattr(user, 'secretaire'):
                return redirect('vue_secretaire')
            elif hasattr(user, 'medecin'):
                return redirect('vue_medecin')
            elif hasattr(user, 'patient'):
                return redirect('vue_patient')
            else:
                return redirect('accueil')  # Page par défaut
        else:
            messages.error(request, "Nom d'utilisateur ou mot de passe incorrect.")
    return render(request, 'connexion.html')

#def connexion(request):
 #   if request.method == 'POST':
 #       username = request.POST['username']
  #      password = request.POST['password']
   #     user = authenticate(request, username=username, password=password)
    #    if user is not None:
     #       login(request, user)
      #      return redirect('vue_medecin')
       # else:
        #    messages.error(request, 'Nom d\'utilisateur ou mot de passe incorrect.')
    #return render(request, 'connexion.html')

@login_required
#def acceuil(request):
 #   return render(request, 'acceuil.html')

def deconnexion(request):
    logout(request)
    return redirect('connexion')


from django.http import HttpResponse
from .forms import SecretaireCreationForm

def inscription_secretaire(request):
    if request.method == "POST":
        form = SecretaireCreationForm(request.POST)
        if form.is_valid():
            form.save()  # Sauvegarde le formulaire et crée l'utilisateur associé
            return HttpResponse("Secrétaire inscrite avec succès !")
    else:
        form = SecretaireCreationForm()

    return render(request, "inscription_secretaire.html", {"form": form})



#vue medcin


@login_required
@role_requis_medecin
def vue_medecin(request):
    medecin = request.user.medecin
    rendezvous = RendezVous.objects.filter(medecin=medecin)
    patients = Patient.objects.filter(rendezvous__medecin=medecin).distinct()

    context = {
        'rendezvous': rendezvous,
        'patients': patients,
    }
    return render(request, 'vuemedcin.html', context)



#vue secertaire




@login_required
@role_requis_secretaire
def vue_secretaire(request):
    medecins = Medecin.objects.all()
    patients = Patient.objects.all()
    rendezvous = RendezVous.objects.all()

    context = {
        'medecins': medecins,
        'patients': patients,
        'rendezvous': rendezvous,
    }
    return render(request, 'vue_secretaire.html', context)

@login_required
def creer_rendezvous(request):
    if request.method == 'POST':
        form = RendezVousForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('vue_secretaire')
    else:
        form = RendezVousForm()
    return render(request, 'creer_rendezvous.html', {'form': form})

@login_required

def creer_medecin(request):
    if request.method == 'POST':
        form = MedecinForm(request.POST)
        if form.is_valid():
            # Appel à form.save(), qui crée un utilisateur et l'associe au médecin
            form.save()
            return redirect('vue_secretaire')  # Redirige après création
        else:
            # Debug : affiche les erreurs dans le terminal
            print(form.errors)
    else:
        form = MedecinForm()

    return render(request, 'creer_medecin.html', {'form': form})


@login_required
def creer_patient(request):
    if request.method == 'POST':
        form = PatientForm(request.POST)
        if form.is_valid():
            form.save()  # Crée un patient et l'utilisateur associé
            return redirect('vue_secretaire')  # Redirige après création
        else:
            print(form.errors)  # Debug : affiche les erreurs du formulaire
    else:
        form = PatientForm()

    return render(request, 'creer_patient.html', {'form': form})


#vuepatient

@login_required
@role_requis_patient
def vue_patient(request):
    patient = request.user.patient
    rendezvous = RendezVous.objects.filter(patient=patient)

    context = {
        'rendezvous': rendezvous,
    }
    return render(request, 'vue_patient.html', context)



