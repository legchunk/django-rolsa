from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name=''),
    path('login/', views.login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('register/', views.register, name='register'),
    path('settings/', views.settings, name='settings'),
    path('calculator/', views.calculator, name='calculator'),
    path('booking/', views.booking, name='booking'),
    path('about/', views.about, name='about'),
]
