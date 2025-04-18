from django.urls import path
from . import views

app_name = 'library'

urlpatterns = [
    path('', views.home, name='home'),
    path('ressources/<int:pk>/', views.ressource_detail, name='ressource_detail'),

]