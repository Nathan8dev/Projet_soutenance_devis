"""
URL configuration for devis project.

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
from django.urls import path, include
from gestion import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.accueil_site, name='accueil_site'),
    path('Inscription/', views.Inscription, name='inscription'),
    path('connexion/', views.Connexion, name='connexion'),
    path('accueil/',views.Accueil, name='accueil'),
    path('logout/', views.log_out, name='logout'),

    path('Add_client/', views.Ajouter_Client, name='Add_client'),
    path('Add_entreprise/', views.Ajouter_entreprise, name='Add_entreprise'),
    path('Liste_client/', views.Liste_client, name='liste_client'),
    path('detailclient/<int:id>/', views.Detail_client, name='detail_client'),
    path('clientAmodifier/<int:id>/', views.detail_client,name='modifier'),
    path('Modifier/<int:id>/', views.Modifier_client, name='Modifier'),
    path('afficher_devis/', views.Afficher_devis, name='afficher_devis'),
    path('delete_client/<int:id>/', views.Delete_client, name='delete'),


    path('creer_devis/', views.Creer_devis, name="creer_devis"),
    path('Devis_final/', views.DevisFinal, name="Devis_final"),



    path('rechercher_client/', views.Search_devis, name='rechercher_client'),
    path('pdf/', views.Generer_pdf, name="pdf"),
    path('word/', views.Generer_word, name="word"),
    path('liste_devis/', views.Liste_devis, name="liste_devis"),
    path('detail_devis/<int:numero>', views.Detail_devis, name="detail"),
    path('supprimer_devis/<int:numero>', views.Supprimer_devis, name="supprimer"),
]
