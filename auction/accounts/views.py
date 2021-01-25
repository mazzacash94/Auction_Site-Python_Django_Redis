from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout as django_logout
from django.contrib import messages
from .forms import registrationForm
from app.models import Profile
from django.contrib.auth.models import User


# Create your views here.


# consente accesso ad utente e modifica ip con cui si è accessi nel caso in cui sia diverso dal precedente riportandone le informazioni nella console tramite sistema di logging

def logIn(request):

    if request.method == 'POST':

        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:

            login(request, user)
            return redirect("../")

        else:

            messages.error(request, "Username o Password Errati... Riprova!")

    return render(request, 'login.html')

# consente a visitatore di registrarsi al sito memorizzandone l'ip e riportandone l'esito nella console tramite sistema di logging

def registration(request):

    if request.method == 'POST':

        form = registrationForm(request.POST)

        if form.is_valid():

            form.save()
            users=User.objects.order_by("-date_joined")
            lastUser = User.objects.get(username=users[0])
            Profile.objects.create(user=lastUser)
            return redirect('../')

        else:

            messages.error(request, 'Account Utente non Creato... Riprova!')

    else:

        form = registrationForm()

    return render(request, "register.html", {'form':form})

# consente ad utente di effettuare il logout dal sito

def logout(request):

    django_logout(request)

    return redirect("../")