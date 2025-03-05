from django.conf import settings
from django.urls import path
from . import views
from django.conf.urls.static import static


urlpatterns = [
    path('', views.accueil, name='accueil'),
    path('interface/admin/', views.interface_admin, name='interface_admin'),
]