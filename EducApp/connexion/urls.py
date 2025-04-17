from django.urls import path
from . import views 

urlpatterns = [
    path('connexion/login/', views.login_page, name='login'),
    path('', views.index, name='index'),
    path('connexion/signup/', views.signup, name='signup'),  # Fixed typo here
    # Url de deconnexion
    path('logout/', views.logout_user, name='logout'),  # Fixed the view name here
    path('activate/<uidb64>/<token>', views.activate, name='activate'),
    # Url de confirmation d'inscription
    path('confirmation_inscription/', views.confirmation_inscription, name='confirmation_inscription'),
]