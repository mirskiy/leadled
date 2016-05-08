from django.shortcuts import render
from django.views.generic.detail import DetailView

from .models import Action

# Create your views here.
class ActivateAction(DetailView):
    model = Action


