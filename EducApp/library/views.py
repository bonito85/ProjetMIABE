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

# Afficher les ressources par categorie
def category_list(request):
    categories = Category.objects.all()
    return render(request, 'ressources/category_list.html', {'categories': categories})

# Les details de chaque categorie
def category_detail(request, pk):
    category = get_object_or_404(Category, pk=pk)
    ressources = category.ressources.all()
    return render(request, 'ressources/category_detail.html', {
        'category': category,
        'ressources': ressources
    })


# Definition de la vue pour la page de recherche
def search(request):
    query = request.GET.get('q')
    if query:
        ressources = Ressource.objects.filter(
            Q(title__icontains=query) | Q(description__icontains=query)
        )
    else:
        ressources = Ressource.objects.all()
    return render(request, 'ressources/search_results.html', {'ressources': ressources})
