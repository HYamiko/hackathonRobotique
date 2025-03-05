from django.shortcuts import render

# Create your views here.
def accueil(request):
    return render(request, 'index.html')


def interface_admin(request):
    return render(request, 'admin_index.html')