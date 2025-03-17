from django.shortcuts import render,redirect,get_object_or_404
from django.shortcuts import get_object_or_404
from .models import Participant, Presence, Seance
import geopy.distance
from django.contrib import messages

# Create your views here.
def accueil(request):
    return render(request, 'index.html')


def interface_admin(request):
    return render(request, 'admin_index.html')



def get_adresse_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def marquer_presence(request, seance_id):
    if request.method == 'POST':
        participant = get_object_or_404(Participant, telephone=request.user.telephone)
        seance = get_object_or_404(Seance, id=seance_id)
        
        adresse_ip = get_adresse_ip(request)
        latitude = request.POST.get('latitude')
        longitude = request.POST.get('longitude')

        Presence.objects.create(
            participant=participant,
            seance=seance,
            presence=True,
            adresse_ip=adresse_ip,
            latitude=latitude,
            longitude=longitude
        )

        messages.success(request, "Votre présence a été enregistrée avec succès.")
        return redirect('detail_seance', seance_id=seance.id)
    return render(request, 'presence/marquer_presence.html', {'seance': seance})




def verifier_localisation(latitude_user, longitude_user, latitude_cible, longitude_cible, rayon=0.1):
    """
    Vérifie si l'utilisateur est dans un rayon donné (en km) autour de la localisation cible.
    """
    if latitude_user and longitude_user:
        distance = geopy.distance.geodesic((latitude_user, longitude_user), (latitude_cible, longitude_cible)).km
        return distance <= rayon
    return False


def ajouter_seance(request):
    if request.method == 'POST':
        nom = request.POST.get('nom')
        description = request.POST.get('description')
        latitude = request.POST.get('latitude')
        longitude = request.POST.get('longitude')

        if not latitude or not longitude:
            messages.error(request, "Veuillez sélectionner un emplacement sur la carte.")
            return redirect('ajouter_seance')

        Seance.objects.create(
            nom=nom,
            description=description,
            latitude=float(latitude),
            longitude=float(longitude),
        )

        messages.success(request, "Séance ajoutée avec succès.")
        return redirect('liste_seances')

    return render(request, 'seance/ajouter_seance.html')