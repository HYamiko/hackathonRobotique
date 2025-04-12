from django.shortcuts import render,redirect,get_object_or_404
from django.shortcuts import get_object_or_404
from .models import Participant, Presence, Seance, Activite
import geopy.distance
from django.http import JsonResponse
from django.contrib import messages

# Create your views here.
def accueil(request):
    return render(request, 'index.html')


def interface_admin(request):
    return render(request, 'admin/admin_index.html')


def participants(request):
    participants = Participant.objects.all()
    return render(request, 'admin/participants.html', {'participants': participants})

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


def seances(request):
    seances = Seance.objects.all()
    activites = Activite.objects.all()
    return render(request, 'admin/seances.html', {'seances': seances, 'activites': activites})

def modifier_seance(request, seance_id):
    try:
        seance = Seance.objects.get(id=seance_id)
        
        if request.method == 'POST':
            titre=request.POST.get('titre')
            date_debut=request.POST.get('date_debut')
            date_fin=request.POST.get('date_fin')
            description=request.POST.get('description')


            seance.titre = titre
            seance.description = description
            seance.date_debut = date_debut
            seance.date_fin = date_fin
            seance.save()

            messages.success(request, "Séance modifiée avec succès.")
            return redirect('seance')
            
        activites = Activite.objects.all()
        return render(request, 'admin/seances.html', {
            'seance': seance,
            'activites': activites
        })
        
    except Seance.DoesNotExist:
        messages.error(request, "La séance demandée n'existe pas.")
        return redirect('seance')

def supprimer_seance(request, seance_id):
    try:
        seance = Seance.objects.get(id=seance_id)
        
        if request.method == 'POST':
            seance.delete()
            messages.success(request, "Séance supprimée avec succès.")
            return redirect('seance')
            
        return render(request, 'admin/seances.html', {'seance': seance})
        
    except Seance.DoesNotExist:
        messages.error(request, "Cette séance n'existe pas.")
        return redirect('seance')

def liste_activites(request):
    activites = Activite.objects.all()
    return render(request, 'admin/activites.html', {'activites': activites})

def ajouter_activite(request):
    if request.method == 'POST':
        code = request.POST.get('code')
        libelle = request.POST.get('libelle')
        Activite.objects.create(code=code, libelle=libelle)
        messages.success(request, 'Activité ajoutée avec succès !')
        return redirect('liste_activites')
    return redirect('liste_activites')

def modifier_activite(request, id):
    activite = Activite.objects.get(id=id)
    if request.method == 'POST':
        activite.code = request.POST.get('code')
        activite.libelle = request.POST.get('libelle')
        activite.save()
        messages.success(request, 'Activité modifiée avec succès !')
        return redirect('liste_activites')
    return redirect('liste_activites')

def supprimer_activite(request, id):
    activite = Activite.objects.get(id=id)
    if request.method == 'POST':
        activite.delete()
        messages.success(request, 'Activité supprimée avec succès !')
    return redirect('liste_activites')


def regenerer_code(request, id):
    try:
        activite = Activite.objects.get(id=id)
        nouveau_code = Activite.generate_unique_code()
        activite.code = nouveau_code
        activite.save()
        return JsonResponse({'success': True, 'new_code': nouveau_code})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})
    

def programmer_seance(request):
    if request.method == 'POST':
        try:
            Seance.objects.create(
                activite_id=request.POST.get('activite'),
                titre=request.POST.get('titre'),
                date_debut=request.POST.get('date_debut'),
                date_fin=request.POST.get('date_fin'),
                description=request.POST.get('description'),
                latitude=request.POST.get('latitude'),
                longitude=request.POST.get('longitude'),
            )
            messages.success(request, 'Séance créée avec succès!')
            return redirect('seance')
        except Exception as e:
            messages.error(request, f'Erreur: {str(e)}')
    
    activites = Activite.objects.all()
    return render(request, 'admin/seances.html', {'activites': activites})