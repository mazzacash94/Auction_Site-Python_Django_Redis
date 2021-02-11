from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout as django_logout
from django.contrib import messages
from .forms import registrationForm


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


def registration(request):

    if request.method == 'POST':

        form = registrationForm(request.POST)

        if form.is_valid():

            form.save()
            return redirect('../')

        else:

            messages.error(request, 'Account Utente non Creato... Riprova!')

    else:

        form = registrationForm()

    return render(request, "registration.html", {'form': form})

# consente ad utente di effettuare il logout dal sito


def logout(request):

    django_logout(request)

    return redirect("../")
