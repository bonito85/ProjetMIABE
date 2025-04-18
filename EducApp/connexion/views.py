from django import forms
from .forms import LoginForm
from django.contrib.auth.models import User
from django.contrib import messages
from django.http import HttpResponse
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from django.template import loader
from django.shortcuts import render, redirect
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.sites.shortcuts import get_current_site
from django.conf import settings
from .tokens import generateToken 
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_text


# Vue de confirmation apres traitement de l'inscription
def confirmation_inscription(request):
    """Fonction de confirmation d'inscription"""
    return render(request, 'connexion/confirmation_inscription.html')

# Page d'index
def index(request): 
    template = loader.get_template('pages/index.html')
    return HttpResponse(template.render())




# Connexion au dahsboard utilisateur

def login_page(request):
    form = LoginForm()
    message = ''

    # Vérification de la méthode de la requête
    if request.method == 'POST':
        form = LoginForm(request.POST)
        # Verifier la validité du formulaire
        if form.is_valid():
            #Recuperer les données
            user = authenticate(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password']
            )
            if user is not None:
                # Connexion de l'utilisateur
                login(request, user)
                return render(request, 'connexion/login.html')
            
            else:
                message = 'Identifiant ou mot de passe incorrect'
    return render(request, 'connexion/login.html', {'form': form, 'message': message})

# Fonction d'inscription de l'utilisateur
def signup(request):
    """Fonction permettant a l'utilisateur de s'inscrire"""
    if request.method == 'POST': 
        username = request.POST['username']
        firstname = request.POST['firstname']
        lastname = request.POST['lastname']
        email = request.POST['email']
        password = request.POST['password']
        confirmpwd = request.POST['confirmpwd']
        # Vérification des champs
        if User.objects.filter(username=username):
            messages.add_message(request, messages.ERROR, 'Ce nom d\'utilisateur existe déjà')
            return render(request, 'connexion/signup.html', {'messages':messages.get_messages(request)})
        

        if len(username)>10:
            messages.add_message(request,messages.ERROR, 'Désolé ! Le nom d\'utilisateur ne doit pas être superieur a 10 caractère.')
            return render(request,'connexion/signup.html',{'messages':messages.get_messages(request)})
        if len(username)<5:
            messages.add_message(request,messages.ERROR, 'Désolé ! Le nom d\'utilisateur doit contenir plus de 5 caractères.')
            return render(request,'connexion/signup.html',{'messages':messages.get_messages(request)})
        if not username.isalnum():
            messages.add_message(request,messages.ERROR, 'Entrer un npm d\'utilisateur valide ')
            return render(request,'connexion/signup.html',{'messages':messages.get_messages(request)})

        if password != confirmpwd:
            messages.add_message(request,messages.ERROR, 'Mot de passe invalide :) ')
            return render(request,'connexion/signup.html',{'messages':messages.get_messages(request)})
        # Creation d'un utilisateur
        user = User.objects.create_user(username, email, password)
        user.first_name =firstname
        user.last_name = lastname
        user.is_active = False
        user.save()
        #Envoie de mail de confirmation
        current_site = get_current_site(request)
        email_subject = "Confirmez votre email - EducApp!"
        message = render_to_string("emailConfirmation.html", {
            'name': user.first_name,
            'domain': current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'token': generateToken.make_token(user),
        })

        try:
            email = EmailMessage(
                email_subject,
                message,
                settings.EMAIL_HOST_USER,
                [email],
            )
            email.fail_silently = False
            email.content_subtype = "html" 
            email.send()
            messages.add_message(request, messages.SUCCESS, 'Un email de confirmation a été envoyé à votre adresse email. Veuillez le confirmer pour vous connecter.')
        except Exception as e:
            messages.add_message(request, messages.ERROR, 'Erreur lors de l\'envoi de l\'email de confirmation. Veuillez réessayer plus tard.')
        return redirect('confirmation_inscription')
    return render(request, 'connexion/signup.html')

# Fonction de deconnexion
def logout_user(request):
    """Fonction de deconnexion"""
    logout(request)
    messages.add_message(request, messages.SUCCESS, 'Vous avez été déconnecté avec succès.')
    return redirect('login')


def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and generateToken.check_token(user, token):
        user.is_active  = True        
        user.save()
        messages.add_message(request,messages.SUCCESS, "You are account is activated you can login by filling the form below.")
        return render(request,"connexion/login.html",{'messages':messages.get_messages(request)})
    else:
        messages.add_message(request,messages.ERROR, 'Activation failed please try again')
        return render(request,'pages/index.html',{'messages':messages.get_messages(request)})
