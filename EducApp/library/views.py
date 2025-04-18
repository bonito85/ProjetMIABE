from django.shortcuts import render
from django.shortcuts import render, get_object_or_404
from .models import Ressource, Category
from django.db.models import Q



# Creation de la vue pour la page d'accueil de la bibliothèque
def home(request): 
    ressources = Ressource.objects.order_by('-created_at')
    #categories = Category.objects.all()
    return render(request, 'library/home.html', {'ressources': ressources})

# Afficher les details des ressources de chaque elements 
def ressource_detail(request, pk):
    ressource = get_object_or_404(Ressource, pk=pk)
    return render(request, 'ressources/ressource_detail.html', {'ressource': ressource})