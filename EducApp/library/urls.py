from django.urls import path
from . import views

app_name = 'library'

urlpatterns = [
    path('', views.home, name='home'),
    path('ressources/<int:pk>/', views.ressource_detail, name='ressource_detail'),
    #lien de recherche des ressources dans la bibliotheque
    path('search/', views.search, name='search'),
    #lien d'affichages de liste des ressources par categorie
    path('categories/', views.category_list, name='category_list'),
    #lien de details de chaque categorie
    path('categories/<int:pk>/', views.category_detail, name='category_detail'),

]