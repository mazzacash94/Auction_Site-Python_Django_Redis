from django.urls import path
from . import views

urlpatterns = [
    path('login', views.logIn, name='login'),
    path('registration', views.registration, name='registration'),
    path('logout', views.logout, name="logout"),

]
