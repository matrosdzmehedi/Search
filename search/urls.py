from django.urls import path
from .views import *
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    path('',HomeView.as_view(),name='home'),
    path('filter/',csrf_exempt( Filterview.as_view()),name='filter'),
   
]