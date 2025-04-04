"""
URL configuration for hospital project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from myhospital import views
from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)


from django.urls import path, include
from myhospital.views import ProtectedView
from django.contrib.auth import views as auth_views








urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.connexion, name='connexion'),

   

    #path('', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    #path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('secretaire/', views.vue_secretaire, name='vue_secretaire'),
    path('medecin/', views.vue_medecin, name='vue_medecin'),
    path('patient/', views.vue_patient, name='vue_patient'),
    path('inscription-secretaire/', views.inscription_secretaire, name='inscription_secretaire'),
    path("creer_rendezvous/", views.creer_rendezvous, name="creer_rendezvous"),
    path("creer_medecin/", views.creer_medecin, name="creer_medecin"),
    path("creer_patient/", views.creer_patient, name="creer_patient"),





    #path('acceuil/', views.acceuil, name='acceuil'), 
    path('deconnexion/', views.deconnexion, name='deconnexion'), 

    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    #path('api/protected/', ProtectedView.as_view(), name='protected_view'),
    #ajouter
    path('api/', include('myhospital.urls')),  # Inclut les URLs de l'application `myhospital`

]
