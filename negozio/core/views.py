from django.shortcuts import render
from core.models import Prodotto, Ordine

def index(request):
    return render(request, "index.html")


def prodotti(request):
    prodotti = Prodotto.objects.all()

    context = {
        "prodotti" : prodotti
    }

    if not prodotti:
        context = {
            "errore" : "prodotti non trovati"
        }

    return render(request, "prodotti.html", context)


def ordini(request):
    ordini = Ordine.objects.all()

    context = {
        "ordini" : ordini
    }

    if not ordini:
        context = {
            "errore" : "ordini non trovati"
        }

    return render(request, "ordini.html", context)
    
