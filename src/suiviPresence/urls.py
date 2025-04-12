from django.conf import settings
from django.urls import path
from . import views
from django.conf.urls.static import static


urlpatterns = [
    path('', views.accueil, name='accueil'),
    path('interface/admin/', views.interface_admin, name='interface_admin'),
    path('seances/', views.seances, name="seance"),
    path('seances/modifier/<int:seance_id>/', views.modifier_seance, name="modifier_seance"),
    path('seances/supprimer/<int:seance_id>/', views.supprimer_seance, name="supprimer_seance"),
    path('activites/', views.liste_activites, name='liste_activites'),
    path('ajouter-activite/', views.ajouter_activite, name='ajouter_activite'),
    path('modifier-activite/<int:id>/', views.modifier_activite, name='modifier_activite'),
    path('supprimer-activite/<int:id>/', views.supprimer_activite, name='supprimer_activite'),
    path('regenerer-code/<int:id>/', views.regenerer_code, name='regenerer_code'),
    path('programmer-seance/', views.programmer_seance, name='programmer_seance'),
    path('participants/', views.participants, name="participant")
]