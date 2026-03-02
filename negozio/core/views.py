from django.shortcuts import render
from core.models import Prodotto, Ordine

def home(request):
    return render(request, "home.html")


def prodotti(request):
    prodotti = Prodotto.objects.all()

    context = {
        "prodotti" : prodotti
    }

    return render(request, "prodotti.html", context)


def ordini(request):
    ordini = Ordine.objects.all()

    context = {
        "ordini" : ordini
    }

    return render(request, "ordini.html", context)
    
